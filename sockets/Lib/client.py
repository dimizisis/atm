import socket
from abc import ABCMeta, abstractmethod


class Client:

    def __init__(self, host='localhost', port=1234, protocol=None):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.data_socket = socket.socket()
        self.data_socket.connect((self.host, self.port))

    def open(self):

        # Prepare request, according to client's protocol
        out_msg = self.protocol.prepare_request()

        # Send request encoded
        self.data_socket.send(out_msg.encode())

        # Receive message from server
        input_msg = self.data_socket.recv(1024)

        # Get server's message in right format
        input_msg = input_msg.decode('UTF-8')  # convert to string
        input_msg = input_msg.replace('\n', '')  # remove newline character

        # Process reply, according to client's protocol
        self.protocol.process_reply(input_msg)

        # Close the connection with server
        self.data_socket.close()


class ClientProtocol:
    __metaclass__ = ABCMeta

    @abstractmethod
    def prepare_request(self): raise NotImplementedError

    @abstractmethod
    def process_reply(self, input_msg): raise NotImplementedError
