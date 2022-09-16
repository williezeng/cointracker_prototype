import abc

class WalletInterface(object):
    # TODO: Implement CACHING
    # Everything must be connected via INTERFACE
    def __init__(self, userid, synch=False):
        if not synch:
            assert userid is not None, "There must be a userid"
        self._userid = userid

    @property
    def user_id(self):
        return self._userid

    @abc.abstractmethod
    def get_transactions(self, btc_address):
        pass

    @abc.abstractmethod
    def get_balance(self, btc_address):
        pass

    @abc.abstractmethod
    def remove_address_from_both_databases(self, btc_address):
        pass

    @abc.abstractmethod
    def add_address(self, btc_address):
        pass
