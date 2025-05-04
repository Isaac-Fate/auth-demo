from fastapi import FastAPI, APIRouter
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .middlewares import auth_middleware
from .routers.health import router as health_router
from .routers.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup
    print("starting up...")

    # Main app
    yield

    # Shutdown
    print("shutting down...")


# Create a FastAPI instance
app = FastAPI(
    title="Auth Demo",
    lifespan=lifespan,
)

# Add middlewares

# Session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key="middleware-secret-key",
)

# Auth middleware
app.middleware("http")(auth_middleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a root router for all APIs
api_router = APIRouter(prefix="/api")

# Register routers
api_router.include_router(health_router)
api_router.include_router(auth_router)

# Add the API root router
app.include_router(api_router)


__all__ = [
    "app",
]
