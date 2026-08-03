# 10 - Deployment SOP (Standard Operating Procedure)

---

# Deployment SOP

---

# Purpose

This Standard Operating Procedure (SOP) describes the complete deployment process for the OT-Micro-Docker platform.

By following this document, a new user should be able to:

- Deploy the complete application
- Verify every component
- Validate APIs
- Validate databases
- Validate Swagger
- Verify email functionality
- View logs
- Reset the environment
- Upgrade images

---

# Prerequisites

Ensure the following software is installed.

| Software | Version |
|-----------|----------|
| Docker Engine | Latest |
| Docker Compose | Latest |
| Git | Latest |

---

# Verify Installation

Docker

```bash
docker --version
```

Docker Compose

```bash
docker compose version
```

Git

```bash
git --version
```

---

# Clone Repository

```bash
git clone https://github.com/478mkharb/OT-Micro-Docker.git

cd OT-Micro-Docker
```

---

# Verify Docker Compose Files

```bash
ls
```

Expected

```
docker-compose.yml

docker-compose.database.yml
```

---

# Verify Compose Configuration

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
config
```

No errors should be displayed.

---

# Pull Latest Images (Optional)

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
pull
```

---

# Start Complete Stack

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
up -d
```

Docker Compose automatically

- Creates network
- Creates volumes
- Pulls missing images
- Starts databases
- Runs migrations
- Starts APIs
- Starts frontend

---

# Verify Containers

```bash
docker ps
```

Expected running containers

```
postgres

redis

scylladb

elasticsearch

employee-api

attendance-api

salary-api

notification-api

frontend

scylla-sync
```

Migration containers

```
attendance-migration

scylla-init

scylla-migration
```

should have status

```
Exited (0)
```

---

# Verify Network

```bash
docker network ls
```

Expected

```
otms-network
```

---

# Verify Volumes

```bash
docker volume ls
```

Expected

```
postgres-data

redis-data

scylladb-data

elasticsearch-data
```

---

# Verify Logs

Employee API

```bash
docker logs employee-api
```

Attendance API

```bash
docker logs attendance-api
```

Salary API

```bash
docker logs salary-api
```

Notification API

```bash
docker logs notification-api
```

Frontend

```bash
docker logs frontend
```

Live logs

```bash
docker logs -f employee-api
```

All services

```bash
docker compose logs
```

---

# Verify Health Endpoints

Employee

```bash
curl http://localhost:8080/api/v1/employee/health
```

Attendance

```bash
curl http://localhost:8081/api/v1/attendance/health
```

Salary

```bash
curl http://localhost:8082/actuator/health
```

Notification

```bash
curl http://localhost:8085/api/v1/notification/health
```

Expected

```
HTTP 200 OK
```

---

# Verify Swagger

Employee API

```
http://localhost:8080/swagger/index.html
```

Attendance API

```
http://localhost:8081/apidocs
```

Salary API

```
http://localhost:8082/swagger-ui/index.html
```

Notification API

```
http://localhost:8085/apidocs
```

All Swagger pages should load successfully.

---

# Verify Frontend

Open

```
http://localhost:3000
```

Verify

- Employee Page
- Attendance Page
- Salary Page

---

# Verify PostgreSQL

Open PostgreSQL

```bash
docker exec -it postgres psql \
-U postgres \
-d attendance_db
```

List tables

```sql
\dt
```

View data

```sql
SELECT * FROM records;
```

Exit

```sql
\q
```

---

# Verify ScyllaDB

Open CQLSH

```bash
docker exec -it scylladb cqlsh
```

Use keyspace

```sql
USE employee_db;
```

List tables

```sql
DESCRIBE TABLES;
```

Employee records

```sql
SELECT * FROM employee_info;
```

Salary records

```sql
SELECT * FROM employee_salary;
```

Exit

```sql
EXIT;
```

---

# Verify Redis

Connect

```bash
docker exec -it redis redis-cli
```

Ping

```text
PING
```

Expected

```
PONG
```

List keys

```text
KEYS *
```

Exit

```text
EXIT
```

---

# Clear Redis

```bash
docker exec -it redis redis-cli FLUSHALL
```

Expected

```
OK
```

---

# Verify Elasticsearch

Cluster Health

```bash
curl http://localhost:9200/_cluster/health?pretty
```

List indices

```bash
curl http://localhost:9200/_cat/indices?v
```

View index

```bash
curl http://localhost:9200/employee_index/_search?pretty
```

---

# Delete Elasticsearch Index

Delete one index

```bash
curl -X DELETE \
http://localhost:9200/employee_index
```

Delete all indices

```bash
curl -X DELETE \
http://localhost:9200/_all
```

---

# Verify Email Notification

1. Create Employee

2. Create Salary

3. Wait for Scylla Sync

4. Verify Elasticsearch

5. Verify Email Received

If email is not received

Check

```bash
docker logs notification-api
```

---

# View Running Containers

```bash
docker ps
```

Stopped containers

```bash
docker ps -a
```

---

# Restart One Service

```bash
docker restart employee-api
```

---

# Restart Entire Stack

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
restart
```

