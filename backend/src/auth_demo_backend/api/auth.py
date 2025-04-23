from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from auth_demo_backend import services
from auth_demo_backend.config import Config
from auth_demo_backend.api.dependencies import get_config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/sign-in")


def get_current_user_info(
    config: Config = Depends(get_config),
    access_token: str = Depends(oauth2_scheme),
):
    try:
        user_info = services.verify_access_token(access_token, config.jwt_secret_key)
        return user_info

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        ) from e
