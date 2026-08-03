# 01 - Project Overview

---

# OT-Micro-Docker

## Project Overview

---

# Introduction

OT-Micro-Docker is a complete microservices-based application designed to demonstrate modern containerization, orchestration, and DevOps practices.

Unlike a traditional monolithic application, this project separates business functionality into independent services. Each service is containerized, independently deployable, and communicates using REST APIs.

The project was originally designed as a learning initiative to understand Docker and Docker Compose in depth. It has gradually evolved into a production-inspired platform that demonstrates containerized microservices, multiple databases, asynchronous processing, search indexing, monitoring, and cloud-native deployment.

---

# Project Objectives

The primary objectives of this project are:

- Learn Docker fundamentals through a real-world application.
- Containerize applications written in multiple programming languages.
- Build reusable Docker images.
- Deploy a complete application stack using Docker Compose.
- Implement service-to-service communication.
- Integrate multiple database technologies.
- Publish application images to Docker Hub.
- Build a self-contained deployment that can run on any Docker host.
- Prepare the application for Kubernetes and Amazon EKS deployment.
- Integrate monitoring, logging, and distributed tracing.

---

# Business Scenario

The project simulates an Employee Management System.

Organizations typically maintain employee records across multiple departments. Instead of storing every function inside one application, responsibilities are divided into multiple independent services.

The system provides functionality for:

- Employee registration
- Attendance management
- Salary management
- Salary notification through email
- Search and indexing
- Data synchronization
- Reporting

---

# High-Level Architecture

```
                           User
                             │
                             ▼
                    React Frontend (NGINX)
                             │
     ┌───────────────────────┼────────────────────────┐
     │                       │                        │
     ▼                       ▼                        ▼
Employee API          Attendance API           Salary API
     │                       │                        │
     │                       │                        │
     ▼                       ▼                        ▼
 ScyllaDB              PostgreSQL              ScyllaDB
     │                                                │
     └──────────────────────────────┐                 │
                                    ▼                 │
                              Scylla Sync             │
                                    │                 │
                                    ▼                 │
                             Elasticsearch ◄──────────┘
                                    │
                                    ▼
                           Notification API
                                    │
                                    ▼
                              SMTP (Gmail)

```

---

# Technology Stack

| Layer | Technology |
|---------|------------|
| Frontend | React |
| Web Server | NGINX |
| Employee Service | Golang |
| Attendance Service | Python Flask |
| Salary Service | Spring Boot |
| Notification Service | Python Flask |
| Background Worker | Python |
| Employee Database | ScyllaDB |
| Salary Database | ScyllaDB |
| Attendance Database | PostgreSQL |
| Cache | Redis |
| Search Engine | Elasticsearch |
| Container Runtime | Docker |
| Container Orchestration | Docker Compose |
| Image Registry | Docker Hub |
| Monitoring *(Planned)* | Prometheus |
| Visualization *(Planned)* | Grafana |
| Logging *(Planned)* | Loki |
| Distributed Tracing *(Planned)* | Tempo |
| Telemetry *(Planned)* | OpenTelemetry |
| Container Orchestration *(Future)* | Kubernetes |
| Cloud Platform *(Future)* | Amazon EKS |

---

# Why Multiple Programming Languages?

The project intentionally uses different programming languages to simulate a real enterprise environment.

| Service | Language | Reason |
|----------|----------|--------|
| Employee API | Go | High performance REST API |
| Attendance API | Python | Lightweight development |
| Salary API | Java Spring Boot | Enterprise application |
| Notification API | Python | Email processing |
| Frontend | React | Modern UI |

This demonstrates that Docker can package applications regardless of their implementation language.

---

# Why Multiple Databases?

Different workloads require different database technologies.

## ScyllaDB

Used for:

- Employee records
- Salary records

Reason:

- High write throughput
- Horizontal scalability
- Cassandra-compatible architecture

---

## PostgreSQL

Used for:

- Attendance records

Reason:

- Relational data model
- ACID compliance
- SQL support

---

## Redis

Used for:

- Frequently accessed data
- Performance optimization
- Temporary storage

---

## Elasticsearch

Used for:

- Search
- Notification indexing
- Fast retrieval of salary records

---

# Key Design Principles

The project follows several architectural principles.

## Microservices

Each service has:

- Independent codebase
- Independent container
- Independent lifecycle

---

## Stateless Services

Application containers do not store persistent data locally.

Persistent data resides inside dedicated database containers.

---

## Container Isolation

Each service runs in its own container.

This provides:

- Fault isolation
- Easy upgrades
- Independent scaling
- Simplified debugging

---

## Environment-Based Configuration

Application configuration is provided using environment variables.

Examples include:

- Database host
- Database port
- SMTP credentials
- Elasticsearch endpoint
- Redis host

This removes hardcoded configuration from application source code.

---

# Communication Flow

The application follows a request-response model.

```
Browser
   │
   ▼
Frontend
   │
   ├────────────► Employee API
   │                  │
   │                  ▼
   │              ScyllaDB
   │
   ├────────────► Attendance API
   │                  │
   │                  ▼
   │             PostgreSQL
   │
   └────────────► Salary API
                      │
                      ▼
                  ScyllaDB
                      │
                      ▼
                Scylla Sync
                      │
                      ▼
                Elasticsearch
                      │
                      ▼
              Notification API
                      │
                      ▼
                  Gmail SMTP
```

---

# Deployment Strategy

The complete platform is deployed using Docker Compose.

The deployment consists of two logical groups.

## Infrastructure

- PostgreSQL
- Redis
- ScyllaDB
- Elasticsearch

---

## Application

- Employee API
- Attendance API
- Salary API
- Notification API
- Frontend
- Scylla Sync
- Migration containers

---

# Image Distribution

All project-specific images are published to Docker Hub under:

```
478mkharb/
```

This allows the complete application stack to be deployed without building source code.

Example:

```
478mkharb/otms-employee-api
478mkharb/otms-attendance-api
478mkharb/otms-salary-api
478mkharb/otms-notification-api
478mkharb/otms-frontend
478mkharb/otms-postgres
478mkharb/otms-redis
478mkharb/otms-scylladb
478mkharb/otms-elasticsearch
```

---

# Current Project Status

## Completed

- Dockerized all services
- Docker Compose deployment
- Docker Hub publishing
- Database initialization
- Migration automation
- SMTP integration
- Elasticsearch integration
- Health checks
- Swagger support

---

## Current Phase

Implementation of complete observability.

The monitoring stack will include:

- Prometheus
- Grafana
- Node Exporter
- cAdvisor

---

## Future Roadmap

Future enhancements include:

- Loki
- Promtail
- Tempo
- OpenTelemetry
- Kubernetes
- Minikube
- Amazon EKS
- Helm
- ArgoCD
- GitHub Actions
- Production CI/CD pipeline

---

# Summary

OT-Micro-Docker is a complete end-to-end microservices platform that demonstrates containerization, service orchestration, multiple database technologies, asynchronous processing, Docker Hub image management, and cloud-native deployment readiness.

The project serves as both a learning platform and a production-inspired reference implementation for modern DevOps practices.
