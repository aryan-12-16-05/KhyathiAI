
from fastapi import APIRouter

from app.api.routes.health import router as health_router

from app.features.summarizer.api.routes import (
    router as summarizer_router,
)


api_router = APIRouter()

# Health endpoints
api_router.include_router(health_router)

# Feature-specific endpoints
api_router.include_router(summarizer_router)
