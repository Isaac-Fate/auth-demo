from fastapi import Request
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import StarletteOAuth2App

from auth_demo_backend.config import Config


def get_config(request: Request) -> Config:

    return request.app.state.config


def get_db_engine(request: Request) -> Engine:

    return request.app.state.db_engine


def get_db_session(request: Request):

    # Get the database engine
    db_engine = request.app.state.db_engine

    # Create the database session
    db_session = Session(db_engine)

    yield db_session

    db_session.close()


def get_google_oauth_app(request: Request) -> StarletteOAuth2App:

    return request.app.state.google_oauth_app
