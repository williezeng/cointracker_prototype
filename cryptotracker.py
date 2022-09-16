import argparse
import requests
import constants
import pprint

def build_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--userid', required=True, dest='userid', default=None, help="The User's ID")
    parser.add_argument('--btc_address', required=True, dest='btc_address', default=None, help="The bitcoin address")
    parser.add_argument('--delete', action='store_true', dest='delete', default=False,  help="delete the bitcoin address")
    parser.add_argument('--add',action='store_true', dest='add', default=False, help="start tracking the btc_address")
    parser.add_argument('--show_balance', action='store_true', dest='show_balance', default=False, help="show full balance")
    parser.add_argument('--show_transactions', action='store_true', dest='show_transactions', default=False, help="Show all transactions")
    parser.add_argument('--synch', action='store_true', dest='synch', default=False, help="refresh transactions and wallet")

    return parser

def show_balance(user_id, btc_address):
    balance_url = 'http://{address}:{port}/balance'.format(address=constants.HTTP_ADDRESS, port=constants.HTTP_PORT)

    response = requests.post(balance_url, json=dict(userid=user_id, btc_address=btc_address),
                             timeout=constants.HTTP_TIMEOUT)
    print(response.json())

def show_transactions(user_id, btc_address):
    transactions_url = 'http://{address}:{port}/transactions'.format(address=constants.HTTP_ADDRESS, port=constants.HTTP_PORT)

    response = requests.post(transactions_url, json=dict(userid=user_id, btc_address=btc_address),
                             timeout=constants.HTTP_TIMEOUT)
    if response.json():
        i = 5
        pprint.pprint(response.json()['transactions'][:i])
        while i < len(response.json()['transactions']):
            if input("continue?") in ('yes', 'y'):
                pprint.pprint(response.json()['transactions'][i:i+5])
                i += 5
            else:
                exit()

def add_address(user_id, btc_address):
    add_url = 'http://{address}:{port}/add'.format(address=constants.HTTP_ADDRESS, port=constants.HTTP_PORT)

    response = requests.post(add_url, json=dict(userid=user_id, btc_address=btc_address),
                             timeout=constants.HTTP_TIMEOUT)

def delete_address(user_id, btc_address):
    delete_url = 'http://{address}:{port}/delete'.format(address=constants.HTTP_ADDRESS, port=constants.HTTP_PORT)

    response = requests.post(delete_url, json=dict(userid=user_id, btc_address=btc_address),
                             timeout=constants.HTTP_TIMEOUT)

def synch_address(user_id, btc_address):
    synch_url = 'http://{address}:{port}/synch'.format(address=constants.HTTP_ADDRESS, port=constants.HTTP_PORT)

    response = requests.post(synch_url, json=dict(userid=user_id, btc_address=btc_address),
                             timeout=constants.HTTP_TIMEOUT)

if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()
    if args.show_balance:
        show_balance(args.userid, args.btc_address)
    if args.show_transactions:
        show_transactions(args.userid, args.btc_address)
    if args.add:
        add_address(args.userid, args.btc_address)
        synch_address(args.userid, args.btc_address)
    if args.delete:
        delete_address(args.userid, args.btc_address)
    if args.synch:
        synch_address(args.userid, args.btc_address)
    if not any((args.delete, args.add, args.show_balance, args.show_transactions, args.synch)):
        print('you need to specify an action (add, delete, show balance, show transactions)')

