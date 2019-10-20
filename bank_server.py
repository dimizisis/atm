
import pymongo
import random
from datetime import datetime

CLIENT = 'mongodb+srv://admin:admin@atm-fdfgm.gcp.mongodb.net/test?retryWrites=true&w=majority'

DATABASE = 'bank_db'

class BankServer():

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
    BALANCE_NOT_ENOUGH_ERR = 'Balance not enough to withdraw'
    BANKNOTES_NOT_VALID_ERR = 'Try another amount (banknotes: 20€, 50€)'
    DEPOSITION_FAILURE_ERR = 'Deposition failed'
    WITHDRAWAL_FAILURE_ERR = 'Withdrawal failed'
    CUSTOMER_PIN_CHANGE_FAILURE_ERR = 'Cannot change ping'
    USERNAME_TAKEN_ERR = 'Sorry, username already taken'

    def __init__(self, client, database):
        self.client = pymongo.MongoClient(client)
        self.db = self.client.get_database(database)

    def customer_exists(self, cid):
        '''
        Checks if customer's id exists in customers' collection
        Takes cid as argument (customer's id)
        Returns True if it exists
        Returns False if doesn't
        '''
        customer = self.db.customer.find_one({'cid': cid})
        if customer is not None:
            return True
        return False

    def insert_customer(self, username, full_name):
        '''
        Adds a customer to customers' collection
        Takes username as argument, generates id and pin.
        Returns True if addition succeeds
        Returns False if addition fails.
        '''
        try:
            cus = self.db.customer.find_one({'username': username})
            if cus is not None:
                print(self.USERNAME_TAKEN_ERR)
                return False, self.USERNAME_TAKEN_ERR
        except:
            print('Application crashed')
        try:
            cid = self.db.customer.count_documents({})+1
            customer = {'cid': cid, 'username': username, 'full_name': full_name, 'pin': self.generate_pin()}
            self.db.customer.insert_one(customer)
            self.init_balance(cid)
            print(self.CUSTOMER_ADDITION_SUCCESS_MSG + ' ' + username)
            return True, self.CUSTOMER_ADDITION_SUCCESS_MSG
        except:
            print(self.CUSTOMER_NOT_ADDED_ERR)
            return False, self.CUSTOMER_NOT_ADDED_ERR

    def delete_customer(self, cid=None, username=None):
        '''
        Removes a customer from customers' collection
        Takes id and/or username as arguments
        Returns True if removal succeeds
        Returns False if removal fails.
        '''
        if username is None:    # if we track the document by id
            try:
                self.db.customer.delete_one({'cid': cid})
                print(self.CUSTOMER_REMOVAL_SUCCESS_MSG + ' with id '+cid)
                return True, self.CUSTOMER_REMOVAL_SUCCESS_MSG
            except:
                print(self.CUSTOMER_NOT_REMOVED_ERR)
                return False, self.CUSTOMER_NOT_REMOVED_ERR
        # else we track the document by username
        try:
            self.db.customer.delete_one({'username': username})
            print(self.CUSTOMER_REMOVAL_SUCCESS_MSG +' with username ' +username)
            return True, self.CUSTOMER_REMOVAL_SUCCESS_MSG
        except:
            print(self.CUSTOMER_NOT_REMOVED_ERR)
            return False, self.CUSTOMER_NOT_REMOVED_ERR

    def change_customer_pin(self, cid):
        '''
        Changes customer's pin (based on id)
        with another random one
        '''
        try:
            self.db.customer.update_one({'cid': cid}, {'$set': {'pin': self.generate_pin()}})
            print(self.CUSTOMER_PIN_CHANGE_SUCCESS_MSG)
            return True, self.CUSTOMER_PIN_CHANGE_SUCCESS_MSG
        except:
            print(self.CUSTOMER_PIN_CHANGE_FAILURE_ERR)
            return False, self.CUSTOMER_PIN_CHANGE_FAILURE_ERR

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
            bid = cid = self.db.balance.count_documents({})+1
            balance_doc = {'bid': bid, 'cid': cid, 'balance': 0, 'last_updated': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}
            self.db.balance.insert_one(balance_doc)
            return True
        except:
            print(self.BALANCE_NOT_INIT_ERR)
            return False

    def withdraw(self, cid, amount):
        '''
        Customer withdraws from his account
        Takes cid and amount as arguements
        Returns True if withdrawal successful
        Returns False if withdrawal unsuccessful
        '''
        if not self.customer_exists(cid):
            print(self.CUSTOMER_DOES_NOT_EXIST_ERR)
            return False, self.CUSTOMER_DOES_NOT_EXIST_ERR

        if amount <= 0:
            print(self.AMOUNT_NOT_VALID_ERR)
            return False, self.AMOUNT_NOT_VALID_ERR

        if self.db.balance.find_one({'cid': cid}, {'balance': 1})['balance'] < amount:
            print(self.BALANCE_NOT_ENOUGH_ERR)
            return False, self.BALANCE_NOT_ENOUGH_ERR
        
        if not self.check_banknotes(amount):
            print(self.BANKNOTES_NOT_VALID_ERR)
            return False, self.BANKNOTES_NOT_VALID_ERR

        try:
            withdrawal_doc = {'wid': self.db.withdraw.count_documents({})+1, 'amount': amount, 'cid': cid, 'time': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}
            balance_doc = {'$inc': {'balance': -amount}, '$set': {'last_updated': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}}
            self.db.withdraw.insert_one(withdrawal_doc)
            self.db.balance.update_one({'cid': cid}, balance_doc)
            print(self.WITHDRAWAL_SUCCESS_MSG)
            return True, self.WITHDRAWAL_SUCCESS_MSG
        except:
            print(self.WITHDRAWAL_FAILURE_ERR)
            return False, self.WITHDRAWAL_FAILURE_ERR

    def check_banknotes(self, amount):
        '''
        Checks if amount is divided by 20 or 50 or 70
        Returns True if it is
        Returns False if not
        '''
        return (amount % 20 == 0 or amount % 50 == 0 or amount % 70 == 0)
        
    def deposit(self, cid, amount):
        '''
        Customer deposits into his account
        Takes cid and amount as arguements
        Returns True if deposition successful
        Returns False if deposition unsuccessful
        '''
        if not self.customer_exists(cid):
            print(self.CUSTOMER_DOES_NOT_EXIST_ERR)
            return False, self.CUSTOMER_DOES_NOT_EXIST_ERR
        
        if amount <= 0:
            print(self.AMOUNT_NOT_VALID_ERR)
            return False, self.AMOUNT_NOT_VALID_ERR

        try:
            deposition_doc = {'did': self.db.deposit.count_documents({})+1, 'amount': amount, 'cid': cid, 'time': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}
            balance_doc = {'$inc': {'balance': amount}, '$set': {'last_updated': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}}
            self.db.deposit.insert_one(deposition_doc)
            self.db.balance.update_one({'cid': cid}, balance_doc)
            print(self.DEPOSITION_SUCCESS_MSG)
            return True, self.DEPOSITION_SUCCESS_MSG
        except:
            print(self.DEPOSITION_FAILURE_ERR)
            return False, self.DEPOSITION_FAILURE_ERR
 
if __name__ == '__main__':
    bank_server = BankServer(CLIENT, DATABASE)
    # bank_server.insert_customer('dimizisis', 'ZISIS DIMITRIOS')
    # bank_server.deposit(2, 540)
    # bank_server.withdraw(1, 10)
    # bank_server.change_customer_pin(1)