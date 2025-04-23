from sqlalchemy import Engine
import bcrypt
import jwt
from authlib.integrations.starlette_client import OAuth, StarletteOAuth2App

from auth_demo_backend.models import User, UserInfo, EmailPasswordSignInData
from .user import get_user_by_email


JWT_ALGORITHM = "HS256"


def sign_in_with_email(
    engine: Engine,
    data: EmailPasswordSignInData,
) -> User:

    # Get the user by email
    user = get_user_by_email(engine, data.email)

    if user is None:
        raise LookupError("user not found")

    # Check password
    if bcrypt.checkpw(
        data.password.encode("utf-8"),
        bytes.fromhex(user.hashed_password),
    ):
        return user

    raise ValueError("invalid password")


def create_google_oauth_app(
    oauth: OAuth,
    google_client_id: str,
    google_client_secret: str,
    jwt_secret_key: str,
) -> StarletteOAuth2App:

    oauth.register(
        name="google",
        client_id=google_client_id,
        client_secret=google_client_secret,
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        authorize_params=None,
        access_token_url="https://oauth2.googleapis.com/token",
        access_token_params=None,
        # authorize_state=jwt_secret_key,
        # redirect_uri="http://localhost:8000/auth/google/callback",
        jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
        client_kwargs={"scope": "openid profile email"},
    )

    google_oauth_app = oauth.create_client("google")
    assert isinstance(google_oauth_app, StarletteOAuth2App)

    return google_oauth_app


def create_access_token(user_info: UserInfo, jwt_secret_key: str) -> str:

    auth_token = jwt.encode(
        payload=user_info.model_dump(),
        key=jwt_secret_key,
        algorithm=JWT_ALGORITHM,
    )

    return auth_token


def verify_access_token(access_token: str, jwt_secret_key: str) -> UserInfo:

    # Decode the token
    payload = jwt.decode(
        jwt=access_token,
        key=jwt_secret_key,
        algorithms=[JWT_ALGORITHM],
    )

    # Convert to UserInfo
    user_info = UserInfo.model_validate(payload)

    return user_info
