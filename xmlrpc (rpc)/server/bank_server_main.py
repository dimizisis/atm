
from xmlrpc.server import SimpleXMLRPCServer
from bank_server import BankServer
import configparser
import os

CONFIG_FILENAME = 'config.ini'
 
def read_config_file():
    '''
    Reads config file, which contains client and database name\n
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
        port = config.get('SERVER_SETTINGS', 'PORT')
        return  host, int(port), client, database_name
    except Exception as e:
        print(e)

if __name__ == '__main__':
    host, port, client, database = read_config_file()

    server = SimpleXMLRPCServer((host, port))
    server.register_instance(BankServer(client, database))
    server.serve_forever()