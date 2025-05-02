from typing import Optional, Type, Callable
from types import TracebackType
from sqlalchemy.orm import Session

from auth_demo_backend.domain.repositories import IUnitOfWork
from .user_repository import SQLAlchemyUserRepository
from .account_repository import SQLAlchemyAccountRepository


class SQLAlchemyUnitOfWork(IUnitOfWork):

    def __init__(self, db_session_factory: Callable[[], Session]):

        self._session_factory = db_session_factory

    def __enter__(self):

        # Create a new session for the unit of work
        self._db_session = self._session_factory()

        # Initialize repositories
        self.user_repository = SQLAlchemyUserRepository(self._db_session)
        self.account_repository = SQLAlchemyAccountRepository(self._db_session)

        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        try:
            # Commit the changes if no exception was raised
            if exc_type is None:
                self.commit()

            # Rollback the changes if an exception was raised
            else:
                self.rollback()

        except Exception as error:
            raise error

        finally:
            # Close the database session
            self._db_session.close()

    def commit(self):

        self._db_session.commit()

    def rollback(self):

        self._db_session.rollback()
