from fastapi import FastAPI

from app.api.ask import router as ask_router
from app.api.health import router as health_router
from app.core.config import get_settings
from app.core.lifespan import lifespan
from app.core.logging import get_logger, setup_logging
from app.core.exception_handlers import register_exception_handlers

# Load application settings
settings = get_settings()

# Configure application logging
setup_logging()

# Application logger
logger = get_logger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="AI-powered Observability Assistant for OTMS",
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Register API routers
app.include_router(health_router)
app.include_router(ask_router)


@app.get(
    "/",
    tags=["Root"],
    summary="Root Endpoint",
    description="Returns basic information about the AI Assistant service.",
)
async def root():
    logger.info("Root endpoint accessed.")

    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "status": "Running",
        "documentation": "/docs",
    }