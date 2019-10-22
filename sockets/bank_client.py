from Lib.client import Client, ClientProtocol
import random

class BankClientProtocol(ClientProtocol):
   
    # MSGS
    DEPOSITION_SUCCESS_MSG = 'Deposition successful'
    WITHDRAWAL_SUCCESS_MSG = 'Withdrawal successful'
    CUSTOMER_ADDITION_SUCCESS_MSG = 'Successfully added customer'
    CUSTOMER_REMOVAL_SUCCESS_MSG = 'Successfully removed customer'
    CUSTOMER_PIN_CHANGE_SUCCESS_MSG = 'Successfully changed pin'

    # ERRORS
    CUSTOMER_DOES_NOT_EXIST_ERR = 'Customer does not exist'
    AMOUNT_NOT_VALID_ERR = 'Not a valid amount'
    CUSTOMER_NOT_ADDED_ERR = 'Customer cannot be added to database'
    CUSTOMER_NOT_REMOVED_ERR = 'Customer cannot be removed from database'
    BALANCE_NOT_INIT_ERR = 'Balance not initialized'
    BALANCE_NOT_FOUND_ERR = 'Balance not found'
    BALANCE_NOT_ENOUGH_ERR = 'Balance not enough to withdraw'
    BANKNOTES_NOT_VALID_ERR = 'Try another amount (banknotes: 20€, 50€)'
    DEPOSITION_FAILURE_ERR = 'Deposition failed'
    WITHDRAWAL_FAILURE_ERR = 'Withdrawal failed'
    CUSTOMER_PIN_CHANGE_FAILURE_ERR = 'Cannot change ping'
    USERNAME_TAKEN_ERR = 'Sorry, username already taken'

    username = 'zdimitris'
    pin = 3473

    def prepare_request(self):

        actions = ['WITHDRAW', 'DEPOSIT', 'CHANGE_PIN', 'GET_BALANCE']

        action = 'DEPOSIT'
        
        if action == 'WITHDRAW':
            output = self.username + ' ' + str(self.pin) + ' ' + action + ' ' + str(20)
        elif action == 'DEPOSIT':
            output = self.username + ' ' + str(self.pin) + ' ' + action + ' ' + str(20)
        elif action == 'CHANGE_PIN':
            output = self.username + ' ' + str(self.pin) + ' ' + action + ' ' + str(1405)
        elif action == 'GET_BALANCE':
            output = self.username + ' ' + str(self.pin) + ' ' + action

        return output

    def process_reply(self, input_msg):
        print('Response: ', input_msg)

if __name__ == '__main__':

    protocol = BankClientProtocol()
    bank_client = Client(protocol=protocol)
    bank_client.open()
