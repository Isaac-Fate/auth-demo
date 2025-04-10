from fastapi import FastAPI
from .routers.health import router as health_router

app = FastAPI()

# Register routers
app.include_router(health_router)
