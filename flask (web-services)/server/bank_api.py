
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_restful import Resource, Api, reqparse, abort
from datetime import datetime
import os
import configparser
import helper_functions
from config_functions import get_database_config
from return_messages import *

app = Flask(__name__)
api = Api(app)

app.config['MONGO_URI'], app.config['MONGO_DBNAME'] = get_database_config()

app.url_map.strict_slashes = False # Disable redirecting on POST method from /star to /star/

mongo = PyMongo(app)

class Balance(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str)
            parser.add_argument('pin', type=int)
            username = parser.parse_args()['username']
            pin = parser.parse_args()['pin']
            customer = helper_functions.find_customer(username)
            if pin == customer['pin']:
                balance_amount, last_updated = helper_functions.get_customer_balance(customer['cid'])
                return {'balance' : format(balance_amount, '.3f'), 'last_updated': last_updated}
            else:
                abort(422, error_message=WRONG_CREDENTIALS)
        except Exception as e:
            print(e)
            abort(404, error_message=BALANCE_NOT_FOUND_ERR)

class Withdrawal(Resource):
    def put(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str)
            parser.add_argument('pin', type=int)
            parser.add_argument('amount', type=int)
            username = parser.parse_args()['username']
            pin = parser.parse_args()['pin']
            amount = parser.parse_args()['amount']
            customer = helper_functions.find_customer(username)
            if pin == customer['pin']:
                curr_balance = helper_functions.withdraw(customer['cid'], amount)
                return {'amount_withdrawn':amount, 'balance' : format(curr_balance, '.3f'), 'message': WITHDRAWAL_SUCCESS_MSG}
            else:
                abort(422, error_message=WRONG_CREDENTIALS)
        except Exception as e:
            print(e)
            abort(404, error_message=WITHDRAWAL_FAILURE_ERR)

class Deposit(Resource):
    def put(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str)
            parser.add_argument('pin', type=int)
            parser.add_argument('amount', type=int)
            username = parser.parse_args()['username']
            pin = parser.parse_args()['pin']
            amount = parser.parse_args()['amount']
            customer = helper_functions.find_customer(username)
            if pin == customer['pin']:
                curr_balance = helper_functions.deposit(customer['cid'], amount)
                return {'amount_deposited':amount, 'balance' : format(curr_balance, '.3f'), 'message': DEPOSITION_SUCCESS_MSG}
            else:
                abort(422, error_message=WRONG_CREDENTIALS)
        except Exception as e:
            print(e)
            abort(404, error_message=DEPOSITION_FAILURE_ERR)

class PinChange(Resource):
    def put(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str)
            parser.add_argument('pin', type=int)
            parser.add_argument('new_pin', type=int)
            username = parser.parse_args()['username']
            pin = parser.parse_args()['pin']
            new_pin = parser.parse_args()['new_pin']
            customer = helper_functions.find_customer(username)
            if pin == customer['pin']:
                success = helper_functions.change_customer_pin(customer['cid'], new_pin)
                return {'message':CUSTOMER_PIN_CHANGE_SUCCESS_MSG}
            else:
                abort(422, error_message=WRONG_CREDENTIALS)
        except Exception as e:
            print(e)
            abort(404, error_message=CUSTOMER_PIN_CHANGE_FAILURE_ERR)

api.add_resource(Withdrawal, '/withdraw', endpoint='withdraw')
api.add_resource(Deposit, '/deposit', endpoint='deposit')
api.add_resource(Balance, '/balance', endpoint='balance')
api.add_resource(PinChange, '/change-pin', endpoint='change-pin')

if __name__ == '__main__':
    app.run()
