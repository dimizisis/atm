import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:8000")

request = "dimizisis 7525 DEPOSIT 20"
print("Sending request %s …" % request)
socket.send_string(request)

#  Get the reply.
message = socket.recv_string()
print("Received reply %s" % message)