# ==================================================
# Stage 1 - Build Salary API
# ==================================================
FROM maven:3.9.9-eclipse-temurin-17 AS builder

WORKDIR /workspace

# Install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        make \
        jq \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pom.xml .
COPY src/ src/
COPY migration/ migration/
COPY Makefile .

# Build application
RUN mvn clean package -DskipTests

# Download migrate binary
RUN wget -qO- \
https://github.com/golang-migrate/migrate/releases/latest/download/migrate.linux-amd64.tar.gz \
| tar -xz -C /tmp

# Download OpenTelemetry Java Agent
RUN wget -O /tmp/opentelemetry-javaagent.jar \
https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/download/v2.20.1/opentelemetry-javaagent.jar

# ==================================================
# Stage 2 - Runtime
# ==================================================
FROM alpine:3.21

LABEL authors="Opstree Solution" \
      application="Salary API" \
      version="v0.1.0"

WORKDIR /app

# Runtime dependencies
RUN apk add --no-cache \
    openjdk17-jre \
    bash \
    curl \
    make \
    jq \
    netcat-openbsd \
    ca-certificates

# Copy application
COPY --from=builder /workspace/target/*.jar /app/salary.jar

# Copy OpenTelemetry Java Agent
COPY --from=builder /tmp/opentelemetry-javaagent.jar /otel/opentelemetry-javaagent.jar

# OpenTelemetry Configuration
ENV OTEL_SERVICE_NAME=salary-api \
    OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318 \
    OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf \
    OTEL_TRACES_EXPORTER=otlp \
    OTEL_METRICS_EXPORTER=none \
    OTEL_LOGS_EXPORTER=none \
    OTEL_INSTRUMENTATION_CASSANDRA_ENABLED=true \
    OTEL_INSTRUMENTATION_SPRING_DATA_ENABLED=true \
    OTEL_RESOURCE_ATTRIBUTES=service.name=salary-api

EXPOSE 8082

ENTRYPOINT ["java","-javaagent:/otel/opentelemetry-javaagent.jar","-jar","/app/salary.jar"]