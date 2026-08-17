import re
from dataclasses import dataclass, field


@dataclass
class QueryPlan:
    """
    Describes which observability sources are required
    to answer a user's question.
    """

    sources: list[str] = field(default_factory=list)

    service: str | None = None

    focus: str = "general"

    include_health: bool = False
    include_traces: bool = False
    include_logs: bool = False

    def to_dict(self) -> dict:
        """
        Convert the query plan into a JSON-friendly dictionary.
        """

        return {
            "sources": self.sources,
            "service": self.service,
            "focus": self.focus,
            "include_health": self.include_health,
            "include_traces": self.include_traces,
            "include_logs": self.include_logs,
        }


class QueryPlanner:
    """
    Determines which observability sources should be queried
    based on the user's question.

    This component does NOT answer the question.

    It only decides what evidence should be collected.
    """

    KNOWN_SERVICES = {
        "frontend",
        "employee-api",
        "attendance-api",
        "salary-api",
        "notification-api",
        "redis",
        "scylladb",
        "postgres",
        "elasticsearch",
    }

    ERROR_KEYWORDS = {
        "error",
        "errors",
        "failed",
        "failure",
        "failures",
        "exception",
        "exceptions",
        "500",
        "503",
        "4xx",
        "5xx",
        "problem",
        "problems",
        "issue",
        "issues",
    }

    PERFORMANCE_KEYWORDS = {
        "slow",
        "slowness",
        "latency",
        "performance",
        "delay",
        "delayed",
        "response time",
        "slowest",
        "bottleneck",
        "timeout",
        "timeouts",
    }

    TRACE_KEYWORDS = {
        "trace",
        "traces",
        "span",
        "spans",
        "distributed tracing",
        "request flow",
        "request path",
        "call chain",
        "service flow",
    }

    HEALTH_KEYWORDS = {
        "health",
        "healthy",
        "availability",
        "available",
        "up",
        "down",
        "status",
    }

    LOG_KEYWORDS = {
        "log",
        "logs",
        "logged",
        "http status",
        "status code",
        "500",
        "503",
        "exception",
    }

    def plan(
        self,
        question: str,
    ) -> QueryPlan:
        """
        Build an observability query plan from a user question.
        """

        normalized_question = self._normalize(
            question
        )

        service = self._detect_service(
            normalized_question
        )

        focus = self._detect_focus(
            normalized_question
        )

        sources = self._select_sources(
            focus=focus,
            normalized_question=normalized_question,
        )

        return QueryPlan(
            sources=sources,
            service=service,
            focus=focus,
            include_health="prometheus" in sources,
            include_traces="tempo" in sources,
            include_logs="loki" in sources,
        )

    def _normalize(
        self,
        question: str,
    ) -> str:
        """
        Normalize user input for keyword matching.
        """

        if not question:
            return ""

        return re.sub(
            r"\s+",
            " ",
            question.strip().lower(),
        )

    def _detect_service(
        self,
        question: str,
    ) -> str | None:
        """
        Detect a known OTMS service mentioned in the question.
        """

        # Longest match first so that specific service names
        # are preferred if names overlap.
        services = sorted(
            self.KNOWN_SERVICES,
            key=len,
            reverse=True,
        )

        for service in services:
            if service in question:
                return service

        return None

    def _detect_focus(
        self,
        question: str,
    ) -> str:
        """
        Determine the primary intent of the question.
        """

        if self._contains_any(
            question,
            self.ERROR_KEYWORDS,
        ):
            return "errors"

        if self._contains_any(
            question,
            self.PERFORMANCE_KEYWORDS,
        ):
            return "performance"

        if self._contains_any(
            question,
            self.TRACE_KEYWORDS,
        ):
            return "traces"

        if self._contains_any(
            question,
            self.HEALTH_KEYWORDS,
        ):
            return "health"

        return "general"

    def _select_sources(
        self,
        focus: str,
        normalized_question: str,
    ) -> list[str]:
        """
        Select observability systems required for the question.
        """

        # --------------------------------------------------
        # Error investigation
        # --------------------------------------------------

        if focus == "errors":
            return [
                "loki",
                "tempo",
            ]

        # --------------------------------------------------
        # Performance investigation
        # --------------------------------------------------

        if focus == "performance":
            return [
                "prometheus",
                "tempo",
                "loki",
            ]

        # --------------------------------------------------
        # Trace questions
        # --------------------------------------------------

        if focus == "traces":
            return [
                "tempo",
            ]

        # --------------------------------------------------
        # Health questions
        # --------------------------------------------------

        if focus == "health":
            return [
                "prometheus",
                "loki",
            ]

        # --------------------------------------------------
        # General questions
        # --------------------------------------------------

        return [
            "prometheus",
            "tempo",
            "loki",
        ]

    def _contains_any(
        self,
        question: str,
        keywords: set[str],
    ) -> bool:
        """
        Return True when any keyword appears in the question.
        """

        return any(
            keyword in question
            for keyword in keywords
        )