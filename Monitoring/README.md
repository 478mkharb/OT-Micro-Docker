# OTMS Monitoring Stack

This directory contains the monitoring and alerting stack for OTMS using **Prometheus**, **Grafana**, and **Alertmanager**.

## Architecture

```text
                OTMS Microservices
                       │
       ┌───────────────┼────────────────┐
       │               │                │
  Node Exporter   DB Exporters   App Metrics
       │               │                │
       └───────────────┼────────────────┘
                       │
                  Prometheus
                       │
         ┌─────────────┴─────────────┐
         │                           │
     Grafana                  Alertmanager
         │                           │
   Dashboards                 Gmail Alerts
```

## Start OTMS Application

```bash
docker compose -f docker-compose.yml up -d
```

## Start Monitoring Stack

```bash
docker compose -f Monitoring/docker-compose.yml up -d
```

## Verify Running Containers

```bash
docker ps
```

## Access

| Component | URL |
|-----------|-----|
| Grafana | http://localhost:3001 |
| Prometheus | http://localhost:9090 |
| Alertmanager | http://localhost:9093 |

## Volumes

### OTMS Application

```text
postgres-data
redis-data
scylladb-data
elasticsearch-data
```

### Monitoring

```text
prometheus-data
grafana-data
```
## View Logs

### Monitoring Stack

```bash
# Prometheus
docker compose -f Monitoring/docker-compose.yml logs -f prometheus

# Grafana
docker compose -f Monitoring/docker-compose.yml logs -f grafana

# Alertmanager
docker compose -f Monitoring/docker-compose.yml logs -f alertmanager

# Node Exporter
docker compose -f Monitoring/docker-compose.yml logs -f node-exporter
```

### OTMS Application

```bash
# View logs for all services
docker compose -f docker-compose.yml logs -f

# Individual services
docker compose -f docker-compose.yml logs -f frontend
docker compose -f docker-compose.yml logs -f employee-api
docker compose -f docker-compose.yml logs -f attendance-api
docker compose -f docker-compose.yml logs -f salary-api
docker compose -f docker-compose.yml logs -f notification-api
docker compose -f docker-compose.yml logs -f redis
docker compose -f docker-compose.yml logs -f postgres
docker compose -f docker-compose.yml logs -f scylladb
docker compose -f docker-compose.yml logs -f elasticsearch
```
## Stop Services

### Stop Monitoring

```bash
docker compose -f Monitoring/docker-compose.yml down
```

### Stop OTMS Application

```bash
docker compose -f docker-compose.yml down
```

## Remove Containers & Volumes

### Remove Monitoring Stack

```bash
docker compose -f Monitoring/docker-compose.yml down -v
```

### Remove OTMS Application

```bash
docker compose -f docker-compose.yml down -v
```

### Remove Everything

```bash
docker compose -f docker-compose.yml down -v
docker compose -f Monitoring/docker-compose.yml down -v

docker volume prune -f
```

> **Note:** Grafana dashboards, Prometheus datasource, and Prometheus alert rules are automatically provisioned during startup. No manual configuration is required.