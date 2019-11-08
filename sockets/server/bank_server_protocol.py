from datetime import datetime
import random
import pymongo
from return_messages import *
from constants import *
from Lib.server import ServerProtocol

class BankServerProtocol(ServerProtocol):

    def __init__(self, client, database):
        self.client = pymongo.MongoClient(client)
        self.db = self.client.get_database(database)

    def process_request(self, input_msg):
        print('Received message from client: ', input_msg)
        arr = input_msg.split()
        result = self.perform_action(arr)
        return str(result)
        
    def perform_action(self, arr):

        username = arr[0]   # String we get according to protocol: <USERNAME> <PIN> <ACTION> ...
        pin = int(arr[1])
        action = arr[2]

        customer = self.authenticate(username, pin)
        if customer is not None:

            if action == 'WITHDRAW':
                amount = arr[3]
                return self.withdraw(customer['cid'], float(amount))
                
            elif action == 'DEPOSIT':
                amount = arr[3]
                return self.deposit(customer['cid'], float(amount))
            
            elif action == 'CHANGE_PIN':
                new_pin = int(arr[3])
                return self.change_customer_pin(customer['cid'], new_pin)

            elif action == 'GET_BALANCE':
                return self.get_customer_balance(customer['cid'])

            else:
                return ACTION_NOT_FOUND

        return WRONG_CREDENTIALS

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
            self.charge(cid, BALANCE_INFO_CHARGES, BALANCE_INFO_CHARGES_DESCR)
            balance = self.db.balance.find_one({'cid': cid}, {'balance': 1})['balance']
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
                return USERNAME_TAKEN_ERR
        except:
            print('Application crashed')
        try:
            cid = self.db.customer.count_documents({})+1
            customer = {'cid': cid, 'username': username, 'full_name': full_name, 'pin': self.generate_pin()}
            self.db.customer.insert_one(customer)
            self.init_balance(cid)
            print(CUSTOMER_ADDITION_SUCCESS_MSG + ' ' + username)
            return CUSTOMER_ADDITION_SUCCESS_MSG
        except:
            return CUSTOMER_NOT_ADDED_ERR

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
                print(CUSTOMER_REMOVAL_SUCCESS_MSG + ' with id '+cid)
                return CUSTOMER_REMOVAL_SUCCESS_MSG
            except:
                print(CUSTOMER_NOT_REMOVED_ERR)
                return CUSTOMER_NOT_REMOVED_ERR
        # else we track the document by username
        try:
            self.db.customer.delete_one({'username': username})
            print(CUSTOMER_REMOVAL_SUCCESS_MSG +' with username ' +username)
            return CUSTOMER_REMOVAL_SUCCESS_MSG
        except:
            return CUSTOMER_NOT_REMOVED_ERR

    def change_customer_pin(self, cid, new_pin):
        '''
        Changes customer's pin (based on id)\n
        with another random one
        '''
        try:
            self.db.customer.update_one({'cid': cid}, {'$set': {'pin': new_pin}})
            return CUSTOMER_PIN_CHANGE_SUCCESS_MSG
        except:
            return CUSTOMER_PIN_CHANGE_FAILURE_ERR

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
            print(BALANCE_NOT_INIT_ERR)
            return False

    def withdraw(self, cid, amount):
        '''
        Customer withdraws from his account\n
        Takes cid and amount as arguements\n
        Returns True if withdrawal successful\n
        Returns False if withdrawal unsuccessful
        '''

        if amount <= 0:
            return AMOUNT_NOT_VALID_ERR

        if self.db.balance.find_one({'cid': cid}, {'balance': 1})['balance'] < amount:
            return BALANCE_NOT_ENOUGH_ERR
        
        if not self.check_banknotes(amount):
            return BANKNOTES_NOT_VALID_ERR

        if self.daily_withdrawal_limit_reached(cid, amount):
            return DAILY_WITHDRAWAL_LIMIT_ERR

        try:
            withdrawal_doc = {'wid': self.db.withdraw.count_documents({})+1, 'amount': amount, 'cid': cid, 'time': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}
            balance_doc = {'$inc': {'balance': -float(amount)}, '$set': {'last_updated': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}}
            self.db.withdraw.insert_one(withdrawal_doc)
            self.db.balance.update_one({'cid': cid}, balance_doc)
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
        
    def deposit(self, cid, amount):
        '''
        Customer deposits into his account\n
        Takes cid and amount as arguements\n
        Returns True if deposition successful\n
        Returns False if deposition unsuccessful
        '''
        
        if amount <= 0:
            return AMOUNT_NOT_VALID_ERR

        try:
            deposition_doc = {'did': self.db.deposit.count_documents({})+1, 'amount': amount, 'cid': cid, 'time': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}
            balance_doc = {'$inc': {'balance': float(amount)}, '$set': {'last_updated': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}}
            self.db.deposit.insert_one(deposition_doc)
            self.db.balance.update_one({'cid': cid}, balance_doc)
            return DEPOSITION_SUCCESS_MSG
        except:
            return DEPOSITION_FAILURE_ERR
