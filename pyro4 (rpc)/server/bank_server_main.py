
import Pyro4
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
        return  client, database_name
    except Exception as e:
        print(e)

def start_name_server():
    import subprocess
    os.popen('python -m Pyro4.naming') # executing python -m Pyro4.naming (command line) in order to start our name server

if __name__ == '__main__':
    client, database = read_config_file()

    start_name_server()

    daemon = Pyro4.Daemon()                # make a Pyro daemon
    ns = Pyro4.locateNS()                  # find the name server
    uri = daemon.register(BankServer(client, database))   # register the greeting maker as a Pyro object
    ns.register('bank_server', uri)   # register the object with a name in the name server

    daemon.requestLoop()                   # start the event loop of the server to wait for calls