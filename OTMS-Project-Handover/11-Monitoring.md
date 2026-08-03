# 11 - Monitoring and Observability

---

# Monitoring and Observability

---

# Introduction

Monitoring is a critical aspect of any modern distributed application. In a microservices architecture, multiple services run independently, making it difficult to understand the overall health of the system without centralized observability.

The OT-Micro-Docker project integrates a complete observability stack to monitor infrastructure, collect metrics, visualize application performance, aggregate logs, and trace requests across services.

The monitoring stack is designed to support both local Docker Compose deployments and future Kubernetes or Amazon EKS environments.

---

# Why Monitoring?

As the number of services grows, manually checking each container becomes impractical.

Monitoring helps answer questions such as:

- Is every service running?
- Which service is consuming high CPU?
- Is memory usage increasing?
- Are requests failing?
- Which container restarted unexpectedly?
- Are emails being sent successfully?
- Is the database responding?
- Which API is slow?

Without monitoring, troubleshooting becomes reactive and time-consuming.

---

# Monitoring Objectives

The OTMS monitoring stack provides:

- Infrastructure monitoring
- Container monitoring
- Application metrics
- Centralized dashboards
- Alerting
- Log aggregation
- Distributed tracing
- Service health monitoring

---

# Monitoring Architecture

```
                    +----------------------+
                    |     React UI         |
                    +----------+-----------+
                               |
                               |
                     Application Metrics
                               |
                               ▼

                  +------------------------+
                  | OpenTelemetry Collector|
                  +-----------+------------+
                              |
          +-------------------+--------------------+
          |                   |                    |
          ▼                   ▼                    ▼

   Prometheus            Loki                Tempo
      │                    │                    │
      │                    │                    │
      └──────────────┬─────┴──────────────┬─────┘
                     ▼                    ▼

                  Grafana Dashboards

```

---

# Components

| Component | Purpose |
|------------|---------|
| Prometheus | Metrics Collection |
| Grafana | Visualization |
| Loki | Log Aggregation |
| Tempo | Distributed Tracing |
| OpenTelemetry Collector | Telemetry Pipeline |
| Alertmanager | Alert Routing |
| Node Exporter | Host Metrics |
| cAdvisor | Container Metrics |

---

# Prometheus

## Purpose

Prometheus collects metrics from infrastructure and application services.

Metrics include:

- CPU usage
- Memory usage
- Disk usage
- Network traffic
- HTTP requests
- API latency
- Error rates

---

## Docker Image

```text
prom/prometheus:v3.13.1
```

---

## Port

```text
9090
```

---

## Responsibilities

- Scrape metrics
- Store time-series data
- Execute alert rules
- Provide query interface

---

## Data Source

Prometheus scrapes metrics from:

- Employee API
- Attendance API
- Salary API
- Notification API
- Node Exporter
- cAdvisor
- OpenTelemetry Collector

---

# Grafana

## Purpose

Grafana provides dashboards for visualizing metrics collected by Prometheus and logs stored in Loki.

---

## Docker Image

```text
grafana/grafana:13.1.0
```

---

## Port

```text
3000
```

---

## Responsibilities

- Dashboards
- Alert visualization
- Log exploration
- Trace visualization

---

## Data Sources

Grafana connects to:

- Prometheus
- Loki
- Tempo

---

# Loki

## Purpose

Loki provides centralized log aggregation.

Instead of checking logs from each container individually, logs are collected into one place.

---

## Docker Image

```text
grafana/loki:3.7.2
```

---

## Port

```text
3100
```

---

## Responsibilities

- Collect application logs
- Store logs efficiently
- Enable log searching
- Integrate with Grafana

---

# Tempo

## Purpose

Tempo stores distributed traces.

Tracing helps understand how a request flows through multiple microservices.

---

## Docker Image

```text
grafana/tempo:2.10.5
```

---

## Port

```text
3200
```

---

## Responsibilities

- Store traces
- Trace visualization
- Service dependency analysis

---

# OpenTelemetry Collector

## Purpose

The OpenTelemetry Collector receives telemetry from applications and exports it to multiple backends.

---

## Docker Image

```text
otel/opentelemetry-collector-contrib:0.157.0
```

---

## Ports

