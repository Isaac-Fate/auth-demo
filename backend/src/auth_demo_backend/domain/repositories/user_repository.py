from typing import Protocol, Optional
from abc import abstractmethod

from ..entities import User


class IUserRepository(Protocol):

    @abstractmethod
    def add_user(self, user: User) -> None:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def find_user_by_email(self, email: str) -> Optional[User]:
        pass
