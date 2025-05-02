from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from auth_demo_backend.domain.repositories import IUserRepository
from auth_demo_backend.domain.entities import User
from ..models import UserInDB
from ..mappers import UserMapper


class SQLAlchemyUserRepository(IUserRepository):

    def __init__(self, db_session: Session):

        self._db_session = db_session

    def add_user(self, user: User) -> None:

        # Convert to a database model
        user_in_db = UserMapper.to_db_model(user)

        # Add the user to the database
        self._db_session.add(user_in_db)

        # Flush the changes
        self._db_session.flush()

        # Update user ID
        user.id = user_in_db.id

    def get_user_by_id(self, user_id: int) -> User:

        stmt = select(UserInDB).where(UserInDB.id == user_id)
        user_in_db = self._db_session.execute(stmt).scalar_one()

        user = UserMapper.to_domain_model(user_in_db)

        return user

    def find_user_by_email(self, email: str) -> Optional[User]:

        stmt = select(UserInDB).where(UserInDB.email == email)
        user_in_db = self._db_session.execute(stmt).scalar_one_or_none()

        if user_in_db is None:
            return None

        user = UserMapper.to_domain_model(user_in_db)

        return user
