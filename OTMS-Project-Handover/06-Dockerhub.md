# 06 - Docker Hub

---

# Docker Hub

---

# Introduction

Docker Hub is the central image registry used by the OT-Micro-Docker project.

Instead of distributing application source code and requiring users to build images locally, all application and infrastructure images are published to Docker Hub.

This enables anyone with Docker installed to deploy the complete application stack without compiling any source code.

---

# Why Docker Hub?

Initially, the project deployment required users to build every Docker image locally.

Example

```bash
docker compose build

docker compose up -d
```

Although functional, this approach has several drawbacks.

- Long build times
- Requires source code
- Requires Dockerfiles
- Requires build dependencies
- Different build environments may produce inconsistent results

Publishing images to Docker Hub eliminates these problems.

---

# Deployment Before Docker Hub

```
GitHub

↓

Clone Repository

↓

Docker Build

↓

Create Images

↓

Run Containers
```

---

# Deployment After Docker Hub

```
GitHub

↓

Clone Repository

↓

Docker Compose

↓

Docker Pull

↓

Run Containers
```

No image build is required.

---

# Docker Hub Repository

Namespace

```
478mkharb
```

All project images are stored under this namespace.

---

# Application Images

| Repository | Purpose |
|------------|----------|
| 478mkharb/otms-employee-api | Employee API |
| 478mkharb/otms-attendance-api | Attendance API |
| 478mkharb/otms-salary-api | Salary API |
| 478mkharb/otms-notification-api | Notification API |
| 478mkharb/otms-frontend | React Frontend |
| 478mkharb/otms-scylla-sync | Background Worker |
| 478mkharb/otms-scylla-init | Scylla Initialization |
| 478mkharb/otms-scylla-migration | Scylla Migration |
| 478mkharb/otms-attendance-migration | Attendance Migration |

---

# Infrastructure Images

The project also publishes customized infrastructure images.

| Repository | Purpose |
|------------|----------|
| 478mkharb/otms-postgres | PostgreSQL |
| 478mkharb/otms-redis | Redis |
| 478mkharb/otms-scylladb | ScyllaDB |
| 478mkharb/otms-elasticsearch | Elasticsearch |

Publishing infrastructure images makes the deployment completely self-contained.

---

# Why Publish Infrastructure Images?

Using official images directly is perfectly valid.

Example

```yaml
image: postgres:16-alpine
```

However, the OTMS project uses customized images.

Example

```yaml
image: 478mkharb/otms-postgres:latest
```

Advantages

- Fully self-contained deployment
- Future customizations are preserved
- Same image across all environments
- Version control over infrastructure

---

# Image Naming Convention

The project follows a consistent naming strategy.

```
<dockerhub-user>/<project>-<service>:<tag>
```

Example

```
478mkharb/otms-employee-api:latest
```

---

# Why Consistent Naming?

Consistent naming improves

- Readability
- Automation
- CI/CD integration
- Kubernetes deployments
- Image management

---

# Image Tags

Current tag

```
latest
```

Example

```
478mkharb/otms-frontend:latest
```

---

# Future Versioning Strategy

Instead of only using

```
latest
```

future releases can use semantic versioning.

Examples

```
v1.0.0

v1.1.0

v1.2.0

v2.0.0
```

This enables predictable deployments.

---

# Build Workflow

Every image follows the same lifecycle.

```
Source Code

↓

Dockerfile

↓

docker build

↓

Docker Image

↓

docker tag

↓

docker push

↓

Docker Hub
```

---

# Building an Image

Example

```bash
docker build -t otms-employee-api .
```

Docker creates a local image.

---

# Tagging an Image

Before pushing to Docker Hub the image must be tagged.

Example

```bash
docker tag \
otms-employee-api:latest \
478mkharb/otms-employee-api:latest
```

The tag associates the image with the Docker Hub repository.

---

# Logging Into Docker Hub

To push images the user must authenticate.

```bash
docker login
```

Successful login allows

- docker push
- docker pull (private repositories)

Public repositories do not require authentication for pulling images.

---

# Pushing an Image

Example

```bash
docker push \
478mkharb/otms-employee-api:latest
```

Docker uploads all image layers to Docker Hub.

Only changed layers are uploaded.

---

# Layer Reuse

Docker images consist of layers.

If two images share common layers

```
Employee API

↓

Java Runtime
```

and

```
Salary API

↓

Java Runtime
```

Docker uploads the shared layer only once.

Benefits

- Faster pushes
- Lower bandwidth
- Smaller storage

---

# Pulling Images

Images can be downloaded using

```bash
docker pull \
478mkharb/otms-employee-api:latest
```

If the image already exists locally and is up-to-date,

Docker reuses it.

---

# Docker Compose Integration

Instead of

```yaml
build:
  context: ./Employee_API
```

the compose file now uses

```yaml
image:
  478mkharb/otms-employee-api:latest
```

Docker Compose automatically performs

```
Image Missing

↓

docker pull

↓

Create Container

↓

Start Container
```

No manual pull is required.

---

# Public Repositories

All OTMS repositories are public.

Therefore

Users do NOT need

```bash
docker login
```

to deploy the project.

A simple

```bash
docker compose up -d
```

automatically downloads all required images.

---

# Updating Images

Suppose the Employee API changes.

Workflow

```
Modify Source

↓

docker build

↓

docker tag

↓

docker push

↓

Docker Hub Updated
```

Users update by executing

```bash
docker compose pull

docker compose up -d
```

---

# Image Distribution

```
Developer

↓

Docker Build

↓

Docker Hub

↓

Developer Laptop

↓

AWS EC2

↓

Minikube

↓

Amazon EKS
```

The same image runs everywhere.

---

# Benefits

Publishing images provides

✔ Faster deployment

✔ No compilation

✔ No Docker build

✔ Smaller CI pipelines

✔ Production-like workflow

✔ Better portability

✔ Consistent runtime

---

# Common Commands

Login

```bash
docker login
```

Logout

```bash
docker logout
```

Build

```bash
docker build -t image-name .
```

Tag

```bash
docker tag image-name username/image-name:latest
```

Push

```bash
docker push username/image-name:latest
```

Pull

```bash
docker pull username/image-name:latest
```

List Images

```bash
docker images
```

Remove Local Image

```bash
docker rmi image-name
```

---

# Common Issues

## Access Denied

Cause

```
Not logged in
```

Solution

```bash
docker login
```

---

## Repository Does Not Exist

Cause

Repository name is incorrect.

Verify

```
username/repository
```

---

## Permission Denied

Cause

Trying to push to another user's repository.

Solution

Push only to repositories you own or have access to.

---

## Image Not Updating

Cause

Old local image.

Solution

```bash
docker compose pull

docker compose up -d
```

---

# Future Improvements

The Docker Hub workflow is designed to integrate with CI/CD.

Future pipeline

```
Git Commit

↓

GitHub Actions / Jenkins

↓

Docker Build

↓

Docker Push

↓

Docker Hub

↓

Deploy
```

This enables automated image publishing.

---

# Summary

Docker Hub serves as the central image registry for the OT-Micro-Docker project.

Publishing both application and infrastructure images provides a self-contained deployment model that requires no local image builds, simplifies distribution, and prepares the project for deployment on Docker Compose, Kubernetes, Minikube, and Amazon EKS.
