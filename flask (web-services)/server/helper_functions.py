
import bank_api
from datetime import datetime
from flask_restful import abort
from math import log10
import configparser
import os
import return_messages
from config_functions import get_balance_charges, get_withdrawal_limit

# CONFIGURATION FILENAME
CONFIG_FILENAME = 'config.ini'

# CHARGES AMOUNT & CHARGE_DESCR
BALANCE_INFO_CHARGES, BALANCE_INFO_CHARGES_DESCR = get_balance_charges()

# DAILY WITHDRAWAL LIMIT
DAILY_WITHDRAWL_LIMIT = get_withdrawal_limit()

def find_customer(username):
    '''
    Checks if customer's username exists in customers' collection\n
    Takes username as argument\n
    Returns cid (customer's id) if customer exists\n
    Returns None if he doesn't
    '''
    customer = bank_api.mongo.db.customer.find_one({'username': username})
    if customer is not None:
        return customer
    return None

def get_customer_balance(cid):
    '''
    Informs customer about his balance\n
    Takes cid (customer id) as argument\n
    Returns balance amount (double) & last_updated str if found\n
    Returns None if not found
    '''
    try:
        charge(cid, BALANCE_INFO_CHARGES, BALANCE_INFO_CHARGES_DESCR)
        balance = bank_api.mongo.db.balance.find_one({'cid': cid}, {'balance': 1, 'last_updated': 1})
        return balance['balance'], balance['last_updated']
    except:
        print('BALANCE_NOT_FOUND_ERR')
        abort(404, message=BALANCE_NOT_FOUND_ERR)
        
    return None, None

def charge(cid, amount, descr):
    '''
    Charges customer when is asking about balance information\n
    Takes cid (customer id), charge amount and charge description as parameters
    '''
    try:
        balance_doc = {'$inc': {'balance': -amount}, '$set': {'last_updated': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}}
        chid = bank_api.mongo.db.charge.count_documents({})+1
        charge_doc = {'chid': chid, 'cid': cid, 'amount': amount, 'descr': descr, 'date': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}
        bank_api.mongo.db.balance.update_one({'cid': cid}, balance_doc)
        bank_api.mongo.db.charge.insert_one(charge_doc)
        print('Customer charged')
    except Exception as e:
        print(e)

def withdraw(cid, amount):
    '''
    Customer withdraws from his account\n
    Takes cid and amount as arguements\n
    Returns True if withdrawal successful\n
    Returns False if withdrawal unsuccessful
    '''

    if amount <= 0:
        print('AMOUNT_NOT_VALID_ERR')
        abort(403, message=AMOUNT_NOT_VALID_ERR)

    if bank_api.mongo.db.balance.find_one({'cid': cid}, {'balance': 1})['balance'] < amount:
        print('BALANCE_NOT_ENOUGH_ERR')
        abort(403, message=BALANCE_NOT_ENOUGH_ERR)
        
    if not check_banknotes(amount):
        print('BANKNOTES_NOT_VALID_ERR')
        abort(403, message=BANKNOTES_NOT_VALID_ERR)

    if daily_withdrawal_limit_reached(cid, amount):
        print('DAILY_WITHDRAWAL_LIMIT_ERR')
        abort(403, message=DAILY_WITHDRAWAL_LIMIT_ERR)

    try:
        withdrawal_doc = {'wid': bank_api.mongo.db.withdraw.count_documents({})+1, 'amount': amount, 'cid': cid, 'time': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}
        balance_doc = {'$inc': {'balance': -float(amount)}, '$set': {'last_updated': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}}
        bank_api.mongo.db.withdraw.insert_one(withdrawal_doc)
        bank_api.mongo.db.balance.update_one({'cid': cid}, balance_doc)
        print('WITHDRAWAL_SUCCESS_MSG')
        curr_balance = bank_api.mongo.db.balance.find_one({'cid': cid}, {'balance': 1})['balance']
        return curr_balance
    except:
        print('WITHDRAWAL_FAILURE_ERR')
        abort(400, message=WITHDRAWAL_FAILURE_ERR)

def daily_withdrawal_limit_reached(cid, amount):
    '''
    Checks if customer reached his daily withdrawal limit (Set as constant 850)\n
    Takes cid as parameter\n
    Returns True if limit reached\n
    Returns False if limit is not reached
    '''
    if amount > DAILY_WITHDRAWL_LIMIT:
        return True
    curr_date = datetime.today().strftime('%Y-%m-%d')
    pipe = [{ "$match": { 'cid': { "$eq": cid } } }, { "$match": { 'time': { "$regex": '.*'+curr_date+'.*' } } }, {'$group': {'_id': "$cid", 'total_amount': {'$sum': '$amount'}}}]
    results = list(bank_api.mongo.db.withdraw.aggregate(pipeline=pipe)) # we get a list with one dict inside (cid and amount that was withdrawn today)
    if results:
        total_amount_withdrawn = results[0]['total_amount'] 
        if total_amount_withdrawn > DAILY_WITHDRAWL_LIMIT:
            return True
    return False

def check_banknotes(amount):
    '''
    Checks if amount is divided by 20 or 50 or 70\n
    Returns True if it is\n
    Returns False if not
    '''
    return (amount % 20 == 0 or amount % 50 == 0 or amount % 70 == 0)
        
def deposit(cid, amount):
    '''
    Customer deposits into his account\n
    Takes cid and amount as arguements\n
    Returns True if deposition successful\n
    Returns False if deposition unsuccessful
    '''
        
    if amount <= 0:
        print('AMOUNT_NOT_VALID_ERR')
        abort(403, message=AMOUNT_NOT_VALID_ERR)

    try:
        deposition_doc = {'did': bank_api.mongo.db.deposit.count_documents({})+1, 'amount': amount, 'cid': cid, 'time': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}
        balance_doc = {'$inc': {'balance': float(amount)}, '$set': {'last_updated': datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}}
        bank_api.mongo.db.deposit.insert_one(deposition_doc)
        bank_api.mongo.db.balance.update_one({'cid': cid}, balance_doc)
        curr_balance = bank_api.mongo.db.balance.find_one({'cid': cid}, {'balance':1})['balance']
        print('DEPOSITION_SUCCESS_MSG')
        return curr_balance
    except:
        print('DEPOSITION_FAILURE_ERR')
        abort(400, message=DEPOSITION_FAILURE_ERR)

def change_customer_pin(cid, new_pin):
    '''
    Changes customer's pin (based on id)\n
    with another random one
    '''
    if int(log10(new_pin))+1 == 4:
        try:
            bank_api.mongo.db.customer.update_one({'cid': cid}, {'$set': {'pin': new_pin}})
            print('CUSTOMER_PIN_CHANGE_SUCCESS_MSG')
            return True
        except:
            print('CUSTOMER_PIN_CHANGE_FAILURE_ERR')
            return False
    return False
