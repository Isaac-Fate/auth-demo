from typing import Optional, Self
import bcrypt

from .entity import Entity


class User(Entity):

    def __init__(
        self,
        *,
        id: Optional[int] = None,
        display_name: str,
        email: str,
        hashed_password: Optional[str] = None,
        avatar_url: Optional[str] = None,
    ) -> None:

        super().__init__(id)

        self.display_name = display_name
        self.email = email
        self.hashed_password = hashed_password
        self.avatar_url = avatar_url

    @classmethod
    def from_sign_up(cls, display_name: str, email: str, password: str) -> Self:

        return cls(
            display_name=display_name,
            email=email,
            hashed_password=User.hash_password(password),
        )

    def ignore_hashed_password(self) -> Self:

        return User(
            id=self.id,
            display_name=self.display_name,
            email=self.email,
        )

    def change_display_name(self, display_name: str) -> None:

        self.display_name = display_name

    @staticmethod
    def hash_password(password: str) -> str:

        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).hex()

    def check_password(self, password: str) -> bool:

        if self.hashed_password is None:
            raise ValueError("Hashed password is not set in the user")

        return bcrypt.checkpw(
            password.encode("utf-8"),
            bytes.fromhex(self.hashed_password),
        )

    def set_avatar_url(self, avatar_url: str) -> None:

        self.avatar_url = avatar_url
