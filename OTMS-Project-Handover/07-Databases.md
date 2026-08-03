# 07 - Databases

---

# Database Architecture

---

# Introduction

The OT-Micro-Docker platform uses multiple databases instead of relying on a single database technology.

This approach follows the **Polyglot Persistence** design pattern, where each database is selected according to the workload it handles.

Rather than forcing every service to use the same database, each microservice stores its data in the database best suited for its requirements.

---

# Why Multiple Databases?

Different types of data have different characteristics.

For example:

- Employee records require high write throughput.
- Attendance records require relational consistency.
- Frequently accessed data benefits from in-memory caching.
- Notification and search operations require fast indexing.

Using one database for all workloads would introduce unnecessary compromises.

---

# Database Overview

| Database | Purpose | Container |
|-----------|----------|-----------|
| PostgreSQL | Attendance Records | postgres |
| ScyllaDB | Employee & Salary Records | scylladb |
| Redis | Cache | redis |
| Elasticsearch | Search & Notification | elasticsearch |

---

# Complete Database Architecture

```
                        Employee API
                              │
                              ▼
                         ScyllaDB
                              │
                              │
Salary API ───────────────────┘
      │
      ▼
Scylla Sync
      │
      ▼
Elasticsearch
      │
      ▼
Notification API


Attendance API
      │
      ▼
 PostgreSQL


Employee API
Attendance API
Salary API
      │
      ▼
     Redis
```

---

# Polyglot Persistence

The project intentionally demonstrates Polyglot Persistence.

```
Different Services

↓

Different Databases

↓

Best Technology

↓

Best Performance
```

Advantages

- Better scalability
- Better performance
- Independent tuning
- Flexible architecture

---

# PostgreSQL

---

## Purpose

PostgreSQL stores attendance information.

Responsibilities

- Attendance records
- Attendance history
- Attendance reporting

---

## Why PostgreSQL?

Attendance data is highly relational.

Requirements include

- ACID transactions
- SQL queries
- Referential integrity
- Date-based reporting

PostgreSQL is ideal for these workloads.

---

## Container

```
postgres
```

---

## Image

```
478mkharb/otms-postgres
```

---

## Default Port

```
5432
```

---

## Volume

```
postgres-data
```

---

## Database

```
attendance_db
```

---

## Initialization

The database is automatically initialized by

```
attendance-migration
```

using Liquibase.

---

## Startup Flow

```
PostgreSQL

↓

Health Check

↓

Attendance Migration

↓

Attendance API
```

---

## Schema

Current table

```
records
```

Composite Primary Key

```
id

+

date
```

This allows one employee to have multiple attendance entries across different dates.

---

# Attendance Migration

The migration container

```
attendance-migration
```

performs

```
Wait for PostgreSQL

↓

Run Liquibase

↓

Create Tables

↓

Exit
```

Advantages

- No schema creation inside application
- Repeatable deployments
- Independent migrations

---

# ScyllaDB

---

## Purpose

ScyllaDB stores

- Employee information
- Salary information

---

## Why ScyllaDB?

ScyllaDB is a distributed NoSQL database compatible with Apache Cassandra.

Advantages

- Extremely high write throughput
- Horizontal scalability
- Low latency
- Large datasets

---

## Container

```
scylladb
```

---

## Image

```
478mkharb/otms-scylladb
```

---

## Default Port

```
9042
```

---

## Volume

```
scylladb-data
```

---

## Keyspace

```
employee_db
```

---

## Initialization Process

ScyllaDB requires two initialization steps.

### Step 1

```
scylla-init
```

Responsibilities

- Wait for ScyllaDB
- Create Keyspace

---

### Step 2

```
scylla-migration
```

Responsibilities

- Create Employee tables
- Create Salary tables

---

## Startup Flow

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

## Tables

Employee

```
employee_info
```

Salary

```
employee_salary
```

---

# Redis

---

## Purpose

Redis provides high-speed caching.

Applications

- Employee API
- Attendance API
- Salary API

