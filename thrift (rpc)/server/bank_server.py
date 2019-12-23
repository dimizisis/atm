
import thrift_gen.OperationService as OperationService
from thrift_gen.ttypes import Request

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
import pymongo
import os
import configparser
from datetime import datetime
from return_messages import *
from thrift_gen.constants import *

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

def connect_to_db(client_link, db_name):
    client = pymongo.MongoClient(client_link)
    db = client.get_database(db_name)

    return client, db

class OperationHandler:
    def __init__(self, client, database):
        self.log = {}
        self.client = client
        self.db = database

    def withdraw(self, request):
        '''
        Customer withdraws from his account\n
        Takes cid and amount as arguements\n
        Returns True if withdrawal successful\n
        Returns False if withdrawal unsuccessful
        '''

        customer = self.authenticate(request.username, request.pin)
        if customer is None:    # if None is returned (no customer with these credentials exists)
            return WRONG_CREDENTIALS

        if request.amount <= 0:
            return AMOUNT_NOT_VALID_ERR

        if self.db.balance.find_one({'cid': customer['cid']}, {'balance': 1})['balance'] < request.amount:
            return BALANCE_NOT_ENOUGH_ERR
        
        if not self.check_banknotes(request.amount):
            return BANKNOTES_NOT_VALID_ERR

        if self.daily_withdrawal_limit_reached(customer['cid'], request.amount):
            return DAILY_WITHDRAWAL_LIMIT_ERR

        try:
            withdrawal_doc = {'wid': self.db.withdraw.count_documents({})+1, 'amount': request.amount, 'cid': customer['cid'], 'time': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}
            balance_doc = {'$inc': {'balance': -float(request.amount)}, '$set': {'last_updated': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}}
            self.db.withdraw.insert_one(withdrawal_doc)
            self.db.balance.update_one({'cid': customer['cid']}, balance_doc)
            print(WITHDRAWAL_SUCCESS_MSG)
            return WITHDRAWAL_SUCCESS_MSG
        except:
            print(WITHDRAWAL_FAILURE_ERR)
            return WITHDRAWAL_FAILURE_ERR

    def daily_withdrawal_limit_reached(self, cid, amount):
        '''
        Checks if customer reached his daily withdrawal limit (Set as constant 850)\n
        Takes cid as parameter\n
        Returns True if limit reached\n
        Returns False if limit is not reached
        '''
        if amount > DAILY_WITHDRAWL_LIMIT:
            return False
        try:
            curr_date = datetime.today().strftime('%Y-%m-%d')
        except Exception as e:
            print(e)
        pipe = [{ "$match": { 'cid': { "$eq": cid } } }, { "$match": { 'time': { "$regex": '.*'+curr_date+'.*' } } }, {'$group': {'_id': "$cid", 'total_amount': {'$sum': '$amount'}}}]
        results = list(self.db.withdraw.aggregate(pipeline=pipe)) # we get a list with one dict inside (cid and amount that was withdrawn today)
        if results:
            total_amount_withdrawn = results[0]['total_amount'] 
            if total_amount_withdrawn > DAILY_WITHDRAWL_LIMIT:
                return True
        return False

    def check_banknotes(self, amount):
        '''
        Checks if amount is divided by 20 or 50 or 70\n
        Returns True if it is\n
        Returns False if not
        '''
        return (amount % 20 == 0 or amount % 50 == 0 or amount % 70 == 0)

    def deposit(self, request):
        '''
        Customer deposits into his account\n
        Takes cid and amount as arguements\n
        Returns True if deposition successful\n
        Returns False if deposition unsuccessful
        '''

        customer = self.authenticate(request.username, request.pin)
        if customer is None:    # if None is returned (no customer with these credentials exists)
            return WRONG_CREDENTIALS
        
        if request.amount <= 0:
            return AMOUNT_NOT_VALID_ERR

        try:
            deposition_doc = {'did': self.db.deposit.count_documents({})+1, 'amount': request.amount, 'cid': customer['cid'], 'time': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}
            balance_doc = {'$inc': {'balance': float(request.amount)}, '$set': {'last_updated': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}}
            self.db.deposit.insert_one(deposition_doc)
            self.db.balance.update_one({'cid': customer['cid']}, balance_doc)
            return DEPOSITION_SUCCESS_MSG
        except:
            return DEPOSITION_FAILURE_ERR

    def get_balance(self, request):
        '''
        Informs customer about his balance\n
        Takes cid (customer id) as argument\n
        Returns balance if found\n
        Returns None if not found
        '''
        customer = self.authenticate(request.username, request.pin)
        if customer is None:    # if None is returned (no customer with these credentials exists)
            return WRONG_CREDENTIALS

        try:
            self.charge(customer['cid'], BALANCE_INFO_CHARGES, BALANCE_INFO_CHARGES_DESCR)
            balance = self.db.balance.find_one({'cid': customer['cid']}, {'balance': 1})['balance']
            return format(balance, '.3f')
        except:
            return BALANCE_NOT_FOUND_ERR
        
        return None

    def charge(self, cid, amount, descr):
        '''
        Charges customer when is asking about balance information\n
        Takes cid (customer id), charge amount and charge description as parameters
        '''
        try:
            balance_doc = {'$inc': {'balance': -amount}, '$set': {'last_updated': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}}
            chid = self.db.charge.count_documents({})+1
            charge_doc = {'chid': chid, 'cid': cid, 'amount': amount, 'descr': descr, 'date': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}
            self.db.balance.update_one({'cid': cid}, balance_doc)
            self.db.charge.insert_one(charge_doc)
            print('Customer charged')
        except Exception as e:
            print(e)

    def find_customer(self, username):
        '''
        Checks if customer's username exists in customers' collection\n
        Takes username as argument\n
        Returns cid (customer's id) if customer exists\n
        Returns None if he doesn't
        '''
        customer = self.db.customer.find_one({'username': username})
        if customer is not None:
            return customer
        return None
    
    def change_pin(self, request):
        '''
        Changes customer's pin (based on id)\n
        with another random one
        '''
        customer = self.authenticate(request.username, request.pin)
        if customer is None:    # if None is returned (no customer with these credentials exists)
            return WRONG_CREDENTIALS
        try:
            self.db.customer.update_one({'cid': customer['cid']}, {'$set': {'pin': request.new_pin}})
            return CUSTOMER_PIN_CHANGE_SUCCESS_MSG
        except:
            return CUSTOMER_PIN_CHANGE_FAILURE_ERR

    def authenticate(self, username, pin):
        '''
        Checks customer's credentials\n
        Takes customer's entered username, pin as arguments\n
        If username & pin match, returns True\n
        If username & pin do not match, returns False
        '''
        customer = self.find_customer(username)
        if customer is not None:
            r_pin = customer['pin']    # Get pin from database
            if r_pin == pin:
                return customer
        return None

if __name__ == '__main__':

    host, port, client_link, database_name = read_config_file() # read settings from .ini file (configuration file)
    client, database = connect_to_db(client_link=client_link, db_name=database_name)    # connect to database (MongoDB Atlas) before we proceed to handler

    handler = OperationHandler(client, database)    # create our handler
    processor = OperationService.Processor(handler)
    transport = TSocket.TServerSocket(host=host, port=port)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)    # multithreaded server

    print(f'serving at {host} {port}')
    server.serve()
