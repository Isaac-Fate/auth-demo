import datetime as dt
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from auth_demo_backend.domain.value_objects import AccountProvider
from .sqlalchemy_base_model import SQLAlchemyBaseModel
from .utils import utcnow


class AccountInDB(SQLAlchemyBaseModel):

    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    provider: Mapped[AccountProvider] = mapped_column()
    email: Mapped[str] = mapped_column(index=True, unique=True)
    avatar_url: Mapped[Optional[str]] = mapped_column()
    created_at: Mapped[dt.datetime] = mapped_column(default=utcnow())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
