# 02 - System Architecture

---

# System Architecture

---

# Introduction

The OT-Micro-Docker platform follows a distributed microservices architecture where every business capability is implemented as an independent service.

Each service executes inside its own Docker container and communicates with other services using REST APIs over a private Docker bridge network.

The architecture is designed to be modular, scalable, and cloud-ready.

---

# High-Level Architecture

```
                                      User
                                        │
                                        │ HTTP
                                        ▼
                          +-----------------------------+
                          |        React Frontend       |
                          |         (NGINX)             |
                          +-------------+---------------+
                                        │
                                        │ REST API
         ┌──────────────────────────────┼───────────────────────────────┐
         │                              │                               │
         ▼                              ▼                               ▼

+------------------+         +-------------------+         +------------------+
| Employee API     |         | Attendance API    |         | Salary API       |
| Golang           |         | Python Flask      |         | Spring Boot      |
+---------+--------+         +---------+---------+         +---------+--------+
          │                            │                             │
          │                            │                             │
          ▼                            ▼                             ▼

    +-----------+               +-------------+               +-------------+
    | ScyllaDB  |               | PostgreSQL  |               | ScyllaDB    |
    +-----------+               +-------------+               +-------------+

          │                                                     │
          │                                                     │
          └──────────────────────────────┐                      │
                                         ▼                      │

                              +--------------------+
                              |   Scylla Sync      |
                              +----------+---------+
                                         │
                                         ▼

                              +--------------------+
                              | Elasticsearch      |
                              +----------+---------+
                                         │
                                         ▼

                              +--------------------+
                              | Notification API   |
                              +----------+---------+
                                         │
                                         ▼

                                   Gmail SMTP Server
```

---

# Deployment Architecture

```
Docker Host
│
├── Docker Network (otms-network)
│
├── PostgreSQL
├── Redis
├── ScyllaDB
├── Elasticsearch
│
├── Employee API
├── Attendance API
├── Salary API
├── Notification API
├── Scylla Sync
├── Frontend
│
├── Attendance Migration
├── Scylla Init
└── Scylla Migration
```

Every service communicates using the internal Docker network instead of localhost.

---

# Docker Network

The project uses a dedicated bridge network.

```
Network Name

otms-network
```

Every container joins this network.

Example:

```
employee-api
      │
      ▼
redis
```

instead of

```
localhost
```

Docker DNS automatically resolves service names.

Examples:

```
postgres

redis

scylladb

elasticsearch

notification-api
```

---

# Why Docker DNS?

Instead of remembering IP addresses,

```
172.18.0.3

172.18.0.5

172.18.0.9
```

Docker automatically maps

```
postgres

redis

scylladb
```

to their respective container IPs.

Therefore applications never need hardcoded IP addresses.

---

# Request Flow

## Employee Creation

```
Browser

↓

Frontend

↓

Employee API

↓

ScyllaDB

↓

HTTP Response

↓

Frontend

↓

Browser
```

---

# Attendance Flow

```
Browser

↓

Frontend

↓

Attendance API

↓

PostgreSQL

↓

Frontend

↓

Browser
```

---

# Salary Flow

```
Browser

↓

Frontend

↓

Salary API

↓

ScyllaDB

↓

HTTP Response
```

---

# Salary Synchronization Flow

Unlike Employee and Attendance, salary records require indexing.

```
Salary API

↓

ScyllaDB

↓

Scylla Sync

↓

Elasticsearch
```

The synchronization container periodically reads ScyllaDB and indexes new salary records into Elasticsearch.

---

# Notification Flow

```
Elasticsearch

↓

Notification API

↓

Generate HTML Email

↓

SMTP Server

↓

Employee Mailbox
```

---

# Complete End-to-End Flow

```
User

↓

React Frontend

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

↓

Employee
```

---

# Container Dependencies

```
Frontend

│

├── Employee API

├── Attendance API

├── Salary API

└── Notification API



Employee API

├── Redis

└── ScyllaDB



Attendance API

├── PostgreSQL

└── Redis



Salary API

├── Redis

└── ScyllaDB



Notification API

└── Elasticsearch



Scylla Sync

├── ScyllaDB

├── Elasticsearch

└── Notification API
```

---

# Database Responsibilities

| Database | Responsibility |
|------------|---------------|
| PostgreSQL | Attendance |
| Redis | Cache |
| ScyllaDB | Employee + Salary |
| Elasticsearch | Search + Notification |

---

# Startup Order

The Docker Compose startup sequence is carefully controlled.

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
All APIs Healthy

↓

Frontend
```

This guarantees that applications never start before their dependencies become available.

---

# Health Checks

Every major service exposes a health endpoint.

| Service | Endpoint |
|-----------|-----------|
| Employee API | `/api/v1/employee/health` |
| Attendance API | `/api/v1/attendance/health` |
| Salary API | `/actuator/health` |
| Notification API | `/api/v1/notification/health` |

Docker Compose waits for healthy dependencies before starting dependent containers.

---

# Persistent Storage

Containers are ephemeral.

Databases therefore use Docker volumes.

```
postgres-data

redis-data

scylladb-data

elasticsearch-data
```

Deleting containers does not delete data.

Volumes preserve data across container restarts.

---

# Port Mapping

| Component | Container Port | Host Port |
|------------|---------------|-----------|
| Frontend | 80 | 3000 |
| Employee API | 8080 | 8080 |
| Attendance API | 8081 | 8081 |
| Salary API | 8082 | 8082 |
| Notification API | 8085 | 8085 |
| PostgreSQL | 5432 | 5432 |
| Redis | 6379 | 6379 |
| ScyllaDB | 9042 | 9042 |
| Elasticsearch | 9200 | 9200 |

---

# Design Decisions

The following architectural decisions were intentionally made.

## Polyglot Architecture

Different services use different languages to demonstrate Docker's language independence.

---

## Database Per Responsibility

Each database is selected based on workload characteristics rather than using a single database for everything.

---

## Independent Containers

Each service can be upgraded independently.

---

## Stateless Services

Business services do not persist local state.

All persistent data resides inside dedicated databases.

---

## Environment-Based Configuration

Application configuration is injected using environment variables.

This enables the same image to run in:

- Local Docker
- Docker Compose
- Kubernetes
- Amazon EKS

without rebuilding.

---

# Future Architecture

The long-term deployment target is Kubernetes.

```
Internet

↓

AWS ALB

↓

Ingress

↓

Frontend

↓

Microservices

↓

Persistent Volumes

↓

Databases

↓

Prometheus

↓

Grafana

↓

Loki

↓

Tempo
```

---

# Summary

The OT-Micro-Docker platform follows a production-inspired distributed architecture built around independent microservices, dedicated databases, Docker networking, health-aware startup sequencing, and container isolation.

This design allows the application to evolve from Docker Compose to Kubernetes and Amazon EKS with minimal changes to the application containers.
