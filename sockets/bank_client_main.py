
from SocketLib.client import Client
import sys
from bank_client_protocol import BankClientProtocol

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
