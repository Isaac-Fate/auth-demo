from typing import Optional

from .entity import Entity
from ..value_objects import AccountProvider


class Account(Entity):

    def __init__(
        self,
        *,
        id: Optional[int] = None,
        email: str,
        provider: AccountProvider,
        avatar_url: Optional[str] = None,
        user_id: Optional[int] = None,
    ) -> None:

        super().__init__(id)

        self.email = email
        self.provider = provider
        self.avatar_url = avatar_url
        self.user_id = user_id

    def link_to_user(self, user_id: int) -> None:

        self.user_id = user_id
