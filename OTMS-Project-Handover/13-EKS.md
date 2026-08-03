# 13 - Amazon Elastic Kubernetes Service (EKS)

---

# Amazon EKS Deployment

---

# Introduction

Amazon Elastic Kubernetes Service (Amazon EKS) is a managed Kubernetes service provided by AWS. It removes the operational overhead of installing, upgrading, and managing the Kubernetes control plane while allowing users to focus on deploying and operating applications.

The OT-Micro-Docker platform has been designed with cloud-native principles, making it suitable for deployment on Amazon EKS with minimal application changes.

---

# Why Amazon EKS?

While Docker Compose is ideal for local development and Kubernetes is suitable for self-managed clusters, Amazon EKS provides a fully managed Kubernetes control plane with built-in AWS integrations.

Advantages include:

- Managed Kubernetes control plane
- High availability
- Automatic control plane upgrades
- Native AWS integration
- IAM authentication
- Elastic Load Balancing
- Persistent storage using Amazon EBS
- CloudWatch integration
- Auto Scaling

---

# High-Level Architecture

```
                    Internet
                        │
                        ▼
             AWS Application Load Balancer
                        │
                        ▼
               AWS Load Balancer Controller
                        │
                        ▼
                   Kubernetes Ingress
                        │
                        ▼
                   Frontend Service
                        │
     ┌──────────────────┼──────────────────┐
     ▼                  ▼                  ▼

 Employee API     Attendance API     Salary API
        │               │                 │
        ▼               ▼                 ▼

   ScyllaDB      PostgreSQL         Redis

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

# EKS Architecture

```
AWS Account

↓

VPC

↓

Public Subnets

↓

Private Subnets

↓

Amazon EKS Cluster

↓

Managed Node Group

↓

Pods

↓

Persistent Storage
```

---

# Core AWS Services

| AWS Service | Purpose |
|-------------|----------|
| Amazon EKS | Kubernetes Control Plane |
| EC2 | Worker Nodes |
| VPC | Networking |
| IAM | Authentication & Authorization |
| EBS | Persistent Volumes |
| ALB | External Traffic |
| Route53 | DNS |
| CloudWatch | Monitoring |
| ECR *(Optional)* | Container Registry |

---

# Recommended VPC Design

```
VPC

10.0.0.0/16

│

├── Public Subnet A

├── Public Subnet B

├── Private Subnet A

├── Private Subnet B
```

---

## Public Subnets

Used for

- Application Load Balancer
- NAT Gateway

---

## Private Subnets

Used for

- Worker Nodes
- Application Pods
- Databases

No application workload should be directly exposed to the Internet.

---

# EKS Cluster Components

## Control Plane

Managed by AWS.

Includes

- API Server
- Scheduler
- Controller Manager
- etcd

Users do not manage these components.

---

## Worker Nodes

Managed Node Groups host application Pods.

Recommended Instance Types

```
t3.large

t3.xlarge
```

depending on workload.

---

# IAM Roles

Several IAM roles are required.

## Cluster Role

Allows EKS to manage the control plane.

---

## Node Group Role

Allows worker nodes to:

- Pull container images
- Mount EBS volumes
- Send logs
- Join the cluster

---

## Load Balancer Controller Role

Allows Kubernetes to create:

- Application Load Balancers
- Target Groups
- Security Groups

---

# Container Images

OTMS images can be pulled directly from Docker Hub.

Example

```yaml
image:

478mkharb/otms-employee-api:latest
```

Alternatively, images can be mirrored to Amazon ECR.

---

# Storage

Application Pods remain stateless.

Persistent storage is required only for databases.

| Database | Storage |
|-----------|---------|
| PostgreSQL | Amazon EBS |
| ScyllaDB | Amazon EBS |
| Elasticsearch | Amazon EBS |
| Redis | Amazon EBS (optional persistence) |

---

# Persistent Volume Flow

```
Pod

↓

PersistentVolumeClaim

↓

PersistentVolume

↓

Amazon EBS Volume
```

---

# Ingress

Traffic enters the cluster through Kubernetes Ingress.

```
Internet

↓

Application Load Balancer

↓

Ingress

↓

Frontend

↓

Microservices
```

---

# Internal Communication

Pods communicate using Kubernetes Services.

Example

```
employee-api