| Port | Purpose |
|------|---------|
| 4317 | OTLP gRPC |
| 4318 | OTLP HTTP |
| 13133 | Health Check |

---

## Responsibilities

- Receive metrics
- Receive traces
- Receive logs
- Export telemetry

---

# Alertmanager

## Purpose

Alertmanager receives alerts from Prometheus and routes them to notification channels.

---

## Docker Image

```text
prom/alertmanager:v0.32.1
```

---

## Port

```text
9093
```

---

## Responsibilities

- Alert grouping
- Alert routing
- Email notifications
- Slack notifications

---

# Node Exporter

## Purpose

Node Exporter exposes operating system metrics.

---

## Metrics

- CPU usage
- Memory usage
- Disk usage
- Network traffic
- File system statistics

---

## Port

```text
9100
```

---

# cAdvisor

## Purpose

cAdvisor monitors Docker containers.

---

## Metrics

- CPU usage
- Memory usage
- Network usage
- Container restarts
- Filesystem usage

---

## Port

```text
8080
```

---

# Monitoring Network

A dedicated Docker network is used.

```yaml
observability
```

This isolates monitoring components from application traffic.

---

# Docker Volumes

Monitoring services store persistent data.

| Volume | Purpose |
|---------|----------|
| prometheus_data | Metrics |
| grafana_data | Dashboards |
| loki_data | Logs |
| alertmanager_data | Alerts |

---

# Application Metrics

The OTMS services expose metrics endpoints.

| Service | Metrics Endpoint |
|----------|------------------|
| Employee API | `/metrics` |
| Attendance API | `/metrics` |
| Salary API | `/actuator/prometheus` |
| Notification API | `/metrics` |

> **Note:** These endpoints should exist only if the respective application has Prometheus instrumentation enabled.

---

# Log Collection

Application logs flow through the following pipeline.

```
Application

↓

Docker Logs

↓

Loki

↓

Grafana
```

Benefits

- Centralized logging
- Full-text search
- Log correlation

---

# Distributed Tracing

A single request may pass through multiple services.

Example

```
Browser

↓

Frontend

↓

Salary API

↓

ScyllaDB

↓

Scylla Sync

↓

Elasticsearch

↓

Notification API

↓

SMTP
```

Tempo stores the complete trace.

---

# Dashboard Categories

The monitoring solution provides dashboards for:

- Host Metrics
- Docker Containers
- Application Metrics
- JVM Metrics
- Go Runtime Metrics
- Python Metrics
- Redis Metrics
- PostgreSQL Metrics
- ScyllaDB Metrics
- Elasticsearch Metrics

---

# Alert Examples

Alerts can be configured for:

- High CPU usage
- High memory usage
- Disk space exhaustion
- Container restart loops
- Application downtime
- Database unavailable
- API latency
- HTTP 5xx responses

---

# Deployment Order

Monitoring services start in the following order:

```
Prometheus

↓

Alertmanager

↓

Loki

↓

Tempo

↓

OpenTelemetry Collector

↓

Grafana
```

---

# Future Kubernetes Deployment

The same monitoring architecture can be deployed on Kubernetes using:

- Prometheus Operator
- Grafana Helm Chart
- Loki Helm Chart
- Tempo Helm Chart
- OpenTelemetry Operator

No major architectural changes are required.

---

# Best Practices

The OTMS monitoring implementation follows these practices:

- Dedicated observability network
- Persistent storage for metrics and dashboards
- Separate monitoring stack from application stack
- Health checks for monitoring services
- Configuration through mounted files
- Dashboards provisioned automatically
- Alert rules stored in version control

---

# Lessons Learned

While integrating monitoring into OTMS, the following concepts were explored:

- Time-series databases
- Metrics scraping
- Dashboard provisioning
- Log aggregation
- Distributed tracing
- Telemetry pipelines
- Container monitoring
- Infrastructure monitoring
- Alert routing

---

# Summary

The OT-Micro-Docker monitoring stack provides complete observability for the platform by combining Prometheus, Grafana, Loki, Tempo, OpenTelemetry Collector, Alertmanager, Node Exporter, and cAdvisor.

Together, these components enable infrastructure monitoring, application metrics, centralized logging, distributed tracing, and proactive alerting, preparing the OTMS platform for production-grade deployments on Docker Compose, Kubernetes, and Amazon EKS.
