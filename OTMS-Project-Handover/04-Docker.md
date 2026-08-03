# 04 - Docker

---

# Docker Implementation

---

# Introduction

Docker is the foundation of the OT-Micro-Docker project.

Every application component is packaged as an independent Docker image and executed as an isolated container. This ensures that every service executes consistently regardless of the host operating system.

Rather than installing dependencies directly on the host machine, every runtime environment is encapsulated inside a container.

The project demonstrates practical Docker usage by containerizing applications written in multiple programming languages together with multiple databases.

---

# Why Docker?

Before Docker, applications were deployed directly onto servers.

Typical problems included:

- Dependency conflicts
- Different library versions
- Different operating systems
- "Works on my machine" issues
- Difficult deployments

Docker solves these problems by packaging:

- Application
- Runtime
- Libraries
- Dependencies
- Configuration

inside a single image.

---

# Docker in OTMS

Every deployable component is containerized.

```

Frontend
↓

Docker Image

↓

Container

```

```

Employee API
↓

Docker Image

↓

Container

```

```

Attendance API
↓

Docker Image

↓

Container

```

```

Salary API
↓

Docker Image

↓

Container

```

```

Notification API
↓

Docker Image

↓

Container

```

Each service executes independently.

---

# Project Docker Images

| Image | Purpose |
|---------|----------|
| otms-frontend | React UI |
| otms-employee-api | Employee Service |
| otms-attendance-api | Attendance Service |
| otms-salary-api | Salary Service |
| otms-notification-api | Email Service |
| otms-scylla-sync | Background Worker |
| otms-scylla-init | Database Initialization |
| otms-scylla-migration | Database Migration |
| otms-attendance-migration | PostgreSQL Migration |

Infrastructure Images

| Image | Purpose |
|---------|----------|
| otms-postgres | PostgreSQL |
| otms-redis | Redis |
| otms-scylladb | ScyllaDB |
| otms-elasticsearch | Elasticsearch |

---

# Docker Build Process

The build lifecycle follows:

```

Dockerfile

↓

docker build

↓

Docker Image

↓

Docker Hub

↓

docker pull

↓

Container

```

---

# Dockerfile

Every service contains its own Dockerfile.

Example

```

Employee_API/

Dockerfile

```

This allows each microservice to be built independently.

---

# Multi-stage Builds

Several services use multi-stage builds.

Example

```

Stage 1

Compile Application

↓

Stage 2

Copy Executable

↓

Runtime Image

```

Advantages

- Smaller images
- Faster downloads
- Reduced attack surface
- Cleaner runtime

---

# Why Multi-stage?

Without multi-stage

```

Java

↓

Source

↓

Maven

↓

Compiler

↓

Application

↓

Final Image

```

Image Size

Large

---

With Multi-stage

```

Builder Image

↓

Compile

↓

JAR

↓

Copy JAR

↓

Runtime Image

```

Image Size

Much Smaller

---

# Docker Image Layers

Every Docker instruction creates a layer.

Example

```

FROM

↓

RUN

↓

COPY

↓

RUN

↓

CMD

```

Layer Stack

```

Layer 5

CMD

-----------

Layer 4

COPY

-----------

Layer 3

RUN

-----------

Layer 2

RUN

-----------

Layer 1

FROM

```

Docker reuses unchanged layers during subsequent builds.

---

# Layer Caching

Suppose only application code changes.

Docker rebuilds

```

COPY

↓

CMD

```

Earlier layers remain cached.

Benefits

- Faster builds
- Reduced downloads
- Better CI performance

---

# Base Images

The project uses lightweight base images.

Examples

```

golang

```

```

python

```

```

eclipse-temurin

```

```

nginx

```

```

alpine

```

Choosing lightweight base images reduces:

- Image size
- Download time
- Attack surface

---

# Build Context

During

```

docker build

```

Docker sends the build context to the daemon.

Example

```

Employee_API/

↓

Docker Build Context

```

Only files inside the build context are available during image creation.

---

# ENTRYPOINT

ENTRYPOINT defines the executable.

Example

```

ENTRYPOINT

↓

notification-api

```

This executable always runs.

---

# CMD

CMD provides default arguments.

Example

```

CMD

↓

--server.port=8080

```

Users may override CMD while keeping ENTRYPOINT unchanged.

---

# Why ENTRYPOINT + CMD?

ENTRYPOINT

Defines

"What to execute"

CMD

Defines

"Default parameters"

This combination provides flexibility.

---

# Environment Variables

Application configuration is injected using environment variables.

Examples

```

POSTGRES_HOST

```

```

REDIS_HOST

```

```

SMTP_SERVER

```

```

ELASTIC_HOST

```

Benefits

- Same image everywhere
- No hardcoded configuration
- Environment independent

---

# Docker Networks

Every container joins

```

otms-network

```

Communication

```

Employee API

↓

redis

```

instead of

```

localhost

```

Docker DNS resolves service names automatically.

---

# Docker Volumes

Persistent data is stored using Docker volumes.

Volumes

```

postgres-data

```

```

redis-data

```

```

scylladb-data

```

```

elasticsearch-data

```

Containers can be removed without losing database contents.

---

# Health Checks

Every critical application exposes a health endpoint.

Docker periodically verifies container health.

Example

```

Employee API

↓

/api/v1/employee/health

```

If unhealthy,

Docker Compose delays dependent services.

---

# Restart Policies

Applications use

```

restart: unless-stopped

```

Migration containers use

```

restart: "no"

```

Reason

Migration executes only once.

---

# Migration Containers

Instead of embedding database initialization inside applications,

dedicated containers perform:

```

Wait

↓

Initialize

↓

Exit

```

Benefits

- Clean architecture
- Independent migrations
- Easier debugging

---

# Image Registry

All application images are published to Docker Hub.

Namespace

```

478mkharb

```

Example

```

478mkharb/otms-employee-api

```

Deployment no longer requires rebuilding source code.

---

# Self-contained Images

The project publishes both

Application Images

and

Infrastructure Images

Examples

```

478mkharb/otms-postgres

```

```

478mkharb/otms-redis

```

```

478mkharb/otms-scylladb

```

```

478mkharb/otms-elasticsearch

```

This makes deployments independent of external image names.

---

# Build Commands

Build

```bash
docker build -t image-name .
```

Run

```bash
docker run image-name
```

List Images

```bash
docker images
```

List Containers

```bash
docker ps
```

View Logs

```bash
docker logs container-name
```

Execute Shell

```bash
docker exec -it container-name sh
```

Remove Image

```bash
docker rmi image-name
```

Remove Container

```bash
docker rm container-name
```

---

# Lessons Learned During the Project

During implementation the following practical concepts were learned:

- Multi-stage builds
- Layer caching
- Docker networking
- Volumes
- Health checks
- Environment variables
- Build context
- ENTRYPOINT vs CMD
- Docker Hub image publishing
- Self-contained infrastructure images
- Docker Compose dependency management
- Migration container pattern

---

# Best Practices Used

✔ One service per container

✔ Lightweight base images

✔ Multi-stage builds

✔ Environment variables

✔ Health checks

✔ Persistent volumes

✔ Docker Compose orchestration

✔ Image versioning support

✔ Docker Hub publishing

✔ Infrastructure separated from application containers

---

# Summary

Docker provides the execution platform for the OT-Micro-Docker project.

Every service is packaged independently, deployed consistently, isolated from other services, and distributed through Docker Hub.

This architecture enables reproducible deployments on local machines, cloud virtual machines, Kubernetes clusters, and Amazon EKS without rebuilding application source code.
