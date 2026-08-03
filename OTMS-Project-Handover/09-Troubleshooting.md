# 09 - Troubleshooting

---

# Troubleshooting Guide

---

# Introduction

During the development of the OT-Micro-Docker project, several real-world issues were encountered while containerizing applications, configuring databases, integrating services, publishing images, and orchestrating the complete stack.

This document captures the actual problems encountered during implementation together with their root causes and resolutions.

Rather than presenting generic troubleshooting advice, this guide documents the practical debugging journey of the project.

---

# Troubleshooting Workflow

Whenever an issue occurs, follow this sequence.

```
Problem

↓

Read Error Carefully

↓

Identify Service

↓

Check Container Status

↓

Check Logs

↓

Verify Health

↓

Verify Network

↓

Verify Database

↓

Fix

↓

Restart Service
```

---

# Container Not Starting

## Symptoms

```
Exited (1)

Restarting

Created

Dead
```

---

## Diagnosis

Check container status

```bash
docker ps -a
```

---

## View Logs

```bash
docker logs container-name
```

Example

```bash
docker logs attendance-api
```

---

## Restart Container

```bash
docker restart container-name
```

---

# Docker Compose Failed

## Symptoms

```
dependency failed

service unhealthy

exit code 1
```

---

## Verify Compose Configuration

```bash
docker compose config
```

---

## Start Again

```bash
docker compose down

docker compose up -d
```

---

# Health Check Failure

## Symptoms

Container keeps waiting.

Dependent service never starts.

---

## Diagnosis

Verify health endpoint.

Example

```bash
curl http://localhost:8080/api/v1/employee/health
```

---

If endpoint fails

```
↓

Check logs

↓

Check database

↓

Restart
```

---

# PostgreSQL Connection Failed

## Symptoms

```
connection refused

database unavailable
```

---

## Verify Container

```bash
docker ps
```

---

## Verify Health

```bash
docker logs postgres
```

---

## Test Database

```bash
docker exec -it postgres psql \
-U postgres \
-d attendance_db
```

---

# Attendance Migration Failed

## Symptoms

Liquibase exits with error.

Attendance API does not start.

---

## Verify Logs

```bash
docker logs attendance-migration
```

---

## Root Cause Encountered

Incorrect Liquibase changelog.

Attendance table originally had

```
id

Primary Key
```

This prevented multiple attendance records for the same employee.

---

## Solution

Changed schema to

Composite Primary Key

```
id

+

date
```

using

```
addPrimaryKey
```

Liquibase migration completed successfully afterwards.

---

# Liquibase File Not Found

## Symptoms

```
No such file

ChangeLog not found
```

---

## Root Cause

Incorrect COPY location inside Dockerfile.

Actual location

```
/migration/migration/
```

instead of

```
/migration/
```

---

## Verification

```bash
docker run --rm \
--entrypoint ls \
image-name \
-R /migration
```

---

# ScyllaDB Not Ready

## Symptoms

Employee API fails.

Salary API fails.

---

## Diagnosis

View logs

```bash
docker logs scylladb
```

---

Verify CQL

```bash
docker exec -it scylladb cqlsh
```

---

## Root Cause

Applications started before keyspace creation.

---

## Solution

Introduced

```
scylla-init

↓

scylla-migration

↓

Employee API
```

using

```
depends_on
```

---

# Redis Connection Failed

## Symptoms

```
connection refused
```

---

## Verify

```bash
docker logs redis
```

---

## Test

```bash
docker exec -it redis redis-cli ping
```

Expected

```
PONG
```

---

# Clearing Redis

Incorrect

```bash
flushall
```

Correct

```bash
docker exec -it redis redis-cli FLUSHALL
```

---

# Elasticsearch Issues

## Symptoms

Notification API returns

```
index not found
```

---

## Verify

```bash
curl http://localhost:9200/_cat/indices?v
```

---

## Delete Index

```bash
curl -X DELETE \
http://localhost:9200/employee_index
```

---

## Delete All Indices

```bash
curl -X DELETE \
http://localhost:9200/_all
```

---

# SMTP Email Not Working

## Symptoms

Emails not delivered.

Authentication failure.

---

## Root Cause

Incorrect Gmail credentials.

---

## Solution

Configure

