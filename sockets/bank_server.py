
import pymongo
import random
from datetime import datetime
import socket
import threading
from abc import ABCMeta, abstractmethod
from Lib.server import MultiThreadedServer, ServerProtocol
import configparser
import os

CONFIG_FILENAME = 'config.ini'

class BankServerProtocol(ServerProtocol):

    # MSGS
    DEPOSITION_SUCCESS_MSG = 'Deposition successful'
    WITHDRAWAL_SUCCESS_MSG = 'Withdrawal successful'
    CUSTOMER_ADDITION_SUCCESS_MSG = 'Successfully added customer'
    CUSTOMER_REMOVAL_SUCCESS_MSG = 'Successfully removed customer'
    CUSTOMER_PIN_CHANGE_SUCCESS_MSG = 'Successfully changed pin'

    # ERRORS
    CUSTOMER_DOES_NOT_EXIST_ERR = 'Customer does not exist'
    AMOUNT_NOT_VALID_ERR = 'Not a valid amount'
    CUSTOMER_NOT_ADDED_ERR = 'Customer cannot be added to database'
    CUSTOMER_NOT_REMOVED_ERR = 'Customer cannot be removed from database'
    BALANCE_NOT_INIT_ERR = 'Balance not initialized'
    BALANCE_NOT_FOUND_ERR = 'Balance not found'
    BALANCE_NOT_ENOUGH_ERR = 'Balance not enough to withdraw'
    BANKNOTES_NOT_VALID_ERR = 'Try another amount (banknotes: 20€, 50€)'
    DEPOSITION_FAILURE_ERR = 'Deposition failed'
    WITHDRAWAL_FAILURE_ERR = 'Withdrawal failed'
    CUSTOMER_PIN_CHANGE_FAILURE_ERR = 'Cannot change ping'
    USERNAME_TAKEN_ERR = 'Sorry, username already taken'

    # CHARGES
    BALANCE_INFO_CHARGES = 0.2

    # CHARGE_DESCR
    BALANCE_INFO_CHARGES_DESCR = "Information about customer's balance"

    # DAILY WITHDRAWAL LIMIT
    DAILY_WITHDRAWL_LIMIT = 850

    def __init__(self, client, database):
        self.client = pymongo.MongoClient(client)
        self.db = self.client.get_database(database)

    def process_request(self, input_msg):
        print('Received message from client: ', input_msg)
        arr = input_msg.split()
        result = self.perform_action(arr)
        return str(result)
        
    def perform_action(self, arr):

        username = arr[0]
        pin = int(arr[1])
        action = arr[2]

        customer = self.authenticate(username, pin)
        if customer is not None:

            if action == 'WITHDRAW':
                amount = arr[3]
                if self.withdraw(customer['cid'], amount):
                    return True
                return False
                
            elif action == 'DEPOSIT':
                amount = arr[3]
                if self.deposit(customer['cid'], amount):
                    return True
                return False
            
            elif action == 'CHANGE_PIN':
                new_pin = int(arr[3])
                if self.change_customer_pin(customer['cid'], new_pin):
                    return True
                return False

            elif action == 'GET_BALANCE':
                balance = self.get_customer_balance(customer['cid'])
                if balance is not None:
                    return format(balance, '.3f')
                else:
                    return False

        return False

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

    def get_customer_balance(self, cid):
        '''
        Informs customer about his balance\n
        Takes cid (customer id) as argument\n
        Returns balance if found\n
        Returns None if not found
        '''
        try:
            balance = self.db.balance.find_one({'cid': cid}, {'balance': 1})['balance']
            self.charge(cid, self.BALANCE_INFO_CHARGES, self.BALANCE_INFO_CHARGES_DESCR)
            return balance
        except:
            print(BALANCE_NOT_FOUND_ERR)
        
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

    def insert_customer(self, username, full_name):
        '''
        Adds a customer to customers' collection\n
        Takes username as argument, generates id and pin\n
        Returns True if addition succeeds\n
        Returns False if addition fails
        '''
        try:
            cus = self.db.customer.find_one({'username': username})
            if cus is not None:
                print(self.USERNAME_TAKEN_ERR)
                return False
        except:
            print('Application crashed')
        try:
            cid = self.db.customer.count_documents({})+1
            customer = {'cid': cid, 'username': username, 'full_name': full_name, 'pin': self.generate_pin()}
            self.db.customer.insert_one(customer)
            self.init_balance(cid)
            print(self.CUSTOMER_ADDITION_SUCCESS_MSG + ' ' + username)
            return True
        except:
            print(self.CUSTOMER_NOT_ADDED_ERR)
            return False

    def delete_customer(self, cid=None, username=None):
        '''
        Removes a customer from customers' collection\n
        Takes id and/or username as arguments\n
        Returns True if removal succeeds\n
        Returns False if removal fails
        '''
        if username is None:    # if we track the document by id
            try:
                self.db.customer.delete_one({'cid': cid})
                print(self.CUSTOMER_REMOVAL_SUCCESS_MSG + ' with id '+cid)
                return True
            except:
                print(self.CUSTOMER_NOT_REMOVED_ERR)
                return False
        # else we track the document by username
        try:
            self.db.customer.delete_one({'username': username})
            print(self.CUSTOMER_REMOVAL_SUCCESS_MSG +' with username ' +username)
            return True
        except:
            print(self.CUSTOMER_NOT_REMOVED_ERR)
            return False

    def change_customer_pin(self, cid, new_pin):
        '''
        Changes customer's pin (based on id)\n
        with another random one
        '''
        try:
            self.db.customer.update_one({'cid': cid}, {'$set': {'pin': new_pin}})
            print(self.CUSTOMER_PIN_CHANGE_SUCCESS_MSG)
            return True
        except:
            print(self.CUSTOMER_PIN_CHANGE_FAILURE_ERR)
            return False

    def generate_pin(self):
        '''
        Generates random 4-digit pin and returns it
        '''
        return random.randint(999, 9999)

    def init_balance(self, cid):
        '''
        Initializes new customer's balance
        '''
        try:
            bid = self.db.balance.count_documents({})+1
            balance_doc = {'bid': bid, 'cid': cid, 'balance': 0.0, 'last_updated': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}
            self.db.balance.insert_one(balance_doc)
            return True
        except:
            print(self.BALANCE_NOT_INIT_ERR)
            return False

    def withdraw(self, cid, amount):
        '''
        Customer withdraws from his account\n
        Takes cid and amount as arguements\n
        Returns True if withdrawal successful\n
        Returns False if withdrawal unsuccessful
        '''

        if amount <= 0:
            print(self.AMOUNT_NOT_VALID_ERR)
            return False

        if self.db.balance.find_one({'cid': cid}, {'balance': 1})['balance'] < amount:
            print(self.BALANCE_NOT_ENOUGH_ERR)
            return False
        
        if not self.check_banknotes(amount):
            print(self.BANKNOTES_NOT_VALID_ERR)
            return False

        if self.daily_withdrawal_limit_reached(cid):
            print(self.DAILY_WITHDRAWAL_LIMIT_ERR)
            return False

        try:
            withdrawal_doc = {'wid': self.db.withdraw.count_documents({})+1, 'amount': amount, 'cid': cid, 'time': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}
            balance_doc = {'$inc': {'balance': -float(amount)}, '$set': {'last_updated': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}}
            self.db.withdraw.insert_one(withdrawal_doc)
            self.db.balance.update_one({'cid': cid}, balance_doc)
            print(self.WITHDRAWAL_SUCCESS_MSG)
            return True
        except:
            print(self.WITHDRAWAL_FAILURE_ERR)
            return False

    def daily_withdrawal_limit_reached(self, cid):
        '''
        Checks if customer reached his daily withdrawal limit (Set as constant 850)\n
        Takes cid as parameter\n
        Returns True if limit reached\n
        Returns False if limit is not reached
        '''
        curr_date = datetime.today().strftime('%Y-%m-%d')
        pipe = [{ "$match": { 'cid': { "$eq": cid } } }, { "$match": { 'time': { "$regex": '.*'+curr_date+'.*' } } }, {'$group': {'_id': "$cid", 'total_amount': {'$sum': '$amount'}}}]
        results = list(self.db.withdraw.aggregate(pipeline=pipe)) # we get a list with one dict inside (cid and amount that was withdrawn today)
        total_amount_withdrawn = results[0]['total_amount'] 

        if total_amount_withdrawn > self.DAILY_WITHDRAWL_LIMIT:
            return True
        return False

    def check_banknotes(self, amount):
        '''
        Checks if amount is divided by 20 or 50 or 70\n
        Returns True if it is\n
        Returns False if not
        '''
        return (amount % 20 == 0 or amount % 50 == 0 or amount % 70 == 0)
        
    def deposit(self, cid, amount):
        '''
        Customer deposits into his account\n
        Takes cid and amount as arguements\n
        Returns True if deposition successful\n
        Returns False if deposition unsuccessful
        '''
        
        if amount <= 0:
            print(self.AMOUNT_NOT_VALID_ERR)
            return False

        try:
            deposition_doc = {'did': self.db.deposit.count_documents({})+1, 'amount': amount, 'cid': cid, 'time': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}
            balance_doc = {'$inc': {'balance': float(amount)}, '$set': {'last_updated': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}}
            self.db.deposit.insert_one(deposition_doc)
            self.db.balance.update_one({'cid': cid}, balance_doc)
            print(self.DEPOSITION_SUCCESS_MSG)
            return True
        except:
            print(self.DEPOSITION_FAILURE_ERR)
            return False
 
def read_config_file():
    try:
        config = configparser.ConfigParser()
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        initfile = os.path.join(curr_dir, CONFIG_FILENAME)
        config.read(initfile)
        client = config.get('SETTINGS', 'CLIENT')
        database_name = config.get('SETTINGS', 'DATABASE_NAME')
        return client, database_name
    except Exception as e:
        print(e)

if __name__ == '__main__':
    client, database = read_config_file()
    protocol = BankServerProtocol(client, database)
    protocol.daily_withdrawal_limit_reached(2)
    bank_server = MultiThreadedServer(protocol=protocol)
    # bank_server.listen()
    # bank_server.insert_customer('dimizisis', 'ZISIS DIMITRIOS')
    # bank_server.deposit(2, 540)
    # bank_server.withdraw(1, 10)
    # bank_server.change_customer_pin(1)
