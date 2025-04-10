from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID, uuid4
import datetime as dt
from functools import partial

from .account_provider import AccountProvider


class User(SQLModel, table=True):

    id: Optional[UUID] = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    display_name: str = Field(nullable=False)
    email: EmailStr = Field(index=True, unique=True)
    hashed_password: Optional[str] = Field(nullable=True)
    created_at: Optional[dt.datetime] = Field(
        default_factory=partial(dt.datetime.now, tz=dt.timezone.utc),
    )

    accounts: list["Account"] = Relationship(back_populates="user")


class UserCreate(BaseModel):

    display_name: str
    email: EmailStr
    password: str


class Account(SQLModel, table=True):

    id: Optional[UUID] = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    user_id: UUID = Field(foreign_key="user.id")
    provider: AccountProvider
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: Optional[int] = None

    user: User = Relationship(back_populates="accounts")
