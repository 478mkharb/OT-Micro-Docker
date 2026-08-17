import httpx

from app.core.config import get_settings
from app.core.exceptions import PrometheusUnavailableError
from app.core.logging import get_logger

settings = get_settings()

logger = get_logger(__name__)


class PrometheusClient:
    """
    Client responsible for communicating with Prometheus.
    """

    async def query(
        self,
        http_client: httpx.AsyncClient,
        promql: str,
    ) -> dict:
        """
        Execute an instant PromQL query against Prometheus.
        """

        logger.info(
            "Executing Prometheus query: %s",
            promql,
        )

        try:
            response = await http_client.get(
                f"{settings.prometheus_url}/api/v1/query",
                params={
                    "query": promql,
                },
                timeout=settings.prometheus_timeout,
            )

            response.raise_for_status()

            result = response.json()

            if result.get("status") != "success":
                raise PrometheusUnavailableError(
                    "Prometheus returned an unsuccessful response."
                )

            logger.info(
                "Prometheus query completed successfully."
            )

            return result

        except PrometheusUnavailableError:
            raise

        except (httpx.HTTPError, ValueError) as exc:
            logger.exception(
                "Unable to communicate with Prometheus."
            )

            raise PrometheusUnavailableError(
                "Unable to communicate with Prometheus."
            ) from exc