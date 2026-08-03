# 08 - Microservices

---

# Microservices

---

# Introduction

The OT-Micro-Docker platform is composed of multiple independent microservices.

Each microservice is responsible for a single business capability and follows the principle of **Single Responsibility**.

Each service:

- Has its own source code
- Has its own Docker image
- Has its own runtime
- Can be deployed independently
- Communicates using REST APIs
- Uses environment variables for configuration

---

# Complete Microservice Architecture

```

                       React Frontend
                              │
      ┌───────────────────────┼──────────────────────┐
      │                       │                      │
      ▼                       ▼                      ▼

 Employee API          Attendance API         Salary API
      │                       │                     │
      ▼                       ▼                     ▼

  ScyllaDB              PostgreSQL           ScyllaDB
      │                                             │
      └──────────────────────┐                      │
                             ▼                      │

                      Scylla Sync                   │
                             │                      │
                             ▼                      │

                     Elasticsearch ◄───────────────┘
                             │
                             ▼

                    Notification API
                             │
                             ▼

                        Gmail SMTP

```

---

# Microservices Overview

| Service | Language | Port | Database |
|-----------|----------|------|----------|
| Employee API | Go | 8080 | ScyllaDB |
| Attendance API | Python | 8081 | PostgreSQL |
| Salary API | Spring Boot | 8082 | ScyllaDB |
| Notification API | Python | 8085 | Elasticsearch |
| Scylla Sync | Python | Background | ScyllaDB + Elasticsearch |
| Frontend | React | 3000 | None |

---

# Employee API

---

## Purpose

Employee API manages employee information.

Responsibilities

- Create Employee
- Update Employee
- Delete Employee
- Retrieve Employee
- Health Check

---

## Technology

```
Golang

Gin Framework
```

---

## Docker Image

```
478mkharb/otms-employee-api
```

---

## Container

```
employee-api
```

---

## Port

```
8080
```

---

## Dependencies

```
ScyllaDB

↓

Redis
```

---

## Environment Variables

```
SCYLLA_HOST

SCYLLA_PORT

SCYLLA_KEYSPACE

REDIS_HOST

REDIS_PORT
```

---

## Health Endpoint

```
GET

/api/v1/employee/health
```

---

## Swagger

```
http://localhost:8080/swagger/index.html
```

---

## Request Flow

```
Browser

↓

Frontend

↓

Employee API

↓

ScyllaDB

↓

Response
```

---

## Database

```
employee_info
```

---

## Startup Dependency

```
Scylla Migration

↓

Employee API
```

---

# Attendance API

---

## Purpose

Attendance API manages employee attendance.

Responsibilities

- Mark Attendance
- Retrieve Attendance
- Attendance History

---

## Technology

```
Python Flask
```

---

## Docker Image

```
478mkharb/otms-attendance-api
```

---

## Container

```
attendance-api
```

---

## Port

```
8081
```

---

## Dependencies

```
PostgreSQL

↓

Redis
```

---

## Environment Variables

```
POSTGRES_HOST

POSTGRES_DB

POSTGRES_USER

POSTGRES_PASSWORD

REDIS_HOST

REDIS_PORT
```

---

## Health Endpoint

```
GET

/api/v1/attendance/health
```

---

## Swagger

```
http://localhost:8081/apidocs
```

---

## Database

```
attendance_db

↓

records
```

---

## Request Flow

```
Frontend

↓

Attendance API

↓

PostgreSQL

↓

Response
```

---

# Salary API

---

## Purpose

Salary API manages employee salary records.

Responsibilities

- Create Salary
- Update Salary
- Retrieve Salary

---

## Technology

```
Spring Boot
```

---

## Docker Image

```
478mkharb/otms-salary-api
```

---

## Container

```
salary-api
```

---

## Port

```
8082
```

---

## Dependencies

```
ScyllaDB

↓

Redis
```

---

## Environment Variables

```
SCYLLA_HOST

SCYLLA_PORT

SCYLLA_KEYSPACE

REDIS_HOST
```

---

## Health Endpoint

```
GET

/actuator/health
```

---

## Swagger

```
http://localhost:8082/swagger-ui/index.html
```

---

## Database

```
employee_salary
```

---

## Request Flow

```
Frontend

↓

Salary API

↓

ScyllaDB

↓

Scylla Sync
```

---

# Notification API

---

## Purpose

Notification API sends salary notifications to employees.

Responsibilities

