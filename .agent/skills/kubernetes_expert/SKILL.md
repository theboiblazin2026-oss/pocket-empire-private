---
name: Kubernetes Expert
description: Pods, deployments, services, Helm charts, and cluster management
---

# Kubernetes Expert Skill

## Core Concepts

| Resource | Purpose |
|----------|---------|
| Pod | Smallest deployable unit (1+ containers) |
| Deployment | Manages pod replicas, rolling updates |
| Service | Stable networking for pods |
| ConfigMap | Non-sensitive config data |
| Secret | Sensitive data (base64 encoded) |
| Ingress | External HTTP routing |

## Essential Commands

```bash
# Get resources
kubectl get pods
kubectl get deployments
kubectl get services

# Describe (debug)
kubectl describe pod <name>

# Logs
kubectl logs <pod> -f

# Shell into pod
kubectl exec -it <pod> -- /bin/sh

# Apply config
kubectl apply -f deployment.yaml

# Scale
kubectl scale deployment <name> --replicas=3
```

## Deployment YAML

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:1.0
        ports:
        - containerPort: 3000
        resources:
          limits:
            memory: "256Mi"
            cpu: "500m"
```

## Service Types

| Type | Use Case |
|------|----------|
| ClusterIP | Internal only (default) |
| NodePort | External via node port |
| LoadBalancer | Cloud load balancer |

## Helm Basics

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install my-release bitnami/postgresql
helm upgrade my-release bitnami/postgresql
helm rollback my-release 1
```

## When to Apply
Use when deploying to Kubernetes, debugging pods, or designing cluster architecture.
