import jwt
import datetime as dt

from auth_demo_backend.domain.ports.access_token_issuer import IAccessTokenIssuer
from auth_demo_backend.domain.entities import User

# Expiration duration
EXPIRATION_DURATION = dt.timedelta(seconds=3600)


class JWTAccessTokenIssuer(IAccessTokenIssuer):

    def __init__(self, secret_key: str, algorithm: str):

        self._secret_key = secret_key
        self._algorithm = algorithm

    def issue_access_token(self, user: User) -> str:

        payload = {
            "user": {
                "id": user.id,
                "displayName": user.display_name,
                "email": user.email,
            },
            "exp": dt.datetime.now(dt.UTC) + EXPIRATION_DURATION,
        }

        access_token = jwt.encode(
            payload=payload,
            key=self._secret_key,
            algorithm=self._algorithm,
        )

        return access_token

    def verify_access_token(self, access_token: str) -> User:

        payload = jwt.decode(
            jwt=access_token,
            key=self._secret_key,
            algorithms=[self._algorithm],
        )

        user_dict = payload["user"]

        user = User(
            id=user_dict["id"],
            display_name=user_dict["displayName"],
            email=user_dict["email"],
        )

        return user
