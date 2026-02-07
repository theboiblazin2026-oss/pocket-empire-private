---
name: Docker Pro
description: Container best practices, multi-stage builds, and Docker Compose patterns
---

# Docker Pro Skill

## Dockerfile Best Practices

### Multi-Stage Build
```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### Layer Optimization
```dockerfile
# ❌ Bad (cache busted on any change)
COPY . .
RUN npm install

# ✅ Good (dependencies cached)
COPY package*.json ./
RUN npm ci
COPY . .
```

## Docker Compose

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://db:5432/app
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}

volumes:
  postgres_data:
```

## Common Commands

| Task | Command |
|------|---------|
| Build image | `docker build -t app:latest .` |
| Run container | `docker run -d -p 3000:3000 app` |
| View logs | `docker logs -f <container>` |
| Shell into container | `docker exec -it <container> sh` |
| Clean up | `docker system prune -a` |
| Compose up | `docker compose up -d` |
| Compose down | `docker compose down -v` |

## Networking

| Network Type | Use Case |
|--------------|----------|
| bridge | Default, container-to-container on same host |
| host | Direct host network (no isolation) |
| none | No networking |

## When to Apply
Use when writing Dockerfiles, debugging containers, or setting up development environments.
