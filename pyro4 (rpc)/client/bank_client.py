import numbers

class BankClient():

    def __init__(self, server):
        self.server = server

    def authenticate(self, username, pin):
        return_val = self.server.authenticate(username, pin)
        if isinstance(return_val, numbers.Integral): return return_val, True
        return return_val, False

    def make_request(self, username, pin, action, amount=None, new_pin=None):

        return_val, success = self.authenticate(username, pin)

        if not success:
            print(return_val)
            return return_val

        cid = return_val
        
        if action == 'WITHDRAW':
            response = self.server.withdraw(cid, amount) 
        elif action == 'DEPOSIT':
            response = self.server.deposit(cid, amount) 
        elif action == 'CHANGE_PIN':
            response = self.server.change_customer_pin(cid, new_pin)
        elif action == 'GET_BALANCE':
            response = self.server.get_customer_balance(cid)

        return response
