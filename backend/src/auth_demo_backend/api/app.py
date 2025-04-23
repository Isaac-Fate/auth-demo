from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from sqlalchemy import create_engine

from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from ..config import load_config
from .. import services
from .routers.health import router as health_router
from .routers.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Start up
    print("Starting up...")

    # Set app state

    # App configuration
    app_config = load_config()
    app.state.config = app_config

    # OAuth

    oauth = OAuth()

    app.state.google_oauth_app = services.create_google_oauth_app(
        oauth,
        app_config.google_client_id,
        app_config.google_client_secret,
        app_config.jwt_secret_key,
    )

    # Database engine
    app.state.db_engine = create_engine(app_config.postgres_uri)

    # App starts here
    yield

    # Shut down
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    "app-secret-key",
)

# API router
api_router = APIRouter(prefix="/api")


# Register routers
api_router.include_router(health_router)
api_router.include_router(auth_router)
app.include_router(api_router)
