from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from auth_demo_backend.application.services import AuthService
from auth_demo_backend.domain.services import AuthService as DomainAuthService
from auth_demo_backend.infrastructure.persistence.repositories import (
    SQLAlchemyUnitOfWork,
)
from auth_demo_backend.infrastructure.auth import JWTAccessTokenIssuer
from auth_demo_backend.config import load_config


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(
        pydantic_settings=[load_config()],
    )

    db_engine = providers.Factory(
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


container = Container()
