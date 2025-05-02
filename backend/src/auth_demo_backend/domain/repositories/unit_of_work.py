from typing import Protocol, ContextManager

from .user_repository import IUserRepository
from .account_repository import IAccountRepository


class IUnitOfWork(ContextManager, Protocol):

    user_repository: IUserRepository
    account_repository: IAccountRepository

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass
