import datetime as dt
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from auth_demo_backend.domain.value_objects import AccountProvider
from .sqlalchemy_base_model import SQLAlchemyBaseModel
from .utils import utcnow


class AccountInDB(SQLAlchemyBaseModel):

    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    provider: Mapped[AccountProvider] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    created_at: Mapped[dt.datetime] = mapped_column(
        default=utcnow(),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
