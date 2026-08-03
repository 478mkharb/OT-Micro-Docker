# 05 - Docker Compose

---

# Docker Compose

---

# Introduction

Docker Compose is used to deploy the complete OT-Micro-Docker platform using a single command.

Instead of manually creating networks, containers, volumes, and environment variables for each service, Docker Compose defines the entire application stack declaratively.

A single command creates the complete environment.

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
up -d
```

---

# Why Docker Compose?

Without Docker Compose every container must be started manually.

Example

```
docker run postgres

docker run redis

docker run scylladb

docker run elasticsearch

docker run employee-api

docker run attendance-api

docker run salary-api

docker run notification-api

docker run frontend
```

Every command requires

- Ports
- Volumes
- Networks
- Environment variables
- Dependencies

Managing dozens of commands quickly becomes difficult.

Docker Compose solves this problem by describing the complete deployment in YAML.

---

# Compose Architecture

The project uses two compose files.

```
docker-compose.database.yml

↓

Infrastructure
```

```
docker-compose.yml

↓

Applications
```

---

# Why Two Compose Files?

Infrastructure services change less frequently than application services.

Separating them provides

- Better readability
- Easier maintenance
- Independent updates
- Cleaner architecture

---

# Infrastructure Compose

The database compose file contains only infrastructure services.

```
PostgreSQL

Redis

ScyllaDB

Elasticsearch
```

Responsibilities

- Persistent storage
- Database networking
- Volume management

Applications are intentionally excluded.

---

# Application Compose

The application compose file contains

```
Employee API

Attendance API

Salary API

Notification API

Frontend

Scylla Sync

Attendance Migration

Scylla Init

Scylla Migration
```

---

# Compose File Structure

A typical compose file consists of

```
services

networks

volumes

secrets (optional)

configs (optional)
```

---

# Services

Every Docker container is represented as a service.

Example

```yaml
services:

  employee-api:
```

Each service describes

- Image
- Container name
- Ports
- Environment variables
- Networks
- Health checks
- Dependencies
- Restart policy

---

# Images

Initially the project used

```yaml
build:
  context: ./Employee_API
```

After publishing images to Docker Hub it became

```yaml
image: 478mkharb/otms-employee-api:latest
```

Advantages

- Faster deployment
- No source compilation
- No Docker build
- Production-like workflow

---

# Container Names

Every service has an explicit container name.

Example

```yaml
container_name: employee-api
```

Benefits

- Easy troubleshooting

```
docker logs employee-api
```

```
docker exec -it employee-api sh
```

instead of random generated names.

---

# Port Mapping

Compose exposes container ports to the host.

Example

```yaml
ports:

- "8080:8080"
```

Meaning

```
Host

8080

↓

Container

8080
```

---

# Environment Variables

Applications are configured through environment variables.

Example

```yaml
environment:

SCYLLA_HOST=scylladb

REDIS_HOST=redis
```

Benefits

- Environment independent
- No hardcoded IPs
- Reusable images

---

# Networks

All services join

```yaml
otms-network
```

Communication

```
employee-api

↓

redis
```

instead of

```
localhost
```

Docker automatically resolves service names.

---

# Docker DNS

Compose creates an internal DNS.

Examples

```
postgres

redis

scylladb

elasticsearch
```

Applications communicate using service names rather than IP addresses.

---

# Volumes

Persistent databases use Docker volumes.

```yaml
volumes:

postgres-data
```

Purpose

```
Container Deleted

↓

Data Preserved
```

---

# Restart Policies

Application services

```yaml
restart: unless-stopped
```

Migration containers

```yaml
restart: "no"
```

Reason

Migration containers execute once and terminate successfully.

---

# Health Checks

Every important service exposes a health endpoint.

Example

```yaml
healthcheck:

test:
```

Purpose

Verify that the application is actually ready before dependent services start.

---

# depends_on

Compose controls startup dependencies.

Example

```yaml
depends_on:

postgres:
  condition: service_healthy
```

Attendance API starts only after PostgreSQL becomes healthy.

---

# Startup Sequence

Database services start first.

```
PostgreSQL

Redis

ScyllaDB

Elasticsearch
```

↓

Migration Containers

```
Attendance Migration

Scylla Init

Scylla Migration
```

↓

Business Services

```
Employee API

Attendance API

Salary API

Notification API
```

↓

Background Worker

```
Scylla Sync
```

↓

Frontend

```
React
```

---

# Why Frontend Starts Last?

Frontend communicates with every API.

If APIs are unavailable

```
Browser

↓

404

↓

Connection Refused
```

Waiting for healthy APIs prevents startup errors.

---

# Database Dependencies

Employee API

↓

ScyllaDB

Attendance API

↓

PostgreSQL

Salary API

↓

ScyllaDB

Notification API

↓

Elasticsearch

---

# Migration Pattern

Instead of

```
Application

↓

Create Tables

↓

Start API
```

the project uses

```
Migration Container

↓

Initialize Database

↓

Exit

↓

Application Starts
```

Benefits

- Cleaner application code
- Independent migrations
- Easier rollback
- Easier debugging

---

# Compose Networking

```
             otms-network

Employee API

Attendance API

Salary API

Notification API

Frontend

Redis

PostgreSQL

ScyllaDB

Elasticsearch

Scylla Sync
```

Every service communicates over the same bridge network.

---

# Docker Hub Integration

Compose no longer builds images.

Instead

```yaml
image:

478mkharb/otms-employee-api:latest
```

Docker automatically

```
Pull Image

↓

Create Container

↓

Start Service
```

---

# Deployment Workflow

## First Deployment

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
up -d
```

Docker automatically downloads missing images.

---

## View Containers

```bash
docker ps
```

---

## View Logs

```bash
docker logs employee-api
```

---

## Stop Stack

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
down
```

---

## Remove Volumes

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
down -v
```

---

# Design Decisions

The following architectural decisions were intentionally made.

## Separate Infrastructure

Infrastructure services are isolated from business services.

---

## Health-aware Startup

Applications wait for dependencies before starting.

---

## Migration Containers

Schema creation is isolated from application startup.

---

## Environment Variables

No configuration is hardcoded into images.

---

## Docker Hub Images

Deployments no longer require source code compilation.

---

## Persistent Volumes

Database data survives container recreation.

---

# Future Enhancements

The Compose architecture has been designed to accommodate additional services without restructuring.

Planned additions include

```
Prometheus

Grafana

Node Exporter

cAdvisor

Loki

Promtail

Tempo

OpenTelemetry

Alertmanager
```

A future monitoring compose file will be added.

```
docker-compose.monitoring.yml
```

This keeps observability independent from the application stack.

---

# Summary

Docker Compose provides the orchestration layer for OT-Micro-Docker.

It manages

- Container lifecycle
- Networking
- Volumes
- Health checks
- Startup order
- Environment variables
- Restart policies

By separating infrastructure and application services into dedicated compose files, the project achieves a modular, maintainable, and production-inspired deployment model that is ready for future migration to Kubernetes and Amazon EKS.
