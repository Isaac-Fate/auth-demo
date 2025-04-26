from typing import Optional
from uuid import UUID
import datetime as dt
from pydantic import EmailStr

from .configured_base_model import ConfiguredBaseModel


class User(ConfiguredBaseModel):

    id: UUID
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
