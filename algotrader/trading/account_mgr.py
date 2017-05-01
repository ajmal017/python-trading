from algotrader import SimpleManager

from algotrader.provider.persistence import PersistenceMode
from algotrader.trading.account import Account
from algotrader.trading.context import ApplicationContext


class AccountManager(SimpleManager):
    def __init__(self):
        super(AccountManager, self).__init__()

    def _start(self, app_context : ApplicationContext, **kwargs):
        self.store = self.app_context.get_trade_data_store()
        self.persist_mode = self.app_context.app_config.get("Application", "persistenceMode")
        self.load_all()

    def load_all(self):
        if hasattr(self, "store") and self.store:
            self.store.start(self.app_context)
            accounts = self.store.load_all('accounts')
            for account in accounts:
                self.add(account)

    def save_all(self):
        if hasattr(self, "store") and self.store and self.persist_mode != PersistenceMode.Disable:
            for account in self.all_items():
                self.store.save_account(account)

    def add(self, account):
        super(AccountManager, self).add(account)
        if hasattr(self, "store") and self.store and self.persist_mode == PersistenceMode.RealTime:
            self.store.save_account(account)

    def id(self):
        return "AccountManager"

    def new_account(self, name, values=None):
        if not values:
            values = {}
        account = Account(name, values=values)
        self.add(account)
        return account
