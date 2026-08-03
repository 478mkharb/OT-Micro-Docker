# 12 - Kubernetes

---

# Kubernetes Deployment

---

# Introduction

Docker Compose is an excellent solution for local development and small deployments. However, as applications grow, requirements such as high availability, auto-scaling, rolling updates, and self-healing become essential.

Kubernetes is an orchestration platform designed to manage containerized applications at scale.

The OT-Micro-Docker platform has been designed with Kubernetes compatibility in mind, making the transition from Docker Compose straightforward.

---

# Why Kubernetes?

Docker Compose manages containers on a single machine.

Kubernetes manages containers across one or more machines (nodes).

It provides:

- Self-healing
- Auto-scaling
- Load balancing
- Rolling updates
- Service discovery
- Secret management
- Persistent storage
- High availability

---

# Docker Compose vs Kubernetes

| Docker Compose | Kubernetes |
|----------------|------------|
| Service | Deployment + Service |
| Network | Cluster Networking |
| Volume | Persistent Volume |
| Environment | ConfigMap / Secret |
| Restart Policy | Pod Restart Policy |
| depends_on | Readiness/Liveness Probes |
| Single Host | Multi-Node Cluster |

---

# Kubernetes Architecture

```
                    kubectl
                       │
                       ▼

             Kubernetes API Server
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼

 Scheduler      Controller Manager    etcd

                       │
                       ▼

                 Worker Nodes

        ┌──────────────┼──────────────┐
        ▼              ▼              ▼

      Pod           Pod           Pod

```

---

# OTMS on Kubernetes

```
                     Ingress

                         │

                Frontend Service

                         │

          ┌──────────────┼──────────────┐

          ▼              ▼              ▼

Employee API     Attendance API    Salary API

          │              │              │

          ▼              ▼              ▼

     ScyllaDB      PostgreSQL      Redis

                         │

                         ▼

                  Elasticsearch

                         │

                         ▼

                 Notification API

                         │

                         ▼

                    Scylla Sync
```

---

# Kubernetes Objects

The OTMS deployment uses the following Kubernetes resources.

| Resource | Purpose |
|----------|----------|
| Namespace | Resource isolation |
| Deployment | Application Pods |
| StatefulSet | Databases |
| Service | Internal communication |
| ConfigMap | Configuration |
| Secret | Credentials |
| PersistentVolume | Storage |
| PersistentVolumeClaim | Volume requests |
| Ingress | External access |
| HorizontalPodAutoscaler | Auto Scaling |

---

# Namespace

All OTMS resources should be deployed inside a dedicated namespace.

Example

```yaml
apiVersion: v1

kind: Namespace

metadata:
  name: otms
```

Benefits

- Resource isolation
- Easier administration
- Cleaner organization

---

# Pods

Every container executes inside a Pod.

Examples

```
employee-api Pod

attendance-api Pod

salary-api Pod

frontend Pod
```

---

# Deployments

Application services use Deployments.

Examples

```
Employee API

Attendance API

Salary API

Notification API

Frontend

Scylla Sync
```

Deployment Features

- Rolling updates
- Rollback
- Replica management
- Self-healing

---

# StatefulSets

Databases should use StatefulSets instead of Deployments.

Applies to

```
PostgreSQL

Redis

ScyllaDB

Elasticsearch
```

Reasons

- Stable identity
- Persistent storage
- Ordered startup
- Stable network names

---

# Services

Every Deployment is exposed using a Kubernetes Service.

Example

```
employee-api

↓

ClusterIP Service

↓

employee-api.otms.svc.cluster.local
```

---

# Service Types

| Type | Purpose |
|-------|----------|
| ClusterIP | Internal communication |
| NodePort | Development |
| LoadBalancer | Cloud |
| Headless | StatefulSets |

---

# ConfigMaps

Application configuration should not be stored inside Docker images.

Example

```
POSTGRES_HOST

REDIS_HOST

SMTP_SERVER

ELASTIC_HOST
```

These values belong inside ConfigMaps.

---

# Secrets

Sensitive values should be stored in Kubernetes Secrets.

Examples

```
SMTP_PASSWORD

Database Passwords

Redis Password

JWT Secret
```

Secrets are mounted into Pods as environment variables or files.

---

# Persistent Storage

Databases require persistent storage.

