# 03 - Repository Structure

---

# Repository Structure

---

# Introduction

The OT-Micro-Docker repository is organized to provide a clear separation between application source code, infrastructure components, migration utilities, configuration, and documentation.

Every major component of the application resides in its own directory, making the project modular, maintainable, and scalable.

---

# Repository Layout

```

OT-Micro-Docker/
│
├── Attendance_API/
├── Employee_API/
├── Salary_API/
├── Notification/
├── Frontend/
│
├── attendance-migration/
├── scylla-init/
├── scylla-migration/
├── Scylla_Sync/
│
├── docker-compose.yml
├── docker-compose.database.yml
├── README.md
│
├── Monitoring/                (Planned)
│
└── docs/                      (Planned)

```

---

# Repository Overview

The repository can be divided into five logical sections.

| Section | Purpose |
|----------|---------|
| Application Services | Business logic |
| Database Utilities | Database initialization and migrations |
| Docker Configuration | Docker Compose deployment |
| Monitoring *(Future)* | Observability stack |
| Documentation | Project documentation |

---

# Application Services

---

# Employee_API/

```

Employee_API/
│
├── cmd/
├── config/
├── database/
├── docs/
├── handler/
├── middleware/
├── models/
├── routes/
├── service/
├── Dockerfile
├── go.mod
└── main.go

```

Purpose

- Employee Management
- Employee CRUD
- Employee search
- Redis integration
- ScyllaDB integration

Technology

- Golang
- Gin Framework

Container

```
employee-api

```

Port

```
8080

```

---

# Attendance_API/

```

Attendance_API/
│
├── client/
├── config/
├── migration/
├── router/
├── swagger/
├── Dockerfile
├── requirements.txt
└── app.py

```

Purpose

- Attendance Management
- Attendance CRUD
- PostgreSQL integration
- Redis caching

Technology

- Python Flask

Container

```
attendance-api

```

Port

```
8081

```

---

# Salary_API/

```

Salary_API/
│
├── src/
├── resources/
├── Dockerfile
├── pom.xml
└── mvnw

```

Purpose

- Salary Management

Technology

- Spring Boot

Container

```
salary-api

```

Port

```
8082

```

---

# Notification/

```

Notification/
│
├── templates/
├── config/
├── Dockerfile
├── requirements.txt
├── notification_api.py
└── entrypoint.sh

```

Purpose

- Send Email Notifications
- SMTP Integration
- Elasticsearch Query
- PDF Attachment Support

Technology

- Python Flask

Container

```
notification-api

```

Port

```
8085

```

---

# Frontend/

```

Frontend/
│
├── src/
├── public/
├── nginx.conf
├── Dockerfile
├── package.json
└── package-lock.json

```

Purpose

- User Interface
- API Communication

Technology

- React
- NGINX

Container

```
frontend

```

Port

```
3000

```

---

# Database Utility Containers

These containers execute only once during deployment.

---

# attendance-migration/

Purpose

Initialize PostgreSQL schema using Liquibase.

Structure

```

attendance-migration/
│
├── Dockerfile
└── entrypoint.sh

```

Responsibilities

- Wait for PostgreSQL
- Execute Liquibase
- Create Attendance tables

Container

```
attendance-migration

```

Lifecycle

```
Runs Once

↓

Exits Successfully

```

---

# scylla-init/

Purpose

Initialize ScyllaDB cluster.

Responsibilities

- Wait for ScyllaDB
- Create Keyspace

Container

```
scylla-init

```

Lifecycle

```
Runs Once

↓

Exits

```

---

# scylla-migration/

Purpose

Create ScyllaDB schema.

Responsibilities

- Create Employee tables
- Create Salary tables

Container

```
scylla-migration

```

Lifecycle

```
Runs Once

↓

Exits

```

---

# Scylla_Sync/

Purpose

Synchronize salary records between ScyllaDB and Elasticsearch.

Responsibilities

- Read Salary Records
- Detect Changes
- Update Elasticsearch
- Trigger Notification API

Container

```
scylla-sync

```

Runs Continuously

---

# Docker Compose Files

---

# docker-compose.database.yml

Contains infrastructure services only.

Responsibilities

- PostgreSQL
- Redis
- ScyllaDB
- Elasticsearch

No application containers exist in this file.

---

# docker-compose.yml

Contains application containers.

Responsibilities

- Frontend
- Employee API
- Attendance API
- Salary API
- Notification API
- Migration Containers
- Scylla Sync

---

# Why Two Compose Files?

Infrastructure changes less frequently than applications.

Separating them provides:

- Cleaner organization
- Faster maintenance
- Independent updates
- Better readability

---

# Monitoring Directory *(Planned)*

Future structure

```

Monitoring/
│
├── prometheus/
├── grafana/
├── loki/
├── tempo/
├── otel-collector/
├── alertmanager/
└── docker-compose.monitoring.yml

```

Responsibilities

- Metrics
- Dashboards
- Logging
- Tracing
- Alerts

---

# Documentation Directory *(Planned)*

```

docs/
│
├── README.md
├── 01-Project-Overview.md
├── 02-Architecture.md
├── 03-Repository-Structure.md
├── 04-Docker.md
├── 05-Docker-Compose.md
├── 06-DockerHub.md
├── 07-Databases.md
├── 08-Microservices.md
├── 09-Troubleshooting.md
├── 10-Deployment-SOP.md
├── 11-Monitoring.md
├── 12-Kubernetes.md
├── 13-EKS.md
├── 14-Future-Roadmap.md
└── 15-Interview-Questions.md

```

---

# Dockerfiles

Each deployable service owns its own Dockerfile.

| Directory | Dockerfile |
|------------|------------|
| Employee_API | Yes |
| Attendance_API | Yes |
| Salary_API | Yes |
| Notification | Yes |
| Frontend | Yes |
| attendance-migration | Yes |
| scylla-init | Yes |
| scylla-migration | Yes |
| Scylla_Sync | Yes |

This ensures every service can be built independently.

---

# Repository Design Principles

The repository follows these principles:

## Service Isolation

Each service has:

- Independent source code
- Independent Dockerfile
- Independent dependencies

---

## Infrastructure Separation

Infrastructure is separated from business services.

Examples

- PostgreSQL
- Redis
- Elasticsearch
- ScyllaDB

---

## Migration Separation

Database initialization is isolated from application startup.

Benefits

- Faster debugging
- Easier maintenance
- Repeatable deployments

---

## Documentation First

Every major component is documented.

This improves onboarding for new developers.

---

## Future Ready

The repository structure has been designed to support future migration to:

- Kubernetes
- Amazon EKS
- Helm
- GitHub Actions
- ArgoCD

without major restructuring.

---

# Summary

The OT-Micro-Docker repository follows a modular organization where each business capability, infrastructure component, migration utility, and future enhancement resides in its own dedicated directory.

This separation simplifies development, testing, deployment, and long-term maintenance while preparing the project for production-grade container orchestration.
