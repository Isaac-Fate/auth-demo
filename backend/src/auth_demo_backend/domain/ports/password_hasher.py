from typing import Protocol
from abc import abstractmethod


class IPasswordHasher(Protocol):

    @abstractmethod
    def hash(self, password: str) -> str:
        pass

    @abstractmethod
    def verify(self, password: str, hashed_password: str) -> bool:
        pass
