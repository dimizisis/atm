
import zmq
import threading
from abc import ABCMeta, abstractmethod

class IterativeServer:

    def __init__(self, ip='localhost', port=1234, protocol=None):
        self.host = ip
        self.protocol = protocol
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(f'tcp://*:{self.port}')

    def listen(self):

        print(f'server is listening on {self.host} {self.port}')

        # A forever loop until we interrupt it
        while True:

            try:
                #  Wait for next request from client
                message = self.socket.recv_string()
                print('Received request ', message)
                    
                # Protocol, in order to generate the output
                out_msg = self.protocol.process_request(message)

                # Send output to client
                self.socket.send_string(out_msg)

            except:
                print('Client disconnected')
                exit(1)

class ServerProtocol:
    __metaclass__ = ABCMeta