from typing import Optional
from uuid import UUID, uuid4
import datetime as dt
from pydantic import Field, EmailStr

from .configured_base_model import ConfiguredBaseModel


class User(ConfiguredBaseModel):

    id: Optional[UUID] = Field(
        default_factory=uuid4,
    )
    display_name: str
    email: EmailStr
    hashed_password: Optional[str]
    created_at: dt.datetime


class UserCreate(ConfiguredBaseModel):

    display_name: str
    email: EmailStr
    password: str


class UserInfo(ConfiguredBaseModel):

    display_name: str
    email: EmailStr
