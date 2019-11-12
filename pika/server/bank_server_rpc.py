
import pika
import os
import configparser
from bank_server_protocol import BankServerProtocol

CONFIG_FILENAME = 'config.ini'
 
def read_config_file():
    '''
    Reads config file, which contains client, database name and host\n
    Config filename set as constant (config.ini)
    '''
    try:
        config = configparser.ConfigParser()
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        initfile = os.path.join(curr_dir, CONFIG_FILENAME)
        config.read(initfile)
        client = config.get('DB_SETTINGS', 'CLIENT')
        database_name = config.get('DB_SETTINGS', 'DATABASE_NAME')
        host = config.get('SERVER_SETTINGS', 'HOST')
        return  client, database_name, host
    except Exception as e:
        print(e)

client, db_name, host = read_config_file()

protocol = BankServerProtocol(client, db_name)  # we add this before everything else in order to connect with the database first (takes a few secs)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=host))

channel = connection.channel()

channel.queue_declare(queue='atm_queue')

def on_request(ch, method, props, body):

    out_msg = str(body.decode('UTF-8'))

    response = protocol.process_request(out_msg)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='atm_queue', on_message_callback=on_request)

print('Awaiting RPC requests')
channel.start_consuming()
