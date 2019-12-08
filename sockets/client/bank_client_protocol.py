
from Lib.client import ClientProtocol

class BankClientProtocol(ClientProtocol):

    def __init__(self, username, pin, action, amount=None, new_pin=None):
        self.username = username
        self.pin = pin
        self.action = action
        self.amount = amount
        self.new_pin = new_pin

    def prepare_request(self):
        
        if self.action == 'WITHDRAW' or self.action == 'DEPOSIT':
            output = self.username + ' ' + str(self.pin) + ' ' + self.action + ' ' + str(self.amount)
        elif self.action == 'CHANGE_PIN':
            output = self.username + ' ' + str(self.pin) + ' ' + self.action + ' ' + str(self.new_pin)
        elif self.action == 'GET_BALANCE':
            output = self.username + ' ' + str(self.pin) + ' ' + self.action

        return output

    def process_reply(self, input_msg):
        print('Response: ', input_msg)
        return input_msg
