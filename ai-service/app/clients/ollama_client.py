import httpx

from app.core.config import get_settings
from app.core.exceptions import OllamaUnavailableError
from app.core.logging import get_logger


settings = get_settings()

logger = get_logger(__name__)


class OllamaClient:
    """
    Client responsible for communicating with Ollama.
    """

    async def generate(
        self,
        http_client: httpx.AsyncClient,
        prompt: str,
    ) -> str:
        """
        Generate a response from the configured Ollama model.

        The generation length is deliberately limited because
        the OTMS AI Assistant is intended to provide concise,
        evidence-based observability answers.
        """

        logger.info(
            "Sending request to Ollama (model=%s)",
            settings.ollama_model,
        )

        try:
            response = await http_client.post(
                f"{settings.ollama_base_url}/api/generate",
                json={
                    "model": settings.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": 384,
                    },
                },
                timeout=settings.ollama_timeout,
            )

            response.raise_for_status()

            result = response.json()

            if "response" not in result:
                raise OllamaUnavailableError(
                    "Ollama returned an invalid response."
                )

            logger.info(
                "Received response from Ollama."
            )

            logger.info(
                "Ollama generation completed "
                "(prompt_tokens=%s, response_tokens=%s, "
                "total_duration_ns=%s).",
                result.get("prompt_eval_count"),
                result.get("eval_count"),
                result.get("total_duration"),
            )

            return result["response"]

        except OllamaUnavailableError:
            raise

        except (
            httpx.HTTPError,
            KeyError,
            ValueError,
        ) as exc:

            logger.exception(
                "Unable to communicate with Ollama."
            )

            raise OllamaUnavailableError(
                "Unable to communicate with Ollama."
            ) from exc