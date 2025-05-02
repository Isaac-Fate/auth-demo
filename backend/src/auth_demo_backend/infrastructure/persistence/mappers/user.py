from auth_demo_backend.domain.entities import User
from .mapper import IMapper
from ..models import UserInDB


class UserMapper(IMapper):

    @staticmethod
    def to_domain_model(user_in_db: UserInDB) -> User:

        user = User(
            id=user_in_db.id,
            display_name=user_in_db.display_name,
            email=user_in_db.email,
            hashed_password=user_in_db.hashed_password,
        )

        return user

    @staticmethod
    def to_db_model(user: User) -> UserInDB:

        user_in_db = UserInDB(
            display_name=user.display_name,
            email=user.email,
            hashed_password=user.hashed_password,
        )

        if user.is_id_set():
            user_in_db.id = user.id

        return user_in_db
