import datetime as dt
from uuid import uuid4
from sqlalchemy import Column, ForeignKey, UUID, String, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


from auth_demo_backend.models import AccountProvider

SQLAlchemyBaseModel = declarative_base()
"""Base class for SQLAlchemy database models."""


def utcnow():
    return dt.datetime.now(dt.timezone.utc)


class UserInDB(SQLAlchemyBaseModel):

    __tablename__ = "users"

    id = Column(UUID, primary_key=True, default=uuid4)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    display_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=utcnow)

    accounts = relationship("AccountInDB", back_populates="user")


class AccountInDB(SQLAlchemyBaseModel):

    __tablename__ = "accounts"

    id = Column(UUID, primary_key=True, default=uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    account_provider = Column(
        Enum(AccountProvider),
        nullable=False,
    )
    created_at = Column(DateTime, default=utcnow)

    user = relationship("UserInDB", back_populates="accounts")
