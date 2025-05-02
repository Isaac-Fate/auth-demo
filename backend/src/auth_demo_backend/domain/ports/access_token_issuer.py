from typing import Protocol
from abc import abstractmethod

from ..entities import User


class IAccessTokenIssuer(Protocol):

    @abstractmethod
    def issue_access_token(self, user: User) -> str:
        pass

    @abstractmethod
    def verify_access_token(self, access_token: str) -> User:
        pass
