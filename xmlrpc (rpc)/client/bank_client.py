import numbers

FAILED_TO_CONNECT = 'Failed to connect to the server. Please try again later.'

class BankClient():

    def __init__(self, proxy):
        self.proxy = proxy

    def authenticate(self, username, pin):
        return_val = self.proxy.authenticate(username, pin)
        if isinstance(return_val, numbers.Integral):
            return return_val, True
        return return_val, False

    def make_request(self, action, username, pin, amount=None, new_pin=None):

        return_val, success = self.authenticate(username, pin)

        if not success:
            print(return_val)
            return FAILED_TO_CONNECT
        
        cid = return_val
        
        if action == 'WITHDRAW':
            response = self.proxy.withdraw(cid, amount) 
        elif action == 'DEPOSIT':
            response = self.proxy.deposit(cid, amount) 
        elif action == 'CHANGE_PIN':
            response = self.proxy.change_customer_pin(cid, new_pin)
        elif action == 'GET_BALANCE':
            response = self.proxy.get_customer_balance(cid)

        return response
