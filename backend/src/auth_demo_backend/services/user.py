from sqlmodel import Session, select
from typing import Optional
import bcrypt

from auth_demo_backend.db.models import UserInDB
from auth_demo_backend.models import User, UserCreate


def create_user(db_session: Session, user_create: UserCreate) -> User:

    # Create a new user in the database
    user_in_db = UserInDB(**user_create.model_dump())

    # Insert into database
    db_session.add(user_in_db)

    # Commit transaction
    db_session.commit()

    # Refresh the object to get the latest data
    db_session.refresh(user_in_db)

    # Convert to Pydantic model
    user = User.model_validate(user_in_db)

    return user


def create_user_by_email_and_password(db_session: Session, user_create: UserCreate):

    # Hash the password
    hashed_password = bcrypt.hashpw(
        user_create.password.encode("utf-8"),
        bcrypt.gensalt(),
    ).hex()

    # Convert to a dictionary
    user_create_dict = user_create.model_dump()

    # Remove the password field
    user_create_dict.pop("password")

    # Create a UserInDB instance
    user_in_db = UserInDB(**user_create_dict, hashed_password=hashed_password)

    # Insert into database
    db_session.add(user_in_db)

    # Commit transaction
    db_session.commit()

    # Refresh the object to get the latest data
    db_session.refresh(user_in_db)

    # Convert to Pydantic model
    user = User.model_validate(user_in_db)

    return user


def get_user_by_email(db_session: Session, email: str) -> Optional[User]:

    # Query statement
    statement = select(User).where(User.email == email)

    # Execute
    user_in_db = db_session.exec(statement).one_or_none()

    if user_in_db is None:
        return None

    # Convert to Pydantic model
    user = User.model_validate(user_in_db)

    return user