```
SMTP_USERNAME

SMTP_PASSWORD

SMTP_SERVER

SMTP_PORT
```

inside Docker Compose.

---

Generate Gmail App Password.

Do NOT use Gmail account password.

---

# Notification API Failed

## Symptoms

Container exits immediately.

---

## Diagnosis

```bash
docker logs notification-api
```

---

## Common Causes

Incorrect

```
SMTP

Elasticsearch

Environment Variables

Python syntax
```

---

# Docker Build Failed

## Symptoms

```
COPY failed

file not found
```

---

## Diagnosis

Verify build context.

```
build:

context:
```

---

Remember

Docker can only access files inside the build context.

---

# Docker Hub Push Failed

## Symptoms

```
access denied
```

---

## Root Cause

Not logged in.

---

## Solution

```bash
docker login
```

---

# Wrong Repository

Incorrect

```
employee-api
```

Correct

```
478mkharb/otms-employee-api
```

---

# Images Not Updating

## Symptoms

Old application still running.

---

## Solution

```bash
docker compose pull

docker compose up -d
```

---

# Git Repository Issue

## Problem Encountered

Repository accidentally became inconsistent after running

```
git init
```

outside intended project structure.

---

## Diagnosis

Verify

```bash
find . -name ".git"
```

---

Check

```bash
git status
```

---

Check

```bash
git remote -v
```

---

Solution

Restore repository and push corrected history.

---

# Docker Desktop Confusion

Docker Engine works independently.

Docker Desktop is optional.

Verified using

```bash
docker info
```

---

# Docker GUI

Recommended

```
Portainer
```

Container

```
portainer/portainer-ce
```

Provides

- Container Management

- Logs

- Networks

- Volumes

- Images

---

# Docker Hub Deployment

Users do NOT need

```bash
docker login
```

when repositories are public.

Simply execute

```bash
docker compose up -d
```

Docker automatically downloads missing images.

---

# Volume Cleanup

Remove containers

```bash
docker compose down
```

---

Remove containers and data

```bash
docker compose down -v
```

---

# View Logs

Single container

```bash
docker logs employee-api
```

---

Live logs

```bash
docker logs -f employee-api
```

---

All services

```bash
docker compose logs
```

---

# Inspect Network

```bash
docker network inspect otms-network
```

---

# Inspect Volumes

```bash
docker volume ls
```

---

# Inspect Running Containers

```bash
docker ps
```

---

Stopped Containers

```bash
docker ps -a
```

---

# Verify APIs

Employee

```bash
curl localhost:8080/api/v1/employee/health
```

Attendance

```bash
curl localhost:8081/api/v1/attendance/health
```

Salary

```bash
curl localhost:8082/actuator/health
```

Notification

```bash
curl localhost:8085/api/v1/notification/health
```

---

# Verify Swagger

Employee

```
http://localhost:8080/swagger/index.html
```

Attendance

```
http://localhost:8081/apidocs
```

Salary

```
http://localhost:8082/swagger-ui/index.html
```

Notification

```
http://localhost:8085/apidocs
```

---

# Debugging Checklist

Whenever any service fails, verify

✔ Docker daemon running

✔ Container running

✔ Logs

✔ Health endpoint

✔ Database connectivity

✔ Environment variables

✔ Docker network

✔ Docker volumes

✔ Database schema

✔ API endpoint

✔ Swagger

✔ Image version

---

# Lessons Learned

Throughout the implementation of OTMS, the following practical lessons were reinforced:

- Always use health checks for service dependencies.
- Separate database migrations from application startup.
- Prefer environment variables over hardcoded configuration.
- Use Docker volumes for persistent data.
- Publish images to Docker Hub for faster deployments.
- Use dedicated logs and health endpoints for troubleshooting.
- Validate Docker Compose configuration before deployment.
- Debug one service at a time instead of restarting the entire stack.
- Build self-contained images to simplify deployments across environments.

---

# Summary

Troubleshooting is an integral part of the OT-Micro-Docker project. By following a structured approach—checking container status, reviewing logs, verifying health checks, confirming network connectivity, and validating database state—most issues can be diagnosed and resolved quickly.

The troubleshooting experience gained while building OTMS provides practical knowledge that extends beyond this project and is directly applicable to production Docker, Docker Compose, Kubernetes, and cloud-native environments.
