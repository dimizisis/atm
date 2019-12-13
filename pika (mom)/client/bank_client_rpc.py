
import pika
import uuid
import sys

FAILED_TO_CONNECT = 'Failed to connect to the server. Please try again later.'

class BankClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, action, username, pin, amount, new_pin):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='atm_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=self.prepare_request(action, username, pin, amount, new_pin))
        while self.response is None:
            self.connection.process_data_events()
        return self.response

    def prepare_request(self, action, username, pin, amount, new_pin):
        '''
        Given all the parameters from client,
        creates the proper string and returns it
        '''
        return username + ' ' + pin + ' ' + action + (' ' + amount if amount is not None else '') + (new_pin if new_pin is not None else '')