
import zmq
import threading
from abc import ABCMeta, abstractmethod

class MultiThreadedServer:

    def __init__(self, ip='', port=1234, protocol=None):
        self.protocol = protocol
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:"+str(port))

    def listen(self):

        while True:
            #  Wait for next request from client
            message = self.socket.recv_string()
            print('Received request ', message)

            # Start thread (each connection == new thread)
            threading.Thread(target=self.server_thread, args=(message,)).start()

    def server_thread(self, input_msg):
        while True:
            try:
                
                # Protocol, in order to generate the output
                out_msg = self.protocol.process_request(input_msg)

                # Send output to client
                self.socket.send_string(out_msg)

                # Close the connection with the client
                self.socket.close()
            except:
                print('Client disconnected')
                exit(1)

class ServerProtocol:
    __metaclass__ = ABCMeta