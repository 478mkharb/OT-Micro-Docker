import base64
from typing import Any


class ObservabilityNormalizer:
    """
    Converts raw Prometheus and Tempo responses into
    compact, structured observability evidence for the LLM.

    This class does not perform diagnosis or inference.
    It only extracts and formats factual telemetry.
    """

    MONITORING_ENDPOINTS = {
        "/metrics",
        "/actuator/prometheus",
        "/health",
        "/health/",
        "/actuator/health",
        "/actuator/health/",
    }

    def normalize_prometheus(
        self,
        data: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """
        Normalize a Prometheus instant-query response.

        Expected query:
            up

        Returns compact service health information.
        """

        normalized: list[dict[str, Any]] = []

        results = (
            data.get("data", {})
            .get("result", [])
        )

        for item in results:
            metric = item.get("metric", {})
            value = item.get("value", [])

            service = (
                metric.get("job")
                or metric.get("service")
                or metric.get("container")
                or metric.get("instance")
                or "unknown"
            )

            status = "UNKNOWN"

            if len(value) >= 2:
                raw_value = str(value[1])

                if raw_value == "1":
                    status = "UP"
                elif raw_value == "0":
                    status = "DOWN"

            normalized.append(
                {
                    "service": service,
                    "status": status,
                }
            )

        return normalized

    def normalize_tempo(
        self,
        data: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """
        Normalize Tempo trace-search results.

        Each trace is preserved individually so that the AI
        can reason about actual trace IDs, services, endpoints,
        durations, and traffic classification.

        The normalizer does not infer errors or performance
        problems from the trace data.
        """

        traces = data.get("traces", [])

        normalized: list[dict[str, Any]] = []

        for trace in traces:
            root_service = trace.get(
                "rootServiceName",
                "unknown",
            )

            root_trace = trace.get(
                "rootTraceName",
                "unknown",
            )

            trace_id = trace.get(
                "traceID",
                "unknown",
            )

            duration_ms = trace.get(
                "durationMs",
            )

            endpoint = self._extract_endpoint(
                root_trace
            )

            traffic_type = (
                "monitoring"
                if self._is_monitoring_endpoint(endpoint)
                else "business"
            )

            item: dict[str, Any] = {
                "trace_id": trace_id,
                "service": root_service,
                "endpoint": endpoint,
                "traffic_type": traffic_type,
            }

            if duration_ms is not None:
                try:
                    item["duration_ms"] = round(
                        float(duration_ms),
                        2,
                    )
                except (
                    TypeError,
                    ValueError,
                ):
                    item["duration_ms"] = None

            normalized.append(item)

        return normalized

    def normalize_tempo_trace(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Normalize a complete Tempo trace into individual spans.

        The method preserves factual telemetry only.
        It does not perform diagnosis or inference.
        """

        spans: list[dict[str, Any]] = []

        batches = data.get("batches", [])

        for batch in batches:
            resource_attributes = self._attributes_to_dict(
                batch.get("resource", {}).get(
                    "attributes",
                    [],
                )
            )

            service = resource_attributes.get(
                "service.name",
                "unknown",
            )

            scope_spans = batch.get(
                "scopeSpans",
                [],
            )

            for scope in scope_spans:
                for span in scope.get("spans", []):
                    span_attributes = self._attributes_to_dict(
                        span.get("attributes", [])
                    )

                    trace_id = self._decode_otel_id(
                        span.get("traceId")
                    )

                    span_id = self._decode_otel_id(
                        span.get("spanId")
                    )

                    parent_span_id = self._decode_otel_id(
                        span.get("parentSpanId")
                    )

                    start_time = span.get(
                        "startTimeUnixNano"
                    )

                    end_time = span.get(
                        "endTimeUnixNano"
                    )

                    duration_ms = None

                    if start_time is not None and end_time is not None:
                        try:
                            duration_ms = round(
                                (
                                    int(end_time)
                                    - int(start_time)
                                )
                                / 1_000_000,
                                2,
                            )
                        except (
                            TypeError,
                            ValueError,
                        ):
                            duration_ms = None

                    operation = span.get(
                        "name",
                        "unknown",
                    )

                    endpoint = span_attributes.get(
                        "url.path"
                    )

                    status_code = span_attributes.get(
                        "http.response.status_code"
                    )

                    status = self._normalize_span_status(
                        span.get("status", {}),
                        status_code,
                    )

                    item: dict[str, Any] = {
                        "trace_id": trace_id,
                        "span_id": span_id,
                        "parent_span_id": parent_span_id,
                        "service": service,
                        "operation": operation,
                        "duration_ms": duration_ms,
                        "status": status,
                    }

                    if endpoint is not None:
                        item["endpoint"] = endpoint

                    if "db.system" in span_attributes:
                        item["db_system"] = span_attributes[
                            "db.system"
                        ]

                    if "db.statement" in span_attributes:
                        item["db_statement"] = span_attributes[
                            "db.statement"
                        ]

                    if "server.address" in span_attributes:
                        item["server_address"] = span_attributes[
                            "server.address"
                        ]

                    spans.append(item)

        trace_id = "unknown"

        if spans:
            trace_id = spans[0].get(
                "trace_id",
                "unknown",
            )

        return {
            "trace_id": trace_id,
            "span_count": len(spans),
            "spans": spans,
        }

    def _attributes_to_dict(
        self,
        attributes: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Convert OTLP attribute objects into a simple dictionary.
        """

        result: dict[str, Any] = {}

        for attribute in attributes:
            key = attribute.get("key")
            value = attribute.get("value", {})

            if not key:
                continue

            if "stringValue" in value:
                result[key] = value["stringValue"]

            elif "intValue" in value:
                try:
                    result[key] = int(
                        value["intValue"]
                    )
                except (
                    TypeError,
                    ValueError,
                ):
                    result[key] = value["intValue"]

            elif "doubleValue" in value:
                result[key] = value["doubleValue"]

            elif "boolValue" in value:
                result[key] = value["boolValue"]

            elif "arrayValue" in value:
                result[key] = value["arrayValue"]

            else:
                result[key] = value

        return result

    def _decode_otel_id(
        self,
        value: str | None,
    ) -> str | None:
        """
        Convert OTLP base64-encoded trace/span IDs
        into hexadecimal representation.
        """

        if not value:
            return None

        try:
            return base64.b64decode(
                value
            ).hex()
        except (
            ValueError,
            TypeError,
        ):
            return value

    def _normalize_span_status(
        self,
        status: dict[str, Any],
        status_code: int | str | None,
    ) -> str:
        """
        Normalize span status using factual status information.
        """

        status_code_value = str(
            status.get("code", "")
        ).upper()

        if status_code_value in {
            "STATUS_CODE_ERROR",
            "ERROR",
        }:
            return "ERROR"

        if status_code_value in {
            "STATUS_CODE_OK",
            "OK",
        }:
            return "OK"

        if status_code is not None:
            try:
                numeric_status = int(
                    status_code
                )

                if numeric_status >= 500:
                    return "ERROR"

                if 200 <= numeric_status < 500:
                    return "OK"

            except (
                TypeError,
                ValueError,
            ):
                pass

        return "UNSET"


    def build_context(
        self,
        prometheus_data: dict[str, Any],
        tempo_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Build the final compact observability context.
        """

        return {
            "service_health": self.normalize_prometheus(
                prometheus_data
            ),
            "recent_traces": self.normalize_tempo(
                tempo_data
            ),
        }

    def _extract_endpoint(
        self,
        trace_name: str,
    ) -> str:
        """
        Extract the HTTP endpoint from a trace name.

        Examples:

            GET /metrics
            POST /api/v1/employee
            GET /actuator/prometheus

        become:

            /metrics
            /api/v1/employee
            /actuator/prometheus
        """

        parts = trace_name.strip().split(
            maxsplit=1
        )

        if len(parts) == 2:
            return parts[1].strip()

        return trace_name.strip()

    def _is_monitoring_endpoint(
        self,
        endpoint: str,
    ) -> bool:
        """
        Determine whether a trace represents
        monitoring or health-check traffic.
        """

        endpoint = endpoint.lower().strip()
        endpoint = endpoint.split(
            "?",
            1,
        )[0]

        # Exact monitoring endpoints.
        if endpoint in self.MONITORING_ENDPOINTS:
            return True

        # Any endpoint ending in /health is considered
        # monitoring/health-check traffic.
        if endpoint.endswith("/health"):
            return True

        # Common actuator health endpoints.
        if endpoint.endswith("/actuator/health"):
            return True

        return False