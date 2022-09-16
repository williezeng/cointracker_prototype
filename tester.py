from wallet_controller import WalletController

import unittest

blockchain_address = 'https://blockchain.info/rawaddr/'


class TestWallet(unittest.TestCase):
    def test_get_balance(self):
        return
        # TODO: we need to implement the interface correctly
        # we need to inject multiple dictionaries into our methods


wallet_obj = WalletController(userid='Willie')
parsed_output = wallet_obj.format_wallet_data(blockchain_address + 'bc1q0sg9rdst255gtldsmcf8rk0764avqy2h2ksqs5')
# len(parsed_output) == 2
print(parsed_output)

