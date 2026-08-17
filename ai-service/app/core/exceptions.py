class AIServiceException(Exception):
    """Base exception for the AI Service."""


class OllamaUnavailableError(AIServiceException):
    """Raised when Ollama is unavailable."""


class PrometheusUnavailableError(AIServiceException):
    """Raised when Prometheus is unavailable."""


class TempoUnavailableError(AIServiceException):
    """Raised when Tempo is unavailable."""


class LokiUnavailableError(AIServiceException):
    """Raised when Loki is unavailable."""