↓

employee-api.otms.svc.cluster.local
```

---

# Secrets Management

Sensitive values should never be stored in manifests.

Examples

- SMTP Password
- Database Passwords
- JWT Secret
- API Keys

Options

- Kubernetes Secrets
- AWS Secrets Manager

---

# Configuration

Application configuration should be stored in ConfigMaps.

Examples

- Database host
- Redis host
- Elasticsearch endpoint
- SMTP server

---

# Load Balancing

External traffic

```
Internet

↓

Application Load Balancer

↓

Frontend Pods
```

Internal traffic

```
Frontend

↓

ClusterIP Services

↓

Application Pods
```

---

# Auto Scaling

## Horizontal Pod Autoscaler

Automatically increases or decreases Pod replicas.

Example

```
Employee API

2 Pods

↓

High CPU

↓

5 Pods
```

---

## Cluster Autoscaler

Automatically adds or removes EC2 worker nodes.

```
Pods Pending

↓

Cluster Autoscaler

↓

New EC2 Node

↓

Pods Scheduled
```

---

# Rolling Updates

Deployments are updated without downtime.

```
Version 1

↓

Deploy Version 2

↓

Readiness Check

↓

Traffic Switch

↓

Remove Version 1
```

---

# Monitoring

The monitoring stack remains unchanged.

Components

- Prometheus
- Grafana
- Loki
- Tempo
- OpenTelemetry Collector
- Alertmanager

These can be deployed using Helm charts.

---

# Logging

Application logs can be shipped to

- Loki
- CloudWatch Logs

Both approaches are supported.

---

# CI/CD Pipeline

A recommended deployment pipeline is

```
Developer

↓

Git Push

↓

GitHub

↓

GitHub Actions / Jenkins

↓

Docker Build

↓

Docker Hub

↓

kubectl apply

↓

Amazon EKS
```

---

# Security Best Practices

- Deploy workloads in private subnets.
- Use IAM Roles for Service Accounts (IRSA).
- Store secrets in AWS Secrets Manager or Kubernetes Secrets.
- Restrict security groups to required ports.
- Enable TLS for Ingress.
- Apply Network Policies.
- Enable Kubernetes RBAC.

---

# High Availability

To achieve high availability:

- Deploy worker nodes across multiple Availability Zones.
- Use multiple Pod replicas.
- Configure Pod anti-affinity.
- Use managed node groups.
- Use multiple public and private subnets.

---

# Cost Optimization

Recommended practices include:

- Use Cluster Autoscaler.
- Right-size EC2 instances.
- Use Spot Instances for non-critical workloads.
- Scale idle workloads to zero where possible.
- Monitor resource utilization with Prometheus and Grafana.

---

# Migration from Docker Compose

The migration path is straightforward.

| Docker Compose | Amazon EKS |
|----------------|------------|
| Compose File | Kubernetes Manifests |
| Bridge Network | Kubernetes Networking |
| Volumes | EBS-backed PVCs |
| Environment Variables | ConfigMaps & Secrets |
| Health Checks | Liveness & Readiness Probes |
| Docker Hub Images | Same Docker Hub Images |

No application code changes are required.

---

# Future Enhancements

Potential improvements for the OTMS platform on EKS include:

- Helm Charts
- GitOps using Argo CD
- AWS Secrets Manager integration
- ExternalDNS
- AWS Certificate Manager (ACM)
- Service Mesh (Istio or Linkerd)
- Karpenter for node provisioning
- Blue-Green Deployments
- Canary Deployments

---

# Lessons Learned

Preparing OTMS for Amazon EKS reinforced several cloud-native principles:

- Stateless application design
- Externalized configuration
- Infrastructure as Code
- Immutable container images
- Managed orchestration
- Cloud-native networking
- Scalable microservices
- Automated deployments

---

# Summary

Amazon EKS provides a production-ready Kubernetes platform for deploying the OT-Micro-Docker application. By combining managed Kubernetes, AWS networking, persistent storage, auto-scaling, and observability, OTMS can run as a resilient, scalable, and cloud-native application.

Because the project already follows containerization best practices, migrating from Docker Compose to Amazon EKS primarily involves replacing Docker Compose with Kubernetes manifests while reusing the same Docker images and application configuration strategy.
