
import thrift_gen.OperationService as OperationService
from thrift_gen.ttypes import Request

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

URI = 'localhost'
PORT = 8000

class BankClient:

    def __init__(self, username, pin, action, amount=None, new_pin=None):
        self.req = None # the request structure that will eventually send
        self.username = username
        self.pin = pin
        self.action = action
        self.amount = amount
        self.new_pin = new_pin
        self.cid = None
        
        self.transport = TSocket.TSocket(URI, PORT) # Make socket      
        self.transport = TTransport.TBufferedTransport(self.transport)   # Buffering is critical    
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)  # Wrap in a protocol    
        self.client = OperationService.Client(self.protocol) # Create a client to use the protocol encoder       
        self.transport.open()   # Connect!
    
    def prepare_request(self):
        '''
        Given all the parameters from client,
        creates the proper request structure and returns it
        '''
        self.req = Request()
        self.req.username = self.username
        self.req.pin = self.pin
        self.req.amount = self.amount
        self.req.new_pin = self.new_pin

    def make_request(self):

        self.prepare_request()

        if self.action == 'WITHDRAW':
            response = self.client.withdraw(request=self.req)
        elif self.action == 'DEPOSIT':
            response = self.client.deposit(request=self.req) 
        elif self.action == 'CHANGE_PIN':
            response = self.client.change_pin(request=self.req)
        elif self.action == 'GET_BALANCE':
            response = self.client.get_balance(request=self.req)

        self.transport.close()   # Close!
        return response
