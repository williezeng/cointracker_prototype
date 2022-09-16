import urllib.error
import urllib.request

from pymongo import MongoClient, InsertOne

from json import loads
import time

from wallet_interface import WalletInterface
blockchain_address = 'https://blockchain.info/rawaddr/'

# TODO: SETUP logging for almost every method
class WalletController(WalletInterface):
    def __init__(self, userid, synch=False):
        WalletInterface.__init__(self, userid, synch)
        self.client = MongoClient("mongodb+srv://tester:tester123@cluster0.azcwewo.mongodb.net/?retryWrites=true&w=majority")

    def get_userid_wallet_collection_from_db(self, user_id):
        # database -> user -> multiple wallets
        db = self.client['wallets']
        collection = db[user_id]
        return collection

    def get_all_user_address(self):
        return list(self._get_user_lookup_collection().find({}))

    def _get_user_lookup_collection(self):
        # database -> user -> user:btc_address
        db = self.client['user_lookup']
        collection = db['user_lookup_table']
        return collection

    def get_addresses_for_user(self):
        return [entry['btc_address'] for entry in list(self._get_user_lookup_collection().find({"userid": self.user_id}))]

    def add_address(self, btc_address):
        # Only add btc address if it doesn't already exist
        user_lookup_collection = self._get_user_lookup_collection()
        user_id_and_btc_addr = {"userid": self.user_id, "btc_address": btc_address}
        found_user = list(user_lookup_collection.find(user_id_and_btc_addr))
        if len(found_user) == 0:
            user_lookup_collection.insert_one(user_id_and_btc_addr)

    def remove_address_from_both_databases(self, btc_address):
        # remove if it exists
        self.remove_userid_btc_addr_from_lookup(self._get_user_lookup_collection(), btc_address)
        self.remove_btc_addr_from_wallet(self.get_userid_wallet_collection_from_db(self.user_id), btc_address)

    def remove_userid_btc_addr_from_lookup(self, user_lookup_collection, btc_address):
        user_id_and_btc_addr = {"userid": self.user_id, "btc_address": btc_address}
        found_user = list(user_lookup_collection.find(user_id_and_btc_addr))
        if len(found_user) == 1:
            user_lookup_collection.delete_one(user_id_and_btc_addr)
        elif len(found_user) == 0:
            return
        else:
            raise Exception('There can only be one entry per userid, but we found %s' % len(found_user))

    def remove_btc_addr_from_wallet(self, wallet_collection, btc_address):
        btc_address = {"btc_address": btc_address}
        found_user = list(wallet_collection.find(btc_address))
        if len(found_user) == 1:
            wallet_collection.delete_one(found_user[0])
        elif len(found_user) == 0:
            return
        else:
            raise Exception('There can only be one entry per btc_addr, but we found %s' % len(found_user))

    def _get_wallet_data_from_api(self, full_address):
        # 'hash160', 'address', 'n_tx', 'n_unredeemed', 'total_received', 'total_sent', 'final_balance', 'txs'
        # TODO: possible bottleneck -- memory usage
        try:
            with urllib.request.urlopen(full_address) as f:
                for jsonobj in f:
                    json_data = loads(jsonobj)
        except urllib.error.URLError as e:
            print(e.reason)
            exit()
        return json_data

    def format_wallet_data(self, full_addr):
        wallet_data = self._get_wallet_data_from_api(full_addr)
        parsed_wallet_data = {
            'btc_address': wallet_data['address'],
            'transactions': wallet_data['txs'],
            'final_balance': wallet_data['final_balance']
        }
        return parsed_wallet_data

    def _read_from_db(self, wallet_collection, btc_address):
        #TODO: read wallet -> userid -> btc_address: transactions and balances
        btc_address = {"btc_address": btc_address}
        found_user = list(wallet_collection.find(btc_address))
        if len(found_user) == 1:
            return found_user[0]
        elif len(found_user) == 0:
            return
        else:
            raise Exception('There can only be one entry per btc_addr, but we found %s' % len(found_user))

    def get_transactions(self, btc_address):
        wallet_collection = self.get_userid_wallet_collection_from_db(self.user_id)
        wallet_db = self._read_from_db(wallet_collection, btc_address)
        if wallet_db:
            return {'transactions': wallet_db['transactions']}
        return

    def get_balance(self, btc_address):
        wallet_collection = self.get_userid_wallet_collection_from_db(self.user_id)
        wallet_db = self._read_from_db(wallet_collection, btc_address)
        if wallet_db:
            return {'final_balance': wallet_db['final_balance']}
        return

    def synch_one_user_id(self):
        for addr in self.get_addresses_for_user():
            json_data = self.format_wallet_data(blockchain_address + addr)
            wallet_collection = self.get_userid_wallet_collection_from_db(self.user_id)
            self.remove_btc_addr_from_wallet(wallet_collection, addr)
            wallet_collection.insert_one(json_data)
            time.sleep(12)

    def synch(self):
        for user_and_btc_addr_dict in self.get_all_user_address():
            json_data = self.format_wallet_data(blockchain_address + user_and_btc_addr_dict['btc_address'])
            wallet_collection = self.get_userid_wallet_collection_from_db(user_and_btc_addr_dict['userid'])
            self.remove_btc_addr_from_wallet(wallet_collection, user_and_btc_addr_dict['btc_address'])
            wallet_collection.insert_one(json_data)
            time.sleep(12)
