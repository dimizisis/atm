
import pymongo
from datetime import datetime

CUSTOMER_ADDITION_SUCCESS_MSG = 'Successfully added customer'

CUSTOMER_NOT_ADDED_ERR = 'Customer cannot be added to database'
USERNAME_TAKEN_ERR = 'Sorry, username already taken'
BALANCE_NOT_INIT_ERR = 'Balance not initialized'

CLIENT = 'mongodb+srv://admin:admin@atm-fdfgm.gcp.mongodb.net/bank_db'
DATABASE_NAME = 'bank_db'

print('Connecting to database...\n')

client = pymongo.MongoClient(CLIENT)
db = client.get_database(DATABASE_NAME)

def init_balance(cid):
    '''
    Initializes new customer's balance
    '''
    try:
        bid = db.balance.count_documents({})+1
        balance_doc = {'bid': bid, 'cid': cid, 'balance': 0.0, 'last_updated': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}
        db.balance.insert_one(balance_doc)
        return True
    except:
        print(BALANCE_NOT_INIT_ERR)
        return False

def insert_customer(username, pin, full_name):
    '''
    Adds a customer to customers' collection\n
    Takes username as argument, generates id and pin\n
    Returns True if addition succeeds\n
    Returns False if addition fails
    '''
    try:
        cus = db.customer.find_one({'username': username})
        if cus is not None:
            return USERNAME_TAKEN_ERR
    except:
        print('Application crashed')
    try:
        cid = db.customer.count_documents({})+1
        customer = {'cid': cid, 'username': username, 'full_name': full_name, 'pin': pin}
        db.customer.insert_one(customer)
        init_balance(cid)
        return CUSTOMER_ADDITION_SUCCESS_MSG
    except Exception as e:
        print(e)
        return CUSTOMER_NOT_ADDED_ERR

if __name__ == '__main__':
    import sys
    username = input('Enter customer''s username: ')
    print()
    pin = input('Enter customer''s pin: ')
    print()
    full_name = input('Enter customer''s full name: ')
    print()
    print(insert_customer(username, int(pin), full_name))
