
import pika
import uuid
import sys

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

    def call(self, output_msg):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='atm_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=output_msg)
        while self.response is None:
            self.connection.process_data_events()
        return self.response

if __name__ == '__main__':

    bank_client = BankClient()
    response = bank_client.call(' '.join(sys.argv[1:]))     # send the parameters as they are
    print(response.decode('UTF-8')) # we add decode to avoid printing 'b' character