---

# Stop Stack

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
down
```

Volumes remain intact.

---

# Stop Stack and Remove Data

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
down -v
```

This removes

- Containers
- Networks
- Volumes

All database data is deleted.

---

# Update Images

Download latest images

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
pull
```

Restart

```bash
docker compose \
-f docker-compose.database.yml \
-f docker-compose.yml \
up -d
```

---

# Remove Images

Example

```bash
docker rmi \
478mkharb/otms-employee-api
```

---

# Remove All OTMS Images

```bash
docker images | grep otms
```

Then

```bash
docker rmi IMAGE_NAME
```

---

# Cleanup Unused Resources

Containers

```bash
docker container prune
```

Images

```bash
docker image prune
```

Volumes

```bash
docker volume prune
```

Everything

```bash
docker system prune -a
```

---

# Common Verification Checklist

| Component | Status |
|-----------|---------|
| Docker Running | ✅ |
| Network Created | ✅ |
| Volumes Created | ✅ |
| PostgreSQL Healthy | ✅ |
| Redis Healthy | ✅ |
| ScyllaDB Healthy | ✅ |
| Elasticsearch Healthy | ✅ |
| Employee API Healthy | ✅ |
| Attendance API Healthy | ✅ |
| Salary API Healthy | ✅ |
| Notification API Healthy | ✅ |
| Frontend Running | ✅ |
| Swagger Working | ✅ |
| Email Working | ✅ |

---

# Troubleshooting Quick Commands

View logs

```bash
docker logs CONTAINER_NAME
```

Container status

```bash
docker ps -a
```

Compose configuration

```bash
docker compose config
```

Restart service

```bash
docker restart CONTAINER_NAME
```

Shell inside container

```bash
docker exec -it CONTAINER_NAME sh
```

Inspect network

```bash
docker network inspect otms-network
```

Inspect volume

```bash
docker volume ls
```

---

# Deployment Flow Summary

```
Clone Repository

↓

Pull Images (Optional)

↓

Docker Compose Up

↓

Infrastructure Starts

↓

Migration Containers Execute

↓

Application Services Start

↓

Health Checks Pass

↓

Frontend Available

↓

Application Ready
```

---

# Success Criteria

The deployment is considered successful when:

- All infrastructure containers are running.
- Migration containers complete with exit code 0.
- All application containers are healthy.
- Swagger documentation is accessible.
- Frontend loads successfully.
- Employee, Attendance, and Salary operations work.
- Notification emails are sent successfully.
- Elasticsearch contains indexed salary records.

---

# Summary

This SOP provides a repeatable deployment procedure for the OT-Micro-Docker platform. Following these steps ensures that the complete microservices stack is deployed consistently, verified thoroughly, and can be maintained or reset with minimal effort.

The deployment process is intentionally designed to mirror production practices by separating infrastructure, migrations, and application services while relying on Docker Compose for orchestration.
