# OT-Micro-Docker

> **Dockerized OT Microservices Platform with Complete DevOps Lifecycle**

---

# Overview

OT-Micro-Docker is a production-inspired microservices application designed to demonstrate modern DevOps practices using Docker, Docker Compose, Docker Hub, Monitoring, Kubernetes, and AWS.

The project contains multiple microservices written in different programming languages and backed by multiple databases. Every component is containerized and orchestrated using Docker Compose. The long-term roadmap includes deployment to Kubernetes (Minikube and Amazon EKS) together with a complete observability stack.

---

# Technology Stack

| Category | Technology |
|----------|------------|
| Frontend | React + NGINX |
| Employee API | Golang |
| Attendance API | Python Flask |
| Salary API | Spring Boot |
| Notification API | Python Flask |
| Background Worker | Python |
| PostgreSQL | Attendance Database |
| ScyllaDB | Employee & Salary Database |
| Redis | Cache |
| Elasticsearch | Search / Notification |
| Docker | Containerization |
| Docker Compose | Local Orchestration |
| Docker Hub | Image Registry |
| Prometheus | Monitoring *(Planned)* |
| Grafana | Visualization *(Planned)* |
| Loki | Logging *(Planned)* |
| Tempo | Distributed Tracing *(Planned)* |
| OpenTelemetry | Observability *(Planned)* |
| Kubernetes | Deployment *(Planned)* |
| Amazon EKS | Cloud Deployment *(Planned)* |

---

# Project Features

- Polyglot Microservices Architecture
- Multi-stage Docker Builds
- Docker Compose Based Deployment
- Independent Database Containers
- Health Checks
- Migration Containers
- Docker Hub Hosted Images
- Self-contained Deployment
- Swagger Documentation
- Persistent Storage
- Environment Variable Based Configuration

---

# Current Project Status

## Completed

- Dockerized all microservices
- Dockerized all supporting databases
- Docker Hub image publishing
- Docker Compose deployment
- ScyllaDB initialization
- PostgreSQL migrations
- Attendance migration
- Salary migration
- Notification email integration
- Elasticsearch integration
- Redis integration
- Complete deployment SOP
- Health check implementation

---

## In Progress

- Monitoring Stack
  - Prometheus
  - Grafana
  - Node Exporter
  - cAdvisor

---

## Planned

- Loki
- Tempo
- OpenTelemetry
- Alertmanager
- Minikube
- Kubernetes
- Helm
- Amazon EKS
- GitHub Actions
- ArgoCD

---

# Documentation Index

| File | Description |
|------|-------------|
| 01-Project-Overview.md | Complete project overview |
| 02-Architecture.md | System architecture |
| 03-Repository-Structure.md | Folder structure explanation |
| 04-Docker.md | Docker implementation |
| 05-Docker-Compose.md | Compose configuration |
| 06-DockerHub.md | Docker Hub images |
| 07-Databases.md | Database architecture |
| 08-Microservices.md | Service documentation |
| 09-Troubleshooting.md | Issues and fixes |
| 10-Deployment-SOP.md | Deployment guide |
| 11-Monitoring.md | Monitoring implementation |
| 12-Kubernetes.md | Kubernetes migration |
| 13-EKS.md | AWS deployment |
| 14-Future-Roadmap.md | Future enhancements |
| 15-Interview-Questions.md | Frequently asked interview questions |

---

# Deployment

The project is deployed using Docker Compose.

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
up -d
```

---

# Author

Mukesh Kharb

DevOps Engineer

---

# License

For educational and learning purposes.
