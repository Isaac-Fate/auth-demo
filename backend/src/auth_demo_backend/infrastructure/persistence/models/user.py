import datetime as dt
from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .sqlalchemy_base_model import SQLAlchemyBaseModel
from .utils import utcnow


class UserInDB(SQLAlchemyBaseModel):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    display_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(index=True, unique=True)
    hashed_password: Mapped[Optional[str]] = mapped_column()
    avatar_url: Mapped[Optional[str]] = mapped_column()
    created_at: Mapped[dt.datetime] = mapped_column(default=utcnow())
