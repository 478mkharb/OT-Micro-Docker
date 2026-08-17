import httpx

from app.core.config import get_settings
from app.core.exceptions import LokiUnavailableError
from app.core.logging import get_logger


settings = get_settings()

logger = get_logger(__name__)


class LokiClient:
    """
    Client responsible for communicating with Grafana Loki.
    """

    APPLICATION_SERVICES = (
        "frontend",
        "employee-api",
        "attendance-api",
        "salary-api",
        "notification-api",
    )

    async def query_logs(
        self,
        http_client: httpx.AsyncClient,
        service_name: str | None = None,
        limit: int = 50,
    ) -> dict:
        """
        Query recent application logs from Loki.

        If service_name is provided, query that specific service.

        Otherwise, query the known OTMS application services.

        Infrastructure services such as Prometheus, Grafana,
        Loki, Tempo, OTel Collector, exporters, etc. are
        intentionally excluded from the application evidence.
        """

        logger.info(
            "Querying Loki logs (service=%s, limit=%s)",
            service_name,
            limit,
        )

        try:
            # --------------------------------------------------
            # Build LogQL query
            # --------------------------------------------------

            if service_name:
                query = (
                    f'{{service_name="{service_name}"}}'
                )

            else:
                services = "|".join(
                    self.APPLICATION_SERVICES
                )

                query = (
                    f'{{service_name=~"{services}"}}'
                )

            logger.info(
                "Executing Loki query: %s",
                query,
            )

            # --------------------------------------------------
            # Query Loki
            # --------------------------------------------------

            response = await http_client.get(
                f"{settings.loki_url}/loki/api/v1/query_range",
                params={
                    "query": query,
                    "limit": limit,
                },
                timeout=settings.loki_timeout,
            )

            response.raise_for_status()

            result = response.json()

            # --------------------------------------------------
            # Validate Loki response
            # --------------------------------------------------

            if result.get("status") != "success":
                raise LokiUnavailableError(
                    "Loki returned an unsuccessful response."
                )

            logger.info(
                "Loki log query completed successfully."
            )

            return result

        except LokiUnavailableError:
            raise

        except (
            httpx.HTTPError,
            ValueError,
        ) as exc:
            logger.exception(
                "Unable to communicate with Loki."
            )

            raise LokiUnavailableError(
                "Unable to communicate with Loki."
            ) from exc