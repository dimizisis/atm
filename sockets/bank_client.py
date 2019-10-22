from Lib.client import Client, ClientProtocol
import random
import sys

class BankClientProtocol(ClientProtocol):

    def __init__(self, username, pin, action, amount=None):
        self.username = username
        self.action = action
        self.pin = pin
        self.amount = amount

    def prepare_request(self):
        
        if action == 'WITHDRAW':
            output = self.username + ' ' + str(self.pin) + ' ' + action + ' ' + str(20)
        elif action == 'DEPOSIT':
            output = self.username + ' ' + str(self.pin) + ' ' + action + ' ' + str(20)
        elif action == 'CHANGE_PIN':
            output = self.username + ' ' + str(self.pin) + ' ' + action + ' ' + str(1405)
        elif action == 'GET_BALANCE':
            output = self.username + ' ' + str(self.pin) + ' ' + action

        return output

    def process_reply(self, input_msg):
        print('Response: ', input_msg)

if __name__ == '__main__':

    username = sys.argv[1]
    pin = int(sys.argv[2])
    action = sys.argv[3]
    if len(sys.argv) == 5:
        amount = float(sys.argv[4])
    else:
        amount = None

    protocol = BankClientProtocol(username, pin, action, amount)
    bank_client = Client(protocol=protocol)
    bank_client.open()
