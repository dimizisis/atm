
import pymongo
import random
from datetime import datetime

CLIENT = 'mongodb+srv://admin:admin@atm-fdfgm.gcp.mongodb.net/test?retryWrites=true&w=majority'

DATABASE = 'bank_db'

class BankServer():

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
        customer = self.db.customer.find_one({}, {'id': cid})
        if customer is not None:
            return True
        return False

    def insert_customer(self, username):
        '''
        Adds a customer to customers' collection
        Takes username as argument, generates id and pin.
        Returns True if addition succeeds
        Returns False if addition fails.
        '''
        try:
            cid = self.db.customer.count_documents({})+1
            customer = {'cid': cid, 'username': username, 'pin': self.generate_pin()}
            self.db.customer.insert_one(customer)
            self.init_balance(cid)
            print('Successfully added customer '+ username)
            return True
        except Exception as e:
            print('Something went wrong!')
            print(e)
            return False


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
                print('Sucessful removed customer with id '+cid)
                return True
            except:
                print('Unsucessful removal!')
                return False
        # else we track the document by username
        try:
            self.db.customer.delete_one({'username': username})
            print('Sucessful removed customer '+username)
            return True
        except:
            print('Unsucessful removal!')
            return False

    def change_customer_pin(self, cid):
        '''
        Changes customer's pin (based on id)
        with another random one
        '''
        self.db.customer.update_one({'cid': cid}, {'pin': self.generate_pin()})

    def generate_pin(self):
        '''
        Generates random 4-digit pin and returns it
        '''
        return random.randint(999, 9999)

    def init_balance(self, cid):
        '''
        Initializes customer's new balance
        '''
        try:
            balance_doc = {'cid': cid, 'balance': 0, 'last_updated': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}
            self.db.balance.insert_one(balance_doc)
        except:
            print('Balance not initialized!')

    def withdraw(self, cid, amount):
        '''
        Customer withdraws from his account
        Takes cid and amount as arguements
        Returns True if withdrawal successful
        Returns False if withdrawal unsuccessful
        '''
        # if self.customer_exists(cid):
        #     print(self.db.balance.find_one({'cid': cid}, { '_id': 0, 'balance': 1 }))
        # # if self.db.balance.find_one({'id': id}, { '_id': 0, 'balance': 1 }):

    def deposit(self, cid, amount):
        '''
        Customer deposits into his account
        Takes cid and amount as arguements
        Returns True if deposition successful
        Returns False if deposition unsuccessful
        '''
        if self.customer_exists(cid) and amount > 0:
            deposit_doc = {'did': self.db.deposit.count_documents({})+1, 'amount': amount, 'cid': cid, 'time': datetime.today().strftime('%Y-%m-%d')}
            balance_doc = {'$inc': {'balance': amount}, '$set': {'last_updated': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}}
            self.db.deposit.insert_one(deposit_doc)
            self.db.balance.update_one({'cid': cid}, balance_doc)
            print('Deposition successful!')
            return True
        print('Deposition unsuccessful!')   
 
if __name__ == '__main__':
    bank_server = BankServer(CLIENT, DATABASE)
    bank_server.insert_customer('dimizisis')
    bank_server.deposit(1, 320)