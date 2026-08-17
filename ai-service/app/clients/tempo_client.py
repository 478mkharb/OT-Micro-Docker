import httpx

from app.core.config import get_settings
from app.core.exceptions import TempoUnavailableError
from app.core.logging import get_logger


settings = get_settings()

logger = get_logger(__name__)


class TempoClient:
    """
    Client responsible for querying traces from Grafana Tempo.
    """

    async def search_traces(
        self,
        http_client: httpx.AsyncClient,
        limit: int = 20,
    ) -> dict:
        """
        Search recent traces from Tempo.
        """

        logger.info(
            "Searching traces from Tempo."
        )

        try:
            response = await http_client.get(
                f"{settings.tempo_url}/api/search",
                params={
                    "limit": limit,
                },
                timeout=30,
            )

            response.raise_for_status()

            result = response.json()

            logger.info(
                "Tempo trace search completed successfully."
            )

            return result

        except (httpx.HTTPError, ValueError) as exc:
            logger.exception(
                "Unable to communicate with Tempo."
            )

            raise TempoUnavailableError(
                "Unable to communicate with Tempo."
            ) from exc

    async def get_trace(
        self,
        http_client: httpx.AsyncClient,
        trace_id: str,
    ) -> dict:
        """
        Retrieve a complete trace from Tempo using its trace ID.
        """

        logger.info(
            "Retrieving trace from Tempo: %s",
            trace_id,
        )

        try:
            response = await http_client.get(
                f"{settings.tempo_url}/api/traces/{trace_id}",
                timeout=30,
            )

            response.raise_for_status()

            result = response.json()

            logger.info(
                "Tempo trace retrieval completed successfully: %s",
                trace_id,
            )

            return result

        except (httpx.HTTPError, ValueError) as exc:
            logger.exception(
                "Unable to retrieve trace from Tempo: %s",
                trace_id,
            )

            raise TempoUnavailableError(
                "Unable to communicate with Tempo."
            ) from exc