communicate with Redis.

---

## Why Redis?

Redis stores data entirely in memory.

Advantages

- Extremely fast
- Lightweight
- Low latency
- Simple key-value storage

---

## Container

```
redis
```

---

## Image

```
478mkharb/otms-redis
```

---

## Default Port

```
6379
```

---

## Volume

```
redis-data
```

---

## Persistence

Redis uses Append Only File (AOF).

Container command

```
redis-server --appendonly yes
```

This provides durability across restarts.

---

## Health Check

```
redis-cli ping
```

Expected

```
PONG
```

---

## Clearing Redis

Flush all keys

```bash
docker exec -it redis redis-cli FLUSHALL
```

---

# Elasticsearch

---

## Purpose

Elasticsearch stores indexed salary information.

Used for

- Search
- Notification processing
- Fast retrieval

---

## Why Elasticsearch?

Searching ScyllaDB repeatedly for notifications would be inefficient.

Instead

```
ScyllaDB

↓

Scylla Sync

↓

Elasticsearch
```

The Notification API reads indexed data.

---

## Container

```
elasticsearch
```

---

## Image

```
478mkharb/otms-elasticsearch
```

---

## Default Ports

REST API

```
9200
```

Transport

```
9300
```

---

## Volume

```
elasticsearch-data
```

---

## Index

```
employee_index
```

---

## Startup

```
Elasticsearch

↓

Health Check

↓

Notification API

↓

Scylla Sync
```

---

# Scylla Sync

Scylla Sync continuously synchronizes

```
ScyllaDB

↓

Elasticsearch
```

Responsibilities

- Read Salary Records
- Detect Changes
- Update Elasticsearch
- Trigger Notifications

---

# Database Communication

```
Employee API

↓

ScyllaDB
```

---

```
Attendance API

↓

PostgreSQL
```

---

```
Salary API

↓

ScyllaDB
```

---

```
Scylla Sync

↓

ScyllaDB

↓

Elasticsearch
```

---

```
Notification API

↓

Elasticsearch
```

---

# Why Redis is Separate

Redis is **not** a primary database.

Purpose

```
Applications

↓

Redis

↓

Frequently Accessed Data
```

The source of truth remains

- PostgreSQL
- ScyllaDB

---

# Data Ownership

| Service | Database |
|-----------|----------|
| Employee API | ScyllaDB |
| Attendance API | PostgreSQL |
| Salary API | ScyllaDB |
| Notification API | Elasticsearch |

Each service owns its own data.

---

# Persistent Volumes

Database containers use Docker volumes.

```
postgres-data

redis-data

scylladb-data

elasticsearch-data
```

Benefits

- Data survives container recreation
- Independent from container lifecycle

---

# Database Recovery

Stopping containers

```bash
docker compose down
```

does **not** remove data.

Removing volumes

```bash
docker compose down -v
```

removes all database contents.

---

# Backup Strategy (Future)

Production deployment should include

- PostgreSQL backups
- Scylla snapshots
- Elasticsearch snapshots
- Redis persistence validation

---

# Database Best Practices

✔ One database per responsibility

✔ Separate migration containers

✔ Persistent Docker volumes

✔ Health checks

✔ Environment variables

✔ No hardcoded credentials

✔ Independent initialization

✔ Separate source of truth from cache

---

# Lessons Learned

During implementation the following concepts were explored:

- Polyglot Persistence
- Liquibase migrations
- Composite primary keys
- Scylla keyspaces
- Docker volumes
- Elasticsearch indexing
- Redis persistence
- Database startup sequencing
- Migration container pattern

---

# Summary

The OT-Micro-Docker platform demonstrates a modern polyglot persistence architecture where each database is selected according to its workload.

- PostgreSQL provides relational storage for attendance.
- ScyllaDB stores employee and salary data.
- Redis improves performance through caching.
- Elasticsearch enables indexing and notification workflows.

This architecture improves scalability, performance, maintainability, and prepares the application for cloud-native deployments on Kubernetes and Amazon EKS.
