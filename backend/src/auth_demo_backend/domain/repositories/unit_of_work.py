from typing import Protocol, ContextManager
from abc import abstractmethod

from .user_repository import IUserRepository
from .account_repository import IAccountRepository


class IUnitOfWork(ContextManager, Protocol):

    user_repository: IUserRepository
    account_repository: IAccountRepository

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass
