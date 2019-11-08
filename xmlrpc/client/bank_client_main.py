
import xmlrpc.client
import numbers
import sys
from bank_client import BankClient

SERVER_PROXY = "http://localhost:8000/"

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

    proxy = xmlrpc.client.ServerProxy(SERVER_PROXY)

    client = BankClient(proxy, username, pin, action, amount, new_pin)

    response = client.make_request()

    print(response)
