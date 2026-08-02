# OT-Micro-Docker

> **Standard Operating Procedure (SOP)** for deploying, verifying, troubleshooting, and maintaining the OT-Micro-Docker microservices application using Docker Compose.

---

# Table of Contents

- [1. Project Overview](#1-project-overview)
- [2. Project Architecture](#2-project-architecture)
- [3. Technology Stack](#3-technology-stack)
- [4. Project Components](#4-project-components)
- [5. Network Flow](#5-network-flow)
- [6. Exposed Ports](#6-exposed-ports)
- [7. Project Directory Structure](#7-project-directory-structure)
- [8. Prerequisites](#8-prerequisites)
- [9. Build Docker Images](#9-build-docker-images)
- [10. Starting the Application Stack](#10-starting-the-application-stack)
- [11. Application Startup Order](#11-application-startup-order)
- [12. Verify Running Containers](#12-verify-running-containers)
- [13. Verify Docker Images](#13-verify-docker-images)
- [14. Verify Docker Network](#14-verify-docker-network)
- [15. Verify Docker Volumes](#15-verify-docker-volumes)
- [16. Restart Services](#16-restart-services)
- [17. Stop the Stack](#17-stop-the-stack)
- [18. Remove Orphan Containers](#18-remove-orphan-containers)
- [19. Database Verification](#19-database-verification)
  - [19.1 ScyllaDB Verification](#191-scylladb-verification)
  - [19.2 PostgreSQL Verification](#192-postgresql-verification)
  - [19.3 Redis Verification](#193-redis-verification)
  - [19.4 Elasticsearch Verification](#194-elasticsearch-verification)
- [20. Database Migration Verification](#20-database-migration-verification)
- [21. Database Reset](#21-database-reset)
- [22. Verify Docker Volumes](#22-verify-docker-volumes)
- [23. API Verification](#23-api-verification)
  - [23.1 Employee API](#231-employee-api)
  - [23.2 Attendance API](#232-attendance-api)
  - [23.3 Salary API](#233-salary-api)
  - [23.4 Notification API](#234-notification-api)
- [24. Frontend Verification](#24-frontend-verification)
- [25. End-to-End Verification](#25-end-to-end-verification)
- [26. Service Logs](#26-service-logs)
- [27. Container Health Verification](#27-container-health-verification)
- [28. Verify Docker Resources](#28-verify-docker-resources)
- [29. Cleanup Procedures](#29-cleanup-procedures)
- [30. Docker Image Management](#30-docker-image-management)
- [31. Docker Volume Cleanup](#31-docker-volume-cleanup)
- [32. Docker Network Cleanup](#32-docker-network-cleanup)
- [33. Reset Individual Components](#33-reset-individual-components)
- [34. Clear Database Records](#34-clear-database-records)
- [35. Complete Environment Cleanup](#35-complete-environment-cleanup)
- [36. Rebuild Complete Environment](#36-rebuild-complete-environment)
- [37. Useful Docker Commands](#37-useful-docker-commands)
- [38. Useful Troubleshooting Commands](#38-useful-troubleshooting-commands)
- [39. Application Verification Checklist](#39-application-verification-checklist)
- [40. Conclusion](#40-conclusion)

---

# 1. Project Overview

OT-Micro-Docker is a Docker Compose based microservices application that demonstrates communication between multiple services using dedicated databases and supporting components.

The application consists of:

- Employee Management Service
- Attendance Management Service
- Salary Management Service
- Notification Service
- React Frontend
- Redis Cache
- ScyllaDB
- PostgreSQL
- Elasticsearch
- Database Migration Containers
- ScyllaDB → Elasticsearch Synchronization Service

The project is designed to provide an end-to-end workflow from employee creation to salary processing and email notification.

---

# 2. Project Architecture

```text
                        +----------------------+
                        |      Frontend        |
                        |    React + NGINX     |
                        +----------+-----------+
                                   |
              -------------------------------------------------
              |                 |                |            |
              ▼                 ▼                ▼            ▼

      Employee API      Attendance API     Salary API   Notification API
          (Go)             (Python)       (Spring Boot)     (Flask)

          |                    |                |               |
          ▼                    ▼                ▼               ▼

      ScyllaDB            PostgreSQL       ScyllaDB      Elasticsearch
          |                                      ▲
          |                                      |
          +-------------> Scylla Sync -----------+
```

---

# 3. Technology Stack

| Component | Technology |
|------------|------------|
| Frontend | React + NGINX |
| Employee API | Golang |
| Attendance API | Python Flask |
| Salary API | Spring Boot |
| Notification API | Python Flask |
| Database | ScyllaDB |
| Database | PostgreSQL |
| Cache | Redis |
| Search Engine | Elasticsearch |
| Database Migration | Golang Migrate |
| Database Migration | Liquibase |
| Container Runtime | Docker |
| Container Orchestration | Docker Compose |

---

# 4. Project Components

| Container | Purpose |
|------------|---------|
| `frontend` | React User Interface |
| `employee-api` | Employee CRUD Operations |
| `attendance-api` | Attendance Management |
| `salary-api` | Salary Management |
| `notification-api` | Sends Salary Notifications |
| `scylladb` | Employee & Salary Database |
| `postgres` | Attendance Database |
| `redis` | Cache Layer |
| `elasticsearch` | Stores searchable employee salary records |
| `scylla-init` | Creates ScyllaDB Keyspace |
| `scylla-migration` | Creates ScyllaDB Tables |
| `attendance-migration` | Creates PostgreSQL Tables |
| `scylla-sync` | Synchronizes ScyllaDB data into Elasticsearch |

---

# 5. Network Flow

```text
                    User
                     │
                     ▼
               React Frontend
                     │
      ┌──────────────┼──────────────┐
      │              │              │
      ▼              ▼              ▼

 Employee API   Attendance API   Salary API
      │              │              │
      ▼              ▼              ▼

 ScyllaDB      PostgreSQL      ScyllaDB
      │
      ▼

 Scylla Sync Service

      │

      ▼

 Elasticsearch

      │

      ▼

 Notification API

      │

      ▼

 Gmail SMTP

      │

      ▼

 Employee Mailbox
```

---

# 6. Exposed Ports

| Service | Port |
|----------|------|
| Frontend | **3000** |
| Employee API | **8080** |
| Attendance API | **8081** |
| Salary API | **8082** |
| Notification API | **8085** |
| PostgreSQL | **5432** |
| Redis | **6379** |
| Elasticsearch | **9200** |
| ScyllaDB | **9042** |

---

# 7. Project Directory Structure

```text
OT-Micro-Docker
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
├── scylla-sync/
│
├── docker-compose.yml
├── docker-compose.database.yml
└── README.md
```

---

# 8. Prerequisites

Ensure the following software is installed before deploying the application.

| Software | Recommended Version |
|----------|---------------------|
| Docker | Latest Stable |
| Docker Compose | v2.x |
| Git | Latest Stable |

---

## Verify Docker Installation

```bash
docker --version
```

Expected Output

```text
Docker version xx.xx.x
```

---

## Verify Docker Compose

```bash
docker compose version
```

Expected Output

```text
Docker Compose version v2.x.x
```

---

## Verify Docker Service

```bash
systemctl status docker
```

Expected Status

```text
active (running)
```

---

## Clone the Repository

```bash
git clone <repository-url>
```

---

## Navigate to the Project

```bash
cd OT-Micro-Docker
```

---

# 9. Build Docker Images

Build all Docker images before starting the application.

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
build
```

---

## Build Without Cache

Use this when Docker images are not reflecting recent source code changes.

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
build --no-cache
```

---

## Build Individual Services

### Employee API

```bash
docker compose build employee-api
```

### Attendance API

```bash
docker compose build attendance-api
```

### Salary API

```bash
docker compose build salary-api
```

### Notification API

```bash
docker compose build notification-api
```

### Frontend

```bash
docker compose build frontend
```

### Attendance Migration

```bash
docker compose build attendance-migration
```

### Scylla Migration

```bash
docker compose build scylla-migration
```

### Scylla Sync

```bash
docker compose build scylla-sync
```

---

# 10. Starting the Application Stack

The application is divided into two compose files.

| Compose File | Purpose |
|--------------|---------|
| docker-compose.database.yml | Database Services |
| docker-compose.yml | Application Services |

---

## Start Complete Stack

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
up -d
```

---

## Start Only Database Stack

```bash
docker compose \
-f docker-compose.database.yml \
up -d
```

This starts

- PostgreSQL
- Redis
- Elasticsearch
- ScyllaDB

---

## Start Only Application Stack

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
up -d \
employee-api \
attendance-api \
salary-api \
notification-api \
frontend
```

---

## Start Individual Containers

### Employee API

```bash
docker compose up -d employee-api
```

### Attendance API

```bash
docker compose up -d attendance-api
```

### Salary API

```bash
docker compose up -d salary-api
```

### Notification API

```bash
docker compose up -d notification-api
```

### Frontend

```bash
docker compose up -d frontend
```

---

# 11. Application Startup Order

The application starts in the following sequence.

```text
ScyllaDB
      │
      ▼
Scylla Init
      │
      ▼
Scylla Migration
      │
      ▼
Employee API
      │
      ▼
Salary API
      │
      ▼
Scylla Sync
      │
      ▼
Elasticsearch
      │
      ▼
Notification API

--------------------------------

PostgreSQL
      │
      ▼
Attendance Migration
      │
      ▼
Attendance API

--------------------------------

Redis

--------------------------------

Frontend
```

---

# 12. Verify Running Containers

List all running containers.

```bash
docker ps
```

Expected Output

| Container | Status |
|------------|--------|
| scylladb | Up |
| postgres | Up (healthy) |
| redis | Up (healthy) |
| elasticsearch | Up (healthy) |
| scylla-init | Exited (0) |
| scylla-migration | Exited (0) |
| attendance-migration | Exited (0) |
| employee-api | Up (healthy) |
| attendance-api | Up (healthy) |
| salary-api | Up (healthy) |
| notification-api | Up (healthy) |
| scylla-sync | Up |
| frontend | Up |

---

## Verify All Containers

```bash
docker ps -a
```

Migration containers should have

```text
Exited (0)
```

This indicates successful database initialization.

---

# 13. Verify Docker Images

```bash
docker images
```

Expected Images

- ot-micro-docker-employee-api
- ot-micro-docker-attendance-api
- ot-micro-docker-salary-api
- ot-micro-docker-notification-api
- ot-micro-docker-frontend
- ot-micro-docker-scylla-sync
- ot-micro-docker-attendance-migration
- ot-micro-docker-scylla-migration

---

# 14. Verify Docker Network

```bash
docker network ls
```

Expected Network

```text
otms-network
```

Inspect network

```bash
docker network inspect otms-network
```

All application containers should appear in the network.

---

# 15. Verify Docker Volumes

```bash
docker volume ls
```

Expected Volumes

```text
ot-micro-docker_postgres-data

ot-micro-docker_scylladb-data

ot-micro-docker_redis-data

ot-micro-docker_elasticsearch-data
```

---

# 16. Restart Services

Restart Entire Stack

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
restart
```

Restart Individual Service

Example

```bash
docker restart employee-api
```

```bash
docker restart attendance-api
```

```bash
docker restart salary-api
```

```bash
docker restart notification-api
```

```bash
docker restart scylla-sync
```

---

# 17. Stop the Stack

Stop all containers

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
down
```

Containers will stop but volumes will be preserved.

---

# 18. Remove Orphan Containers

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
down --remove-orphans
```

This removes unused containers created by previous compose configurations.

---

# 19. Database Verification

This section describes how to verify each database after the application stack has started successfully.

---

# 19.1 ScyllaDB Verification

## Access ScyllaDB

```bash
docker exec -it scylladb cqlsh
```

---

## List Keyspaces

```sql
DESCRIBE KEYSPACES;
```

Expected Output

```text
employee_db
system
system_auth
system_schema
...
```

---

## Use Employee Keyspace

```sql
USE employee_db;
```

---

## Verify Tables

```sql
DESCRIBE TABLES;
```

Expected Output

```text
employee_info
employee_salary
schema_migrations
```

---

## Verify Employee Records

```sql
SELECT * FROM employee_info;
```

Example

```text
 id | designation | email                 | name
----+-------------+----------------------+--------
 1  | DevOps      | abc@gmail.com        | Mukesh
```

---

## Verify Salary Records

```sql
SELECT * FROM employee_salary;
```

Example

```text
 id | process_date | name | salary | status
```

---

## Verify Migration Version

```sql
SELECT * FROM schema_migrations;
```

Expected Output

```text
 version | dirty
---------+-------
       2 | False
```

> **Note:** `dirty = False` indicates that all migrations have been applied successfully.

---

## Exit ScyllaDB

```sql
exit
```

---

# 19.2 PostgreSQL Verification

## Access PostgreSQL

```bash
docker exec -it postgres psql -U postgres -d attendance_db
```

---

## List Tables

```sql
\dt
```

Expected Output

```text
records
databasechangelog
databasechangeloglock
```

---

## Verify Table Structure

```sql
\d records
```

Expected Output

```text
id
name
status
date
```

Primary Key

```text
records_pk PRIMARY KEY (id, date)
```

---

## View Attendance Records

```sql
SELECT * FROM records;
```

Example

```text
 id | name | status | date
```

---

## Verify Liquibase Changesets

```sql
SELECT * FROM databasechangelog;
```

Expected Output

```text
ID | AUTHOR
```

---

## Exit PostgreSQL

```sql
\q
```

---

# 19.3 Redis Verification

## Access Redis

```bash
docker exec -it redis redis-cli
```

---

## Test Redis

```redis
PING
```

Expected Output

```text
PONG
```

---

## List Keys

```redis
KEYS *
```

---

## Get Key

```redis
GET <key-name>
```

---

## Exit Redis

```redis
exit
```

---

# 19.4 Elasticsearch Verification

## Verify Elasticsearch Health

```bash
curl http://localhost:9200
```

Expected Output

```json
{
  "cluster_name":"docker-cluster"
}
```

---

## List Indices

```bash
curl "http://localhost:9200/_cat/indices?v"
```

Expected Output

```text
employee_index
.geoip_databases
```

---

## View Indexed Documents

```bash
curl "http://localhost:9200/employee_index/_search?pretty"
```

Expected Output

```json
{
    "hits": {
        "total": {
            "value": 1
        }
    }
}
```

---

## Search by Employee ID

```bash
curl -X GET "http://localhost:9200/employee_index/_search?pretty" \
-H "Content-Type: application/json" \
-d '{
  "query": {
    "match": {
      "employee_id": "1"
    }
  }
}'
```

---

## Delete All Documents (Keep Index)

```bash
curl -X POST \
"http://localhost:9200/employee_index/_delete_by_query?pretty" \
-H "Content-Type: application/json" \
-d '{
  "query": {
    "match_all": {}
  }
}'
```

---

## Delete Employee Index

```bash
curl -X DELETE \
http://localhost:9200/employee_index
```

The Scylla Sync service will recreate the index automatically when synchronization runs.

---

## Restart Scylla Sync

```bash
docker restart scylla-sync
```

---

## Verify Index Recreation

```bash
curl "http://localhost:9200/_cat/indices?v"
```

---

# 20. Database Migration Verification

## Verify Scylla Migration

```bash
docker logs scylla-migration
```

Expected

```text
ScyllaDB Migration Completed Successfully
```

---

## Verify Attendance Migration

```bash
docker logs attendance-migration
```

Expected

```text
Attendance Migration Completed Successfully
```

---

## Verify Scylla Initialization

```bash
docker logs scylla-init
```

Expected

```text
Keyspace employee_db created successfully
```

---

# 21. Database Reset

> **Use only in development environments.** These commands remove all persisted data.

---

## Reset PostgreSQL

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
down
```

Remove volume

```bash
docker volume rm ot-micro-docker_postgres-data
```

Start stack

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
up -d
```

---

## Reset ScyllaDB

Stop stack

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
down
```

Remove volume

```bash
docker volume rm ot-micro-docker_scylladb-data
```

Start stack

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
up -d
```

---

## Reset Elasticsearch

Stop stack

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
down
```

Remove volume

```bash
docker volume rm ot-micro-docker_elasticsearch-data
```

Start stack

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
up -d
```

---

## Reset Redis

Stop stack

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
down
```

Remove volume

```bash
docker volume rm ot-micro-docker_redis-data
```

Start stack

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
up -d
```

---

# 22. Verify Docker Volumes

```bash
docker volume ls
```

Expected

```text
ot-micro-docker_postgres-data
ot-micro-docker_scylladb-data
ot-micro-docker_elasticsearch-data
ot-micro-docker_redis-data
```

---

# 23. API Verification

This section describes how to verify each microservice after the application stack is running.

---

# 23.1 Employee API

## Health Check

```bash
curl http://localhost:8080/api/v1/employee/health
```

Expected Response

```json
{
  "status": "UP"
}
```

---

## Swagger UI

Open in browser

```
http://localhost:8080/swagger/index.html
```

Verify

- Swagger page loads successfully.
- All Employee API endpoints are visible.
- APIs can be executed successfully.

---

## Create Employee

```bash
curl -X POST http://localhost:8080/api/v1/employee \
-H "Content-Type: application/json" \
-d '{
  "id":"101",
  "name":"Mukesh",
  "designation":"DevOps Engineer",
  "email":"mukesh@gmail.com"
}'
```

Expected Response

```json
{
  "id":"101",
  "name":"Mukesh"
}
```

---

## Verify Employee in ScyllaDB

```bash
docker exec -it scylladb cqlsh
```

```sql
USE employee_db;

SELECT * FROM employee_info;
```

---

# 23.2 Attendance API

## Health Check

```bash
curl http://localhost:8081/api/v1/attendance/health
```

Expected Response

```json
{
  "status":"UP"
}
```

---

## Swagger UI

Open

```
http://localhost:8081/apidocs
```

Verify

- Swagger UI loads.
- Attendance APIs are visible.
- Endpoints execute successfully.

---

## Create Attendance

```bash
curl -X POST http://localhost:8081/api/v1/attendance \
-H "Content-Type: application/json" \
-d '{
    "id":"101",
    "name":"Mukesh",
    "status":"Present",
    "date":"2026-08-02"
}'
```

Expected Response

```json
{
    "message":"Attendance Recorded Successfully"
}
```

---

## Verify Attendance

```bash
docker exec -it postgres \
psql -U postgres -d attendance_db
```

```sql
SELECT * FROM records;
```

---

# 23.3 Salary API

## Health Check

```bash
curl http://localhost:8082/actuator/health
```

Expected Response

```json
{
    "status":"UP"
}
```

---

## Swagger UI

Open

```
http://localhost:8082/swagger-ui/index.html
```

Verify

- Swagger page loads.
- Salary APIs are visible.
- APIs execute successfully.

---

## Add Salary Record

```bash
curl -X POST http://localhost:8082/api/v1/salary \
-H "Content-Type: application/json" \
-d '{
    "id":"101",
    "name":"Mukesh",
    "salary":120000,
    "processDate":"2026-08-02",
    "status":"Active"
}'
```

---

## Verify Salary

```bash
docker exec -it scylladb cqlsh
```

```sql
USE employee_db;

SELECT * FROM employee_salary;
```

---

# 23.4 Notification API

## Health Check

```bash
curl http://localhost:8085/api/v1/notification/health
```

Expected Response

```json
{
    "status":"UP"
}
```

---

## Swagger UI

Open

```
http://localhost:8085/apidocs
```

Verify

- Swagger loads successfully.
- All Notification APIs are listed.

---

## Send Notification

```bash
curl -X POST \
http://localhost:8085/api/v1/notification/send/all
```

Expected Response

```json
{
    "notifications_sent":1,
    "failed_notifications":0
}
```

---

# 24. Frontend Verification

Open

```
http://localhost:3000
```

Verify

- Frontend loads successfully.
- Navigation menu is visible.
- No browser console errors.
- All pages open correctly.

---

## Employee Module

Verify

- Add Employee
- View Employees

---

## Attendance Module

Verify

- Add Attendance
- View Attendance

---

## Salary Module

Verify

- Process Salary
- View Salary Records

---

## Notification

Verify

- Email is delivered successfully.
- Employee receives salary notification.

---

# 25. End-to-End Verification

Perform the following sequence.

## Step 1

Create Employee

↓

Verify in ScyllaDB

---

## Step 2

Create Attendance

↓

Verify in PostgreSQL

---

## Step 3

Process Salary

↓

Verify in ScyllaDB

---

## Step 4

Verify Scylla Sync

```bash
docker logs scylla-sync
```

Expected

```text
Indexed Employee:
```

---

## Step 5

Verify Elasticsearch

```bash
curl \
"http://localhost:9200/employee_index/_search?pretty"
```

Employee document should exist.

---

## Step 6

Trigger Notification

```bash
curl -X POST \
http://localhost:8085/api/v1/notification/send/all
```

---

## Step 7

Verify Email

Employee should receive the salary notification email.

---

## Step 8

Verify Elasticsearch Status

```bash
curl \
"http://localhost:9200/employee_index/_search?pretty"
```

Expected

```json
"notified": true
```

---

# 26. Service Logs

## Employee API

```bash
docker logs employee-api
```

Follow logs

```bash
docker logs -f employee-api
```

---

## Attendance API

```bash
docker logs attendance-api
```

Follow logs

```bash
docker logs -f attendance-api
```

---

## Salary API

```bash
docker logs salary-api
```

Follow logs

```bash
docker logs -f salary-api
```

---

## Notification API

```bash
docker logs notification-api
```

Follow logs

```bash
docker logs -f notification-api
```

---

## Scylla Sync

```bash
docker logs scylla-sync
```

Follow logs

```bash
docker logs -f scylla-sync
```

---

## Scylla Migration

```bash
docker logs scylla-migration
```

---

## Attendance Migration

```bash
docker logs attendance-migration
```

---

## Scylla Initialization

```bash
docker logs scylla-init
```

---

## PostgreSQL

```bash
docker logs postgres
```

---

## Redis

```bash
docker logs redis
```

---

## Elasticsearch

```bash
docker logs elasticsearch
```

---

# 27. Container Health Verification

View health status

```bash
docker ps
```

Inspect health

```bash
docker inspect employee-api
```

```bash
docker inspect attendance-api
```

```bash
docker inspect salary-api
```

```bash
docker inspect notification-api
```

Expected

```text
healthy
```

---

# 28. Verify Docker Resources

## Running Containers

```bash
docker ps
```

---

## Images

```bash
docker images
```

---

## Networks

```bash
docker network ls
```

---

## Volumes

```bash
docker volume ls
```

---

# 29. Cleanup Procedures

This section covers stopping services, removing containers, deleting images, clearing persisted data, and performing a complete environment reset.

> **Warning**
>
> The commands in this section permanently remove containers, images, networks, and database volumes. Use them only in development environments.

---

# 29.1 Stop the Complete Stack

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
down
```

---

# 29.2 Stop and Remove Orphan Containers

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
down --remove-orphans
```

---

# 29.3 Stop Individual Containers

Example

```bash
docker stop employee-api
```

```bash
docker stop attendance-api
```

```bash
docker stop salary-api
```

```bash
docker stop notification-api
```

```bash
docker stop frontend
```

---

# 29.4 Remove Individual Containers

```bash
docker rm employee-api
```

```bash
docker rm attendance-api
```

```bash
docker rm salary-api
```

```bash
docker rm notification-api
```

```bash
docker rm frontend
```

---

# 30. Docker Image Management

## List Images

```bash
docker images
```

---

## Remove Individual Image

Example

```bash
docker rmi ot-micro-docker-employee-api
```

---

## Remove All Project Images

```bash
docker rmi \
ot-micro-docker-employee-api \
ot-micro-docker-attendance-api \
ot-micro-docker-salary-api \
ot-micro-docker-notification-api \
ot-micro-docker-frontend \
ot-micro-docker-scylla-sync \
ot-micro-docker-scylla-migration \
ot-micro-docker-attendance-migration
```

---

## Remove Dangling Images

```bash
docker image prune
```

---

## Remove All Unused Images

```bash
docker image prune -a
```

---

# 31. Docker Volume Cleanup

## List Volumes

```bash
docker volume ls
```

---

## Remove PostgreSQL Volume

```bash
docker volume rm ot-micro-docker_postgres-data
```

---

## Remove ScyllaDB Volume

```bash
docker volume rm ot-micro-docker_scylladb-data
```

---

## Remove Redis Volume

```bash
docker volume rm ot-micro-docker_redis-data
```

---

## Remove Elasticsearch Volume

```bash
docker volume rm ot-micro-docker_elasticsearch-data
```

---

## Remove All Unused Volumes

```bash
docker volume prune
```

---

# 32. Docker Network Cleanup

## List Networks

```bash
docker network ls
```

---

## Remove Project Network

```bash
docker network rm otms-network
```

---

## Remove Unused Networks

```bash
docker network prune
```

---

# 33. Reset Individual Components

---

## Reset PostgreSQL

```bash
docker compose down
```

```bash
docker volume rm ot-micro-docker_postgres-data
```

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
up -d
```

---

## Reset ScyllaDB

```bash
docker compose down
```

```bash
docker volume rm ot-micro-docker_scylladb-data
```

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
up -d
```

---

## Reset Elasticsearch

```bash
docker compose down
```

```bash
docker volume rm ot-micro-docker_elasticsearch-data
```

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
up -d
```

---

## Reset Redis

```bash
docker compose down
```

```bash
docker volume rm ot-micro-docker_redis-data
```

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
up -d
```

---

# 34. Clear Database Records

---

## Delete Elasticsearch Index

```bash
curl -X DELETE \
http://localhost:9200/employee_index
```

---

## Delete All Elasticsearch Documents

```bash
curl -X POST \
"http://localhost:9200/employee_index/_delete_by_query?pretty" \
-H "Content-Type: application/json" \
-d '{
  "query": {
    "match_all": {}
  }
}'
```

---

## Restart Scylla Sync

```bash
docker restart scylla-sync
```

The synchronization service recreates the Elasticsearch index and reindexes employee salary records from ScyllaDB.

---

## Delete Employee Data from ScyllaDB

```bash
docker exec -it scylladb cqlsh
```

```sql
USE employee_db;

TRUNCATE employee_info;

TRUNCATE employee_salary;
```

---

## Delete Attendance Records

```bash
docker exec -it postgres \
psql -U postgres -d attendance_db
```

```sql
TRUNCATE TABLE records;
```

---

## Clear Redis Cache

```bash
docker exec -it redis redis-cli
```

```redis
FLUSHALL
```

Expected Response

```text
OK
```

---

# 35. Complete Environment Cleanup

Remove containers, images, networks, and volumes.

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
down \
-v \
--remove-orphans
```

Remove unused resources

```bash
docker system prune -a
```

Remove unused volumes

```bash
docker volume prune
```

Remove unused networks

```bash
docker network prune
```

---

# 36. Rebuild Complete Environment

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
build --no-cache
```

Start the stack

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
up -d
```

---

# 37. Useful Docker Commands

## Running Containers

```bash
docker ps
```

---

## All Containers

```bash
docker ps -a
```

---

## Images

```bash
docker images
```

---

## Networks

```bash
docker network ls
```

---

## Volumes

```bash
docker volume ls
```

---

## Docker System Usage

```bash
docker system df
```

---

## Docker Events

```bash
docker events
```

---

# 38. Useful Troubleshooting Commands

## Follow Logs

```bash
docker logs -f employee-api
```

```bash
docker logs -f attendance-api
```

```bash
docker logs -f salary-api
```

```bash
docker logs -f notification-api
```

```bash
docker logs -f scylla-sync
```

---

## Execute Commands Inside Containers

```bash
docker exec -it employee-api sh
```

```bash
docker exec -it attendance-api sh
```

```bash
docker exec -it salary-api sh
```

```bash
docker exec -it notification-api sh
```

```bash
docker exec -it scylladb bash
```

```bash
docker exec -it postgres bash
```

```bash
docker exec -it redis sh
```

---

## Inspect Container

```bash
docker inspect employee-api
```

---

## View Resource Usage

```bash
docker stats
```

---

# 39. Application Verification Checklist

| Verification | Status |
|--------------|--------|
| Docker Engine Running | ☐ |
| Docker Compose Installed | ☐ |
| All Images Built | ☐ |
| All Containers Running | ☐ |
| Docker Network Created | ☐ |
| Docker Volumes Created | ☐ |
| ScyllaDB Healthy | ☐ |
| PostgreSQL Healthy | ☐ |
| Redis Healthy | ☐ |
| Elasticsearch Healthy | ☐ |
| Employee Migration Completed | ☐ |
| Attendance Migration Completed | ☐ |
| Employee API Healthy | ☐ |
| Attendance API Healthy | ☐ |
| Salary API Healthy | ☐ |
| Notification API Healthy | ☐ |
| Frontend Accessible | ☐ |
| Employee Creation Working | ☐ |
| Attendance Creation Working | ☐ |
| Salary Processing Working | ☐ |
| Scylla Sync Working | ☐ |
| Elasticsearch Indexed Data | ☐ |
| Email Notification Sent | ☐ |
| End-to-End Flow Verified | ☐ |

---

# 40. Conclusion

Following this SOP ensures that:

- Docker images are built successfully.
- All infrastructure services start in the correct order.
- Database migrations execute successfully.
- Microservices communicate correctly.
- ScyllaDB synchronizes salary data to Elasticsearch.
- Notification service sends salary emails using Gmail SMTP.
- All APIs are verified through health endpoints and Swagger UI.
- Database contents can be inspected and reset as needed.
- Logs and troubleshooting commands are readily available for diagnosing issues.
- The complete OT-Micro-Docker application can be deployed, verified, maintained, and reset in a repeatable manner.

---# OT-Micro-Docker