```
PersistentVolume

↓

PersistentVolumeClaim

↓

Pod
```

Volumes survive Pod restarts.

---

# Health Probes

Docker health checks become Kubernetes probes.

---

## Liveness Probe

Determines whether the application should be restarted.

Example

```
GET

/api/v1/employee/health
```

---

## Readiness Probe

Determines whether the application is ready to receive traffic.

Traffic is routed only after the readiness probe succeeds.

---

# Resource Requests and Limits

Each Deployment should define CPU and memory resources.

Example

```yaml
resources:

  requests:

    cpu: "250m"

    memory: "256Mi"

  limits:

    cpu: "500m"

    memory: "512Mi"
```

Benefits

- Prevent resource starvation
- Better scheduling
- Cluster stability

---

# Ingress

Instead of exposing multiple NodePorts,

Ingress provides a single entry point.

```
Browser

↓

Ingress

↓

Frontend

↓

APIs
```

Benefits

- One external IP
- HTTPS support
- URL routing

---

# Horizontal Pod Autoscaler

Kubernetes can automatically scale applications.

Example

```
Employee API

2 Pods

↓

High CPU

↓

5 Pods
```

Scaling is automatic based on metrics.

---

# Rolling Updates

Deployments support zero-downtime updates.

```
Version 1

↓

Create Version 2

↓

Health Check

↓

Switch Traffic

↓

Delete Version 1
```

---

# Rollback

If deployment fails

```
Version 2

↓

Rollback

↓

Version 1
```

No manual recovery is required.

---

# Service Discovery

Applications communicate using Kubernetes DNS.

Example

```
employee-api

↓

employee-api.otms.svc.cluster.local
```

Instead of

```
localhost
```

---

# Environment Variables

Environment variables are injected from ConfigMaps and Secrets.

Applications remain identical to Docker Compose.

No code changes are required.

---

# OTMS Deployment Order

```
Namespace

↓

Persistent Volumes

↓

Persistent Volume Claims

↓

ConfigMaps

↓

Secrets

↓

StatefulSets

↓

Deployments

↓

Services

↓

Ingress

↓

HPA
```

---

# Mapping Docker Compose to Kubernetes

| Docker Compose | Kubernetes |
|----------------|------------|
| image | Deployment |
| ports | Service |
| volumes | PVC |
| environment | ConfigMap / Secret |
| healthcheck | Liveness & Readiness Probes |
| restart | Deployment Controller |
| network | Cluster Networking |
| depends_on | Readiness Probes |

---

# Minikube Deployment

For local Kubernetes development:

```bash
minikube start
```

Load images (if not pulling from Docker Hub)

```bash
minikube image load 478mkharb/otms-employee-api:latest
```

Apply manifests

```bash
kubectl apply -f k8s/
```

Verify Pods

```bash
kubectl get pods
```

Verify Services

```bash
kubectl get svc
```

---

# Monitoring on Kubernetes

The same monitoring stack can be deployed using Helm.

Components

- Prometheus
- Grafana
- Loki
- Tempo
- Alertmanager
- OpenTelemetry Collector

No application code changes are required.

---

# Best Practices

The OTMS Kubernetes deployment follows these principles:

- One Deployment per microservice
- StatefulSets for databases
- ConfigMaps for configuration
- Secrets for sensitive data
- Health probes for all services
- Resource requests and limits
- Persistent volumes for databases
- Rolling updates
- Auto-scaling
- Namespace isolation

---

# Future Enhancements

Future Kubernetes improvements include:

- Helm Charts
- GitOps with Argo CD
- Service Mesh (Istio or Linkerd)
- Network Policies
- Pod Disruption Budgets
- Vertical Pod Autoscaler
- Multi-node deployment
- Blue-Green and Canary deployments

---

# Lessons Learned

Preparing OTMS for Kubernetes reinforced several key concepts:

- Stateless application design
- Externalized configuration
- Database persistence
- Health-aware deployments
- Service discovery
- Declarative infrastructure
- Container portability

---

# Summary

The OT-Micro-Docker platform is designed to transition seamlessly from Docker Compose to Kubernetes. By using containerized microservices, environment-based configuration, persistent storage, and health checks, the application aligns with Kubernetes best practices.

Deploying OTMS on Kubernetes provides high availability, scalability, self-healing, and production-grade orchestration while preserving the same application images used in Docker Compose.
