from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    AIServiceException,
    OllamaUnavailableError,
    PrometheusUnavailableError,
    TempoUnavailableError,
    LokiUnavailableError,
)
from app.core.logging import get_logger

logger = get_logger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all application exception handlers.
    """

    @app.exception_handler(OllamaUnavailableError)
    async def ollama_exception_handler(
        request: Request,
        exc: OllamaUnavailableError,
    ):
        logger.error("Ollama unavailable: %s", exc)

        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "error": "OLLAMA_UNAVAILABLE",
                "message": str(exc),
            },
        )

    @app.exception_handler(PrometheusUnavailableError)
    async def prometheus_exception_handler(
        request: Request,
        exc: PrometheusUnavailableError,
    ):
        logger.error("Prometheus unavailable: %s", exc)

        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "error": "PROMETHEUS_UNAVAILABLE",
                "message": str(exc),
            },
        )

    @app.exception_handler(TempoUnavailableError)
    async def tempo_exception_handler(
        request: Request,
        exc: TempoUnavailableError,
    ):
        logger.error("Tempo unavailable: %s", exc)

        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "error": "TEMPO_UNAVAILABLE",
                "message": str(exc),
            },
        )

    @app.exception_handler(LokiUnavailableError)
    async def loki_exception_handler(
        request: Request,
        exc: LokiUnavailableError,
    ):
        logger.error("Loki unavailable: %s", exc)

        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "error": "LOKI_UNAVAILABLE",
                "message": str(exc),
            },
        )

    @app.exception_handler(AIServiceException)
    async def ai_exception_handler(
        request: Request,
        exc: AIServiceException,
    ):
        logger.error("AI Service error: %s", exc)

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "AI_SERVICE_ERROR",
                "message": str(exc),
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception,
    ):
        logger.exception("Unexpected exception.")

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred.",
            },
        )