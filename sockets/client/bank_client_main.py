
from Lib.client import Client
import sys
from bank_client_protocol import BankClientProtocol

if __name__ == '__main__':

    username = sys.argv[1]
    pin = int(sys.argv[2])
    action = sys.argv[3]
    amount = None
    new_pin = None
    if len(sys.argv) == 5 and action == 'CHANGE_PIN':
        new_pin = int(sys.argv[4])
    elif len(sys.argv) == 5:
        amount = float(sys.argv[4])

    protocol = BankClientProtocol(username, pin, action, amount, new_pin)
    bank_client = Client(protocol=protocol)
    bank_client.open()
