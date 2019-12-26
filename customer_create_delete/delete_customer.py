
import pymongo

CUSTOMER_NOT_REMOVED_ERR = 'Customer cannot be removed from database'
CUSTOMER_REMOVAL_SUCCESS_MSG = 'Successfully removed customer'

CLIENT = 'mongodb+srv://admin:admin@atm-fdfgm.gcp.mongodb.net/bank_db'
DATABASE_NAME = 'bank_db'

print('Connecting to database...\n')

client = pymongo.MongoClient(CLIENT)
db = client.get_database(DATABASE_NAME)

def delete_customer(username):
    '''
    Removes a customer from customers' collection\n
    Takes id and/or username as arguments\n
    Returns True if removal succeeds\n
    Returns False if removal fails
    '''
    # we track the document by username
    try:
        cus = db.customer.find_one({'username': username})
        db.customer.delete_one({'username': username})
        db.balance.delete_one({'cid': cus['cid']})
        db.deposit.delete_many({'cid': cus['cid']})
        db.withdraw.delete_many({'cid': cus['cid']})
        db.charge.delete_many({'cid': cus['cid']})
        return CUSTOMER_REMOVAL_SUCCESS_MSG
    except:
        return CUSTOMER_NOT_REMOVED_ERR

if __name__ == '__main__':
    import sys
    username = input('Enter customer''s username: ')
    print()
    print(delete_customer(username))