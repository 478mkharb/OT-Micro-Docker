import json
from typing import Any

import httpx

from app.clients.loki_client import LokiClient
from app.clients.ollama_client import OllamaClient
from app.clients.prometheus_client import PrometheusClient
from app.clients.tempo_client import TempoClient
from app.core.logging import get_logger
from app.services.normalizers.loki_normalizer import LokiNormalizer
from app.services.normalizers.observability_normalizer import (
    ObservabilityNormalizer,
)
from app.services.query_planner import QueryPlanner


logger = get_logger(__name__)


class AIService:
    """
    Business layer responsible for AI observability orchestration.

    The service:

        1. Plans which observability sources are required.
        2. Collects telemetry from Prometheus, Tempo and/or Loki.
        3. Normalizes telemetry into compact evidence.
        4. Uses deterministic fast-path responses for simple
           retrieval questions.
        5. Uses Ollama only when reasoning/investigation is required.
    """

    def __init__(self):
        self.ollama = OllamaClient()

        self.prometheus = PrometheusClient()
        self.tempo = TempoClient()
        self.loki = LokiClient()

        self.observability_normalizer = (
            ObservabilityNormalizer()
        )

        self.loki_normalizer = LokiNormalizer()

        self.query_planner = QueryPlanner()

    async def ask(
        self,
        http_client: httpx.AsyncClient,
        question: str,
    ) -> str:
        """
        Process a user question using query-aware observability.

        Simple retrieval questions use deterministic responses
        and do not invoke Ollama.

        Investigation questions use the collected telemetry
        as evidence for Ollama.
        """

        logger.info(
            "Processing AI request."
        )

        # ==================================================
        # 1. Build query plan
        # ==================================================

        query_plan = self.query_planner.plan(
            question
        )

        logger.info(
            "Query plan: sources=%s, service=%s, focus=%s",
            query_plan.sources,
            query_plan.service,
            query_plan.focus,
        )

        # ==================================================
        # 2. Initialize empty telemetry results
        # ==================================================

        prometheus_result: dict[str, Any] = {}
        tempo_result: dict[str, Any] = {}
        loki_result: dict[str, Any] = {}

        # ==================================================
        # 3. Collect Prometheus metrics
        # ==================================================

        if query_plan.include_health:
            prometheus_result = await self.prometheus.query(
                http_client=http_client,
                promql="up",
            )

            logger.info(
                "Prometheus context collected successfully."
            )
        else:
            logger.info(
                "Prometheus query skipped by query planner."
            )

        # ==================================================
        # 4. Collect Tempo traces
        # ==================================================

        if query_plan.include_traces:
            tempo_result = await self.tempo.search_traces(
                http_client=http_client,
                limit=20,
            )

            logger.info(
                "Tempo trace context collected successfully."
            )
        else:
            logger.info(
                "Tempo query skipped by query planner."
            )

        # ==================================================
        # 5. Collect Loki logs
        # ==================================================

        if query_plan.include_logs:
            loki_result = await self.loki.query_logs(
                http_client=http_client,
                service_name=query_plan.service,
                limit=50,
            )

            logger.info(
                "Loki log context collected successfully."
            )
        else:
            logger.info(
                "Loki query skipped by query planner."
            )

        # ==================================================
        # 6. Normalize Prometheus + Tempo
        # ==================================================

        observability_context = (
            self.observability_normalizer.build_context(
                prometheus_data=prometheus_result,
                tempo_data=tempo_result,
            )
        )

        logger.info(
            "Prometheus and Tempo context normalized."
        )

        # ==================================================
        # 7. Normalize Loki
        # ==================================================

        loki_context: list[dict[str, Any]] = []

        if query_plan.include_logs:
            loki_context = (
                self.loki_normalizer.normalize(
                    loki_result
                )
            )

            logger.info(
                "Loki context normalized."
            )
        else:
            logger.info(
                "Loki normalization skipped."
            )

        # ==================================================
        # 8. FAST PATH
        # ==================================================
        #
        # Simple retrieval questions do not need an LLM.
        #
        # This is intentionally AFTER telemetry collection
        # and normalization, so the response is based on
        # actual live observability evidence.
        # ==================================================

        fast_response = self._build_fast_response(
            query_plan=query_plan,
            observability_context=observability_context,
            loki_context=loki_context,
        )

        if fast_response is not None:
            logger.info(
                "Returning deterministic fast-path response."
            )

            return fast_response

        # ==================================================
        # 9. Build combined evidence for AI investigation
        # ==================================================

        combined_context: dict[str, Any] = {}

        if query_plan.include_health:
            combined_context["service_health"] = (
                observability_context.get(
                    "service_health",
                    [],
                )
            )

        if query_plan.include_traces:
            combined_context["recent_traces"] = (
                observability_context.get(
                    "recent_traces",
                    [],
                )
            )

        if query_plan.include_logs:
            combined_context["recent_logs"] = loki_context

        combined_context["query_context"] = {
            "focus": query_plan.focus,
            "service": query_plan.service,
            "sources": query_plan.sources,
        }

        context_json = json.dumps(
            combined_context,
            indent=2,
        )

        logger.info(
            "Observability context normalized successfully."
        )

        logger.info(
            "Normalized context size: %d characters.",
            len(context_json),
        )

        # ==================================================
        # 10. Build evidence-based AI prompt
        # ==================================================

        prompt = f"""
You are the OTMS AI Observability Assistant.

OTMS is an Office Transport Management System consisting
of multiple microservices and supporting infrastructure.

The user's question has been analyzed by a deterministic
observability query planner.

QUERY PLAN:

Focus:
{query_plan.focus}

Service:
{query_plan.service or "All relevant services"}

Observability sources collected:
{", ".join(query_plan.sources)}

You have access only to the telemetry sources listed above.

OBSERVABILITY SOURCES:

1. Prometheus

   - Service health
   - Target availability

2. Grafana Tempo

   - Recent distributed traces
   - Trace IDs
   - Services
   - Endpoints
   - Trace durations
   - Traffic classification

3. Grafana Loki

   - Recent application HTTP activity
   - HTTP methods
   - Endpoints
   - HTTP status codes
   - Request latency
   - Trace IDs
   - Span IDs
   - Traffic classification

IMPORTANT EVIDENCE RULES:

Use ONLY the supplied observability evidence as factual
evidence.

Do NOT invent:

- metrics
- traces
- logs
- services
- endpoints
- incidents
- errors
- performance problems
- root causes

Do NOT assume that absence of an error in the supplied
sample means the entire OTMS system has no errors.

The evidence represents a recent telemetry sample.

Prometheus "UP" means that the corresponding target was
reachable and successfully scraped. It does NOT by itself
prove that the application has no errors.

Monitoring traffic includes endpoints such as:

- /metrics
- /health
- /actuator/health
- /actuator/prometheus

Do not automatically treat monitoring traffic as business
traffic.

HTTP status classification:

- success = HTTP 200-299
- redirect = HTTP 300-399
- client_error = HTTP 400-499
- server_error = HTTP 500+

A slow request is evidence of latency in the observed
request. Do not infer the root cause unless the telemetry
supports that conclusion.

Tempo trace IDs identify individual traces returned by
the recent Tempo trace search.

Each Tempo trace record represents one observed trace from
the supplied telemetry sample.

A Tempo trace ID is not a span ID.

Detailed span information must not be invented when it is
not present in the supplied evidence.

IMPORTANT:

If a telemetry source was not collected, do not claim that
the source confirms or disproves anything.

If the supplied telemetry is insufficient to answer the
question, explicitly say:

"Additional telemetry is required."

When answering, distinguish clearly between:

1. What the telemetry directly shows.
2. What can reasonably be inferred.
3. What cannot be determined from the available evidence.

Do not use phrases such as:

- "the entire system is healthy"
- "there are definitely no errors"
- "all requests are successful"

unless the supplied evidence actually proves that statement.

Prefer precise wording such as:

"No errors are evident in the supplied recent telemetry."

or:

"The supplied telemetry does not show evidence of a
performance problem."

Keep the answer concise and technically accurate.

TRACE QUESTION RULES:

If the user's question is about recent traces and the
"recent_traces" evidence contains one or more records:

- Confirm that recent traces are available.
- State the number of traces in the supplied sample.
- Summarize the observed services and endpoints.
- Include trace IDs when useful.
- Include duration when available.
- Identify whether the traces are monitoring or business
  traffic.
- Do NOT say that no traces exist.
- Do NOT claim that the sample represents every trace in
  OTMS.

OBSERVABILITY EVIDENCE:

{context_json}

USER QUESTION:

{question}

Answer the user's question using only the supplied
observability evidence.
"""

        # ==================================================
        # 11. Send evidence to Ollama
        # ==================================================

        logger.info(
            "Sending investigation request to Ollama."
        )

        response = await self.ollama.generate(
            http_client=http_client,
            prompt=prompt,
        )

        logger.info(
            "AI response generated successfully."
        )

        return response

    def _build_fast_response(
        self,
        query_plan,
        observability_context: dict[str, Any],
        loki_context: list[dict[str, Any]],
    ) -> str | None:
        """
        Build deterministic responses for simple retrieval
        questions.

        Returns:
            str  -> fast-path response
            None -> question requires AI reasoning
        """

        # ==================================================
        # TRACE RETRIEVAL
        # ==================================================

        if query_plan.focus == "traces":
            traces = observability_context.get(
                "recent_traces",
                [],
            )

            return self._format_recent_traces(
                traces
            )

        # ==================================================
        # HEALTH RETRIEVAL
        # ==================================================

        if query_plan.focus == "health":
            health = observability_context.get(
                "service_health",
                [],
            )

            return self._format_service_health(
                health,
                service_name=query_plan.service,
            )

        # ==================================================
        # ERROR RETRIEVAL
        # ==================================================

        if query_plan.focus == "errors":
            return self._format_recent_errors(
                loki_context
            )

        # ==================================================
        # EVERYTHING ELSE
        # ==================================================

        return None

    def _format_recent_traces(
        self,
        traces: list[dict[str, Any]],
    ) -> str:
        """
        Format recent Tempo traces without using Ollama.
        """

        if not traces:
            return (
                "No recent traces were returned by the "
                "supplied Tempo query."
            )

        lines = [
            f"{len(traces)} recent Tempo traces were "
            "returned in the supplied telemetry sample.",
            "",
        ]

        for index, trace in enumerate(
            traces,
            start=1,
        ):
            trace_id = trace.get(
                "trace_id",
                "unknown",
            )

            service = trace.get(
                "service",
                "unknown",
            )

            endpoint = trace.get(
                "endpoint",
                "unknown",
            )

            traffic_type = trace.get(
                "traffic_type",
                "unknown",
            )

            duration = trace.get(
                "duration_ms"
            )

            if duration is not None:
                duration_text = (
                    f"{duration} ms"
                )
            else:
                duration_text = "unknown"

            lines.append(
                f"{index}. {service} | "
                f"{endpoint} | "
                f"{traffic_type} | "
                f"{duration_text} | "
                f"trace_id={trace_id}"
            )

        return "\n".join(lines)

    def _format_service_health(
        self,
        health: list[dict[str, Any]],
        service_name: str | None = None,
    ) -> str:
        """
        Format Prometheus service health without using Ollama.
        """

        if not health:
            return (
                "No service health data was returned by "
                "the supplied Prometheus query."
            )

        if service_name:
            matching = [
                item
                for item in health
                if item.get("service") == service_name
            ]

            if not matching:
                return (
                    f"No Prometheus health data was found "
                    f"for service '{service_name}'."
                )

            item = matching[0]

            return (
                f"{service_name}: "
                f"{item.get('status', 'UNKNOWN')}"
            )

        lines = [
            f"{len(health)} Prometheus service-health "
            "records were returned:",
            "",
        ]

        for item in health:
            lines.append(
                f"- {item.get('service', 'unknown')}: "
                f"{item.get('status', 'UNKNOWN')}"
            )

        return "\n".join(lines)

    def _format_recent_errors(
        self,
        loki_context: list[dict[str, Any]],
    ) -> str:
        """
        Format recent Loki error evidence without using Ollama.
        """

        errors = [
            item
            for item in loki_context
            if item.get("error") is True
            or item.get("status_type")
            in {
                "client_error",
                "server_error",
            }
        ]

        if not loki_context:
            return (
                "No recent Loki log records were returned "
                "for the supplied telemetry sample."
            )

        if not errors:
            return (
                "No errors are evident in the supplied "
                "recent Loki telemetry sample. "
                "This does not prove that OTMS has no errors."
            )

        lines = [
            f"{len(errors)} recent error record(s) were "
            "identified in the supplied Loki telemetry:",
            "",
        ]

        for index, error in enumerate(
            errors,
            start=1,
        ):
            service = error.get(
                "service",
                "unknown",
            )

            method = error.get(
                "method",
                "UNKNOWN",
            )

            endpoint = error.get(
                "endpoint",
                "unknown",
            )

            status = error.get(
                "status",
                "unknown",
            )

            status_type = error.get(
                "status_type",
                "unknown",
            )

            request_count = error.get(
                "request_count",
                1,
            )

            lines.append(
                f"{index}. {service} | "
                f"{method} {endpoint} | "
                f"status={status} "
                f"({status_type}) | "
                f"requests={request_count}"
            )

        return "\n".join(lines)