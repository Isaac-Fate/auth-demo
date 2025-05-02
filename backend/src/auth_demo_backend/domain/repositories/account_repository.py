from typing import Protocol, Optional
from abc import abstractmethod

from ..entities import Account
from ..value_objects import AccountProvider


class IAccountRepository(Protocol):

    @abstractmethod
    def add_account(self, account: Account) -> None:
        pass

    @abstractmethod
    def find_accounts_by_user_id(self, user_id: int) -> list[Account]:
        pass

    @abstractmethod
    def find_account_by_user_id_and_provider(
        self,
        provider: AccountProvider,
        user_id: int,
    ) -> Optional[Account]:
        pass
