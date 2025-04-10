from sqlmodel import Session, select
from sqlalchemy import Engine
from typing import Optional
import bcrypt
from ..schemas import User, UserCreate


def create_user(engine: Engine, user: User):

    # Store the user ID
    user_id = user.id

    with Session(engine) as session:

        # Insert into database
        session.add(user)

        # Commit transaction
        session.commit()

    return user_id


def create_user_by_email_password(engine: Engine, user_create: UserCreate):

    # Hash the password
    hashed_password = bcrypt.hashpw(
        user_create.password.encode("utf-8"), bcrypt.gensalt()
    ).hex()

    # Create a new user
    user = User(
        display_name=user_create.display_name,
        email=user_create.email,
        hashed_password=hashed_password,
    )

    # Get the user ID
    user_id = user.id

    with Session(engine) as session:

        # Insert into database
        session.add(user)

        # Commit transaction
        session.commit()

    return user_id


def get_user_by_email(engine: Engine, email: str) -> Optional[User]:

    with Session(engine) as session:

        # Query statement
        statement = select(User).where(User.email == email)

        # Execute
        result = session.exec(statement)

        # Get the user
        user = result.one_or_none()

    return user
