from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from auth_demo_backend.domain.repositories import IAccountRepository
from auth_demo_backend.domain.entities import Account
from auth_demo_backend.domain.value_objects import AccountProvider
from ..mappers import AccountMapper
from ..models import AccountInDB


class SQLAlchemyAccountRepository(IAccountRepository):

    def __init__(self, db_session: Session):

        self._db_session = db_session

    def add_account(self, account: Account) -> None:

        # Convert to a database model
        account_in_db = AccountMapper.to_db_model(account)

        # Add the account to the database
        self._db_session.add(account_in_db)

        # Flush the changes
        self._db_session.flush()

        # Update account ID
        account.id = account_in_db.id

    def find_accounts_by_user_id(self, user_id: int) -> list[Account]:

        stmt = select(AccountInDB).where(AccountInDB.user_id == user_id)
        accounts_in_db = self._db_session.execute(stmt).scalars().all()

        accounts = [
            AccountMapper.to_domain_model(account_in_db)
            for account_in_db in accounts_in_db
        ]

        return accounts

    def find_account_by_user_id_and_provider(
        self,
        provider: AccountProvider,
        user_id: int,
    ) -> Optional[Account]:

        stmt = select(AccountInDB).where(
            AccountInDB.user_id == user_id,
            AccountInDB.provider == provider,
        )
        account_in_db = self._db_session.execute(stmt).scalar_one_or_none()

        if account_in_db is None:
            return None

        return AccountMapper.to_domain_model(account_in_db)
