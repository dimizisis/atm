
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flask_pymongo import PyMongo
from flask_restful import Resource, Api, abort, reqparse
from datetime import datetime
import os
import configparser
import helper_functions
from config_functions import get_database_config

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

app.config['MONGO_URI'], app.config['MONGO_DBNAME'] = get_database_config()

app.url_map.strict_slashes = False # Disable redirecting on POST method from /star to /star/

mongo = PyMongo(app)

@auth.verify_password
def verify(username, pin):
    '''
    Checks customer's credentials\n
    Takes customer's entered username, pin as arguments\n
    If username & pin match, returns True\n
    If username & pin do not match, returns False
    '''
    if not (username and pin):
        return False
    customer = helper_functions.find_customer(username)
    if customer is not None:
        r_pin = customer['pin']    # Get pin from database
        return r_pin == int(pin)
    return False

class Balance(Resource):
    @auth.login_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cid', type=int)
        cid = parser.parse_args()['cid']
        balance_amount, last_updated = helper_functions.get_customer_balance(cid)
        return {'balance' : format(balance_amount, '.3f'), 'last_updated': last_updated}

class Withdrawal(Resource):
    @auth.login_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cid', type=int)
        parser.add_argument('amount', type=float)
        cid = parser.parse_args()['cid']
        amount = parser.parse_args()['amount']
        curr_balance = helper_functions.withdraw(cid, amount)
        return {'amount_withdrawn':amount, 'balance' : format(curr_balance, '.3f')}

class Deposit(Resource):
    @auth.login_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cid', type=int)
        parser.add_argument('amount', type=float)
        cid = parser.parse_args()['cid']
        amount = parser.parse_args()['amount']
        curr_balance = helper_functions.deposit(cid, amount)
        return {'amount_deposited':amount, 'balance' : format(curr_balance, '.3f')}

class PinChange(Resource):
    @auth.login_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cid', type=int)
        parser.add_argument('new_pin', type=int)
        cid = parser.parse_args()['cid']
        new_pin = parser.parse_args()['new_pin']
        success = helper_functions.change_customer_pin(cid, new_pin)
        return {'success':success}

api.add_resource(Withdrawal, '/withdraw', endpoint='withdraw')
api.add_resource(Deposit, '/deposit', endpoint='deposit')
api.add_resource(Balance, '/balance', endpoint='balance')
api.add_resource(PinChange, '/change-pin', endpoint='change-pin')

if __name__ == '__main__':
    app.run(debug=True)
