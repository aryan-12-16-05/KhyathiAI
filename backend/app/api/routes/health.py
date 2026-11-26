
from fastapi import APIRouter

from app.core.config import settings


router = APIRouter()


@router.get(
    "/health",
    tags=["Health"],
    summary="Check API health",
    description="Returns the current application health status.",
)
async def health_check() -> dict[str, str]:
    """
    Provides a simple health-check response.
    """

    return {
        "status": "healthy",
        "application": settings.app_name,
        "version": settings.app_version,
    }
