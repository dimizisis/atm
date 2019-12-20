import asyncio
import websockets
import numbers

FAILED_TO_CONNECT = 'Failed to connect to the server. Please try again later.'
URI = "ws://localhost:8000"   

class BankClient:

    def __init__(self, username, pin, action, amount=None, new_pin=None):
        self.username = username
        self.pin = pin
        self.action = action
        self.amount = amount
        self.new_pin = new_pin

    async def make_request(self):
        request = self.prepare_request()
        async with websockets.connect(URI) as websocket:

            await websocket.send(request)
            print(f"> {request}")

            response = await websocket.recv()
        
        return response

    def prepare_request(self):

        if self.action == 'WITHDRAW' or self.action == 'DEPOSIT':
            output = self.username + ' ' + str(self.pin) + ' ' + self.action + ' ' + str(self.amount)
        elif self.action == 'CHANGE_PIN':
            output = self.username + ' ' + str(self.pin) + ' ' + self.action + ' ' + str(self.new_pin)
        elif self.action == 'GET_BALANCE':
            output = self.username + ' ' + str(self.pin) + ' ' + self.action

        return output
