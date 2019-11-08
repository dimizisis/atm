import numbers

class BankClient():

    def __init__(self, server, username, pin, action, amount=None, new_pin=None):
        self.server = server
        self.username = username
        self.pin = pin
        self.action = action
        self.amount = amount
        self.cid = None
        self.new_pin = new_pin

    def authenticate(self):
        return_val = self.server.authenticate(self.username, self.pin)
        if isinstance(return_val, numbers.Integral):
            self.cid = return_val
            return return_val, True
        return return_val, False

    def make_request(self):

        return_val, success = self.authenticate()

        if not success:
            print(return_val)
            exit(1)
        
        if self.action == 'WITHDRAW':
            response = self.server.withdraw(self.cid, self.amount) 
        elif self.action == 'DEPOSIT':
            response = self.server.deposit(self.cid, self.amount) 
        elif self.action == 'CHANGE_PIN':
            response = self.server.change_customer_pin(self.cid, self.new_pin)
        elif self.action == 'GET_BALANCE':
            response = self.server.get_customer_balance(self.cid)

        return response
