
import sys
import requests

IP = 'http://127.0.0.1:5000/'

FAILED_TO_CONNECT = 'Failed to connect to the server. Please try again later.'

class BankClient():

    def make_request(self, action, username, pin, **kwargs):

        if 'amount' in kwargs and kwargs.get('amount') is not None: amount = kwargs.get('amount') 
        elif 'new_pin' in kwargs and kwargs.get('new_pin') is not None: new_pin = kwargs.get('new_pin')

        try:
            if action == 'GET_BALANCE':
                response = requests.get(f'{IP}balance?username={username}&pin={pin}')
                try:
                    response_txt = response.json()['balance']
                except:
                    response_txt = response.json()['error_message']
            elif action == 'CHANGE_PIN':
                response = requests.put(f'{IP}change-pin?username={username}&pin={pin}&new_pin={new_pin}')
                try:
                    response_txt = response.json()['message']
                except:
                    response_txt = response.json()['error_message']
            elif action == 'DEPOSIT':
                response = requests.put(f'{IP}deposit?username={username}&pin={pin}&amount={amount}')
                try:
                    response_txt = response.json()['message']
                except:
                    response_txt = response.json()['error_message']
            elif action == 'WITHDRAW':
                response = requests.put(f'{IP}withdraw?username={username}&pin={pin}&amount={amount}')
                try:
                    response_txt = response.json()['message']
                except:
                    response_txt = response.json()['error_message']
        except Exception as e:
            print(e)
            response_txt = FAILED_TO_CONNECT

        return response_txt
