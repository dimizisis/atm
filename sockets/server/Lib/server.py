
import socket
import threading
from abc import ABCMeta, abstractmethod

class IterativeServer:

    def __init__(self, ip='', port=1234, protocol=None):
        self.protocol = protocol
        self.ip = ip
        self.port = port
        self.connection_socket = socket.socket()
        self.connection_socket.bind((self.ip, self.port))    # localhost

    def listen(self):

        # Put the socket into listening mode
        self.connection_socket.listen(5)
        print('Server is listening to port ', self.port)

        # A forever loop until we interrupt it
        while True:

            try:
                # Establish connection with client.
                conn, address = self.connection_socket.accept()
                print('Received request from ', address)

                # Get client's message
                input_msg = conn.recv(1024)

                # Get client's message in right format
                input_msg = input_msg.decode('UTF-8')  # convert to string
                input_msg = input_msg.replace('\n', '')  # remove newline character

                # Protocol, in order to generate the output
                out_msg = self.protocol.process_request(input_msg)

                # Send output to client
                conn.send(out_msg.encode())

                # Close the connection with the client
                conn.close()
            except:
                print('Client disconnected')
                exit(1)

class Server:

    def __init__(self, port=1234, protocol=None):
        self.protocol = protocol
        self.port = port
        self.connection_socket = socket.socket()
        self.connection_socket.bind(('', self.port))    # localhost

    def listen(self):

        # Put the socket into listening mode
        self.connection_socket.listen(5)
        print('Server is listening to port ', self.port)

        try:

            # Establish connection with client
            conn, address = self.connection_socket.accept()
            print('Received request from ', address)

            # Get client's message
            input_msg = conn.recv(1024)

            # Get client's message in right format
            input_msg = input_msg.decode('UTF-8')  # convert to string
            input_msg = input_msg.replace('\n', '')  # remove newline character

            # Protocol, in order to generate the output
            out_msg = self.protocol.process_request(input_msg)

            # Send output to client
            conn.send(out_msg.encode())

            # Close the connection with the client
            conn.close()
        except:
            print('Client disconnected')
            exit(1)

class MultiThreadedServer:

    def __init__(self, ip='', port=1234, protocol=None):
        self.protocol = protocol
        self.port = port
        self.connection_socket = socket.socket()
        self.connection_socket.bind((ip, self.port))    # localhost

    def listen(self):

        # Put the socket into listening mode
        self.connection_socket.listen(5)
        print('Server is listening to port ', self.port)

        while True:

            # Establish connection with client
            conn, address = self.connection_socket.accept()
            print('Received request from ', address)

            # Start thread (each connection == new thread)
            threading.Thread(target=self.server_thread, args=(conn, address)).start()

    def server_thread(self, conn, address):
        while True:
            try:
                # Get client's message
                input_msg = conn.recv(1024)

                # Get client's message in right format
                input_msg = input_msg.decode('UTF-8')  # convert to string
                input_msg = input_msg.replace('\n', '')  # remove newline character

                # Protocol, in order to generate the output
                out_msg = self.protocol.process_request(input_msg)

                # Send output to client
                conn.send(out_msg.encode())

                # Close the connection with the client
                conn.close()
            except:
                print('Client disconnected')
                exit(1)

class ServerProtocol:
    __metaclass__ = ABCMeta

    @abstractmethod
    def process_request(self, input_msg): raise NotImplementedError
