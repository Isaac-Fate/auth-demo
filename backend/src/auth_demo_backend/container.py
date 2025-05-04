from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from authlib.integrations.starlette_client import OAuth

from auth_demo_backend.application.services import AuthService
from auth_demo_backend.domain.services import AuthService as DomainAuthService
from auth_demo_backend.infrastructure.persistence.repositories import (
    SQLAlchemyUnitOfWork,
)
from auth_demo_backend.infrastructure.auth import JWTAccessTokenIssuer
from auth_demo_backend.config import load_config


def register_oauth(
    *,
    google_client_id: str,
    google_client_secret: str,
):

    oauth = OAuth()

    oauth.register(
        name="google",
        client_id=google_client_id,
        client_secret=google_client_secret,
        # server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        access_token_url="https://oauth2.googleapis.com/token",
        authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
        jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
        client_kwargs={
            "scope": "openid profile email",
        },
    )

    return oauth


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(
        pydantic_settings=[load_config()],
    )

    db_engine = providers.Singleton(
        create_engine,
        config.postgres_uri,
    )

    db_session_factory = providers.Factory(
        sessionmaker,
        bind=db_engine,
    )

    auth_service = providers.Factory(
        AuthService,
        domain_auth_service=providers.Factory(
            DomainAuthService,
            unit_of_work=providers.Factory(
                SQLAlchemyUnitOfWork,
                db_session_factory=db_session_factory,
            ),
            access_token_issuer=providers.Factory(
                JWTAccessTokenIssuer,
                secret_key=config.jwt_secret_key,
                algorithm=config.jwt_algorithm,
            ),
        ),
    )

    oauth = providers.Factory(
        register_oauth,
        google_client_id=config.google_client_id,
        google_client_secret=config.google_client_secret,
    )


container = Container()
