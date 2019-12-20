import numbers
from return_messages import *

FAILED_TO_CONNECT = 'Failed to connect to the server. Please try again later.'

class BankClient:

    def __init__(self, proxy, action, username, pin, amount=None, new_pin=None):
        self.proxy = proxy
        self.action = action
        self.username = username
        self.pin = pin
        self.amount = amount
        self.new_pin = new_pin
        self.cid = None

    def authenticate(self):
        try:
            return_val = self.proxy.authenticate(self.username, self.pin)
            if isinstance(return_val, numbers.Integral):
                return return_val, True
            return return_val, False
        except Exception as e:
            return FAILED_TO_CONNECT, False

    def make_request(self):

        return_val, success = self.authenticate()

        if not success:
            print(return_val)
            return return_val
        
        self.cid = return_val
        
        if self.action == 'WITHDRAW':
            response = self.proxy.withdraw(self.cid, self.amount) 
        elif self.action == 'DEPOSIT':
            response = self.proxy.deposit(self.cid, self.amount) 
        elif self.action == 'CHANGE_PIN':
            response = self.proxy.change_customer_pin(self.cid, self.new_pin)
        elif self.action == 'GET_BALANCE':
            response = self.proxy.get_customer_balance(self.cid)

        return response
