from auth_demo_backend.domain.entities import Account
from .mapper import IMapper
from ..models import AccountInDB


class AccountMapper(IMapper):

    @staticmethod
    def to_domain_model(account_in_db: AccountInDB) -> Account:

        account = Account(
            id=account_in_db.id,
            provider=account_in_db.provider,
            email=account_in_db.email,
        )

        return account

    @staticmethod
    def to_db_model(account: Account) -> AccountInDB:

        account_in_db = AccountInDB(
            provider=account.provider,
            email=account.email,
        )

        if account.is_id_set():
            account_in_db.id = account.id

        return account_in_db
