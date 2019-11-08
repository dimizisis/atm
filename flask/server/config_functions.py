
import os
import configparser

# CONFIGURATION FILENAME
CONFIG_FILENAME = 'config.ini'

def get_database_config():
    '''
    Reads config file, which contains client and database name\n
    Config filename set as constant (config.ini)
    '''
    try:
        config = configparser.ConfigParser()
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        initfile = os.path.join(curr_dir, CONFIG_FILENAME)
        config.read(initfile)
        client = config.get('SETTINGS', 'CLIENT')
        database_name = config.get('SETTINGS', 'DATABASE_NAME')
        return client, database_name
    except Exception as e:
        print(e)

def get_balance_charges():
    '''
    Reads config file, which contains charges amount and charges description\n
    Config filename set as constant (config.ini)
    '''
    try:
        config = configparser.ConfigParser()
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        initfile = os.path.join(curr_dir, CONFIG_FILENAME)
        config.read(initfile)
        charges_amount = config.get('CHARGES', 'BALANCE_INFO_CHARGES')
        charges_descr = config.get('CHARGES', 'BALANCE_INFO_CHARGES_DESCR')
        return charges_amount, charges_descr
    except Exception as e:
        print(e)

def get_withdrawal_limit():
    '''
    Reads config file, which contains charges amount and charges description\n
    Config filename set as constant (config.ini)
    '''
    try:
        config = configparser.ConfigParser()
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        initfile = os.path.join(curr_dir, CONFIG_FILENAME)
        config.read(initfile)
        withdrawal_limit = config.get('LIMITATIONS', 'DAILY_WITHDRAWAL_LIMIT')
        return withdrawal_limit
    except Exception as e:
        print(e)
