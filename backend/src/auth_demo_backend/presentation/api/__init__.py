from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager

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
