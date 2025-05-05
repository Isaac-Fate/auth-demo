from typing import Protocol, Optional
from abc import abstractmethod

from ..entities import User


class IOAuthClient(Protocol):

    @abstractmethod
    async def create_authorization_url(
        self,
        redirect_uri: str,
        prompt: Optional[str] = None,
        **kwargs,
    ) -> str:
        pass

    @abstractmethod
    async def get_user_with_account(
        self,
        redirect_uri: str,
        code: str,
        state: Optional[str] = None,
        **kwargs,
    ) -> User:
        pass
