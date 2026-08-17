from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from app.core.logging import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage shared application resources.
    """

    logger.info("Starting OTMS AI Assistant...")

    app.state.http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(120.0)
    )

    try:
        yield
    finally:
        logger.info("Stopping OTMS AI Assistant...")

        await app.state.http_client.aclose()

        logger.info("OTMS AI Assistant stopped.")