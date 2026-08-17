from fastapi import APIRouter

from app.core.config import get_settings
from app.core.logging import get_logger

settings = get_settings()

logger = get_logger(__name__)

router = APIRouter(
    prefix=settings.api_prefix,
    tags=["Health"],
)


@router.get(
    "/health",
    summary="Health Check",
    description="Returns the health status of the AI Assistant service.",
)
async def health():
    logger.info("Health check requested.")

    return {
        "status": "UP",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }