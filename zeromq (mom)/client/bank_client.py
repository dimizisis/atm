import zmq

URI = 'tcp://localhost:8000'

class BankClient:
    def __init__(self, action, username, pin, amount=None, new_pin=None):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(URI)
        self.action = action
        self.username = username
        self.pin = pin
        self.amount = amount
        self.new_pin = new_pin
        self.cid = None

    def make_request(self):
        request = self.prepare_request()
        print("Sending request %s …" % request)
        self.socket.send_string(request)
        response = self.socket.recv_string()
        print(response)
        return response

    def prepare_request(self):
        '''
        Given all the parameters from client,
        creates the proper string and returns it
        '''
        return self.username + ' ' + self.pin + ' ' + self.action + (' ' + self.amount if self.amount is not None else '') + (self.new_pin if self.new_pin is not None else '')