- Read Elasticsearch
- Generate Email
- Send SMTP Mail
- Health Check

---

## Technology

```
Python Flask
```

---

## Docker Image

```
478mkharb/otms-notification-api
```

---

## Container

```
notification-api
```

---

## Port

```
8085
```

---

## Dependencies

```
Elasticsearch

↓

SMTP Server
```

---

## Environment Variables

```
SMTP_USERNAME

SMTP_PASSWORD

SMTP_SERVER

SMTP_PORT

ELASTIC_HOST

ELASTIC_INDEX
```

---

## Health Endpoint

```
GET

/api/v1/notification/health
```

---

## Swagger

```
http://localhost:8085/apidocs
```

---

## Request Flow

```
Scylla Sync

↓

Notification API

↓

SMTP

↓

Employee Mailbox
```

---

# Scylla Sync

---

## Purpose

Scylla Sync synchronizes salary records into Elasticsearch.

---

## Responsibilities

- Read ScyllaDB
- Detect Changes
- Index Elasticsearch
- Trigger Notification API

---

## Docker Image

```
478mkharb/otms-scylla-sync
```

---

## Container

```
scylla-sync
```

---

## Port

No exposed port.

Runs as a background worker.

---

## Dependencies

```
ScyllaDB

↓

Elasticsearch

↓

Notification API
```

---

## Synchronization Flow

```
ScyllaDB

↓

Read Records

↓

Transform

↓

Elasticsearch

↓

Notification API
```

---

# Frontend

---

## Purpose

Provides the web interface for the complete platform.

---

## Technology

```
React

NGINX
```

---

## Docker Image

```
478mkharb/otms-frontend
```

---

## Container

```
frontend
```

---

## Port

```
3000
```

---

## Responsibilities

- Employee UI
- Attendance UI
- Salary UI
- Notification UI
- API Communication

---

## Dependencies

```
Employee API

Attendance API

Salary API

Notification API
```

---

# Service Communication Matrix

| Source | Destination | Purpose |
|----------|-------------|----------|
| Frontend | Employee API | Employee Operations |
| Frontend | Attendance API | Attendance |
| Frontend | Salary API | Salary |
| Employee API | ScyllaDB | Employee Data |
| Attendance API | PostgreSQL | Attendance Data |
| Salary API | ScyllaDB | Salary Data |
| Scylla Sync | Elasticsearch | Indexing |
| Scylla Sync | Notification API | Trigger Email |
| Notification API | SMTP | Send Email |

---

# Startup Order

```
ScyllaDB

↓

Scylla Init

↓

Scylla Migration

↓

Employee API

↓

Salary API
```

---

```
PostgreSQL

↓

Attendance Migration

↓

Attendance API
```

---

```
Elasticsearch

↓

Notification API

↓

Scylla Sync
```

---

```
Frontend
```

---

# Health Endpoints

| Service | Endpoint |
|----------|----------|
| Employee API | `/api/v1/employee/health` |
| Attendance API | `/api/v1/attendance/health` |
| Salary API | `/actuator/health` |
| Notification API | `/api/v1/notification/health` |

---

# Swagger Endpoints

| Service | URL |
|----------|-----|
| Employee API | `http://localhost:8080/swagger/index.html` |
| Attendance API | `http://localhost:8081/apidocs` |
| Salary API | `http://localhost:8082/swagger-ui/index.html` |
| Notification API | `http://localhost:8085/apidocs` |

---

# Design Principles

The OTMS microservices follow these architectural principles:

- One business capability per service
- Independent deployment
- Independent Docker image
- Stateless application containers
- Database-per-service responsibility
- Environment-based configuration
- RESTful communication
- Health-aware startup
- Docker-first deployment
- Kubernetes-ready design

---

# Future Enhancements

The microservices are designed to support future enhancements such as:

- JWT authentication
- API Gateway
- Service discovery
- Distributed tracing
- Circuit breakers
- Rate limiting
- Kubernetes deployment
- Horizontal Pod Autoscaling (HPA)
- Helm charts

---

# Summary

The OT-Micro-Docker platform consists of independent microservices that communicate over REST APIs and leverage specialized databases for their respective workloads. Each service is containerized, independently deployable, and configured through environment variables, making the platform portable across Docker Compose, Kubernetes, and Amazon EKS.

This modular architecture simplifies development, testing, deployment, and future scalability while serving as a practical demonstration of modern microservices and DevOps practices.
