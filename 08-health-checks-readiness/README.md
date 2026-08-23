# 08 - Health Checks & Readiness

This project builds on **Project 07** and introduces **production-grade health monitoring** using **Docker Health Checks**, **FastAPI liveness and readiness endpoints**, and **startup sequencing**.

Instead of assuming that a running container is ready to serve requests, Docker now verifies that services are actually healthy before allowing dependent services to continue.

This is a fundamental concept used in Docker Compose, Kubernetes, and modern production deployments.

---

## Learning Objectives

By the end of this project, you'll understand:

- Docker Health Checks
- Liveness vs Readiness
- Startup sequencing
- `depends_on: condition: service_healthy`
- Application lifecycle management
- Production monitoring basics
- Why "Running" does not always mean "Ready"

---

## Tech Stack

| Technology | Version |
|------------|----------|
| Python | 3.12 |
| FastAPI | 0.141.1 |
| Uvicorn | 0.52.4 |
| MySQL Connector | 9.7.0 |
| Pydantic Settings | 2.11.0 |
| MySQL | 9.7 |
| Nginx | 1.29 (Alpine) |
| Docker | Latest |
| Docker Compose | Latest |

---

## Project Structure

```text
08-health-checks-readiness/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   └── routes.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── schemas/
│   │   └── task.py
│   └── services/
│       └── task_service.py
├── nginx/
│   └── nginx.conf
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .dockerignore
├── requirements.txt
└── README.md
```

---

# Architecture

## Production Startup Flow

```text
                 Browser / API Client
                        │
                        ▼
                Nginx Container
                 (Waits for API)
                        │
                backend-network
                        │
                        ▼
                FastAPI Container
         Liveness • Readiness • Health
                        │
                        ▼
                MySQL Container
            Health Check Required
                        │
                        ▼
             Named Volume (mysql_data)
```

### Startup Flow

1. Docker starts the MySQL container.
2. Docker repeatedly checks MySQL's health.
3. FastAPI waits until MySQL becomes healthy.
4. FastAPI completes startup (`lifespan`).
5. FastAPI reports **Ready**.
6. Nginx begins forwarding traffic.

This prevents users from reaching an application that is still initializing.

---

# What's New Compared to Project 07

| Project 07 | Project 08 |
|------------|------------|
| Reverse Proxy | Health Monitoring |
| Basic startup | Verified startup |
| Request forwarding | Liveness & Readiness |
| Service dependency | Health-aware dependency |
| Running containers | Healthy containers |

The application still behaves the same.

The difference is that startup is now **verified**, not assumed.

---

# Why Health Checks Matter

A container can be:

- Running
- Broken
- Waiting for a database
- Still loading configuration

Without health checks, Docker only knows whether the process exists.

With health checks, Docker knows whether the application is actually working.

---

# Docker Health Check

The API container includes:

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"
```

Docker periodically requests:

```text
GET /health
```

If the request succeeds:

- Container becomes **healthy**

If it repeatedly fails:

- Container becomes **unhealthy**

---

# FastAPI Health Endpoints

This project introduces three production-style endpoints.

| Endpoint | Purpose |
|----------|---------|
| `/health` | General health |
| `/live` | Liveness |
| `/ready` | Readiness |

Each serves a different purpose.

---

## `/health`

General application status.

```bash
curl http://localhost/health
```

Response.

```json
{
  "status": "healthy"
}
```

Used by Docker's health check.

---

## `/live`

Liveness answers one question:

> Is the application process still alive?

```bash
curl http://localhost/live
```

Response.

```json
{
  "status": "alive"
}
```

A dead process should be restarted.

---

## `/ready`

Readiness answers a different question.

> Is the application ready to receive traffic?

During startup:

```text
503 Service Unavailable
```

After initialization:

```json
{
  "status": "ready"
}
```

This prevents traffic from reaching an application that hasn't finished connecting to MySQL.

---

# Startup Sequencing

MySQL becomes healthy first.

```yaml
depends_on:
  mysql:
    condition: service_healthy
```

FastAPI waits.

After FastAPI becomes healthy:

```yaml
depends_on:
  api:
    condition: service_healthy
```

Nginx starts serving traffic.

This creates a reliable startup order.

---

# Running the Project

## Step 1

Create the environment file.

```bash
cp .env.example .env
```

## Step 2

Start everything.

```bash
docker compose up --build
```

Docker creates:

- backend-network
- mysql_data
- MySQL
- FastAPI
- Nginx

---

# Checking Container Health

List running containers.

```bash
docker ps
```

Example.

```text
NAME           STATUS
fastapi-api    Up (healthy)
mysql          Up (healthy)
fastapi-nginx  Up
```

Notice the API and MySQL show **healthy**, not just **Up**.

---

# Available Endpoints

Access everything through Nginx.

| URL | Purpose |
|-----|---------|
| `http://localhost/` | Welcome |
| `http://localhost/health` | Health |
| `http://localhost/live` | Liveness |
| `http://localhost/ready` | Readiness |
| `http://localhost/docs` | Swagger UI |
| `http://localhost/proxy-info` | Proxy details |
| `http://localhost/tasks` | Task API |

---

# Testing

## Health

```bash
curl http://localhost/health
```

Expected.

```json
{
  "status": "healthy"
}
```

---

## Liveness

```bash
curl http://localhost/live
```

Expected.

```json
{
  "status": "alive"
}
```

---

## Readiness

```bash
curl http://localhost/ready
```

If startup finished:

```json
{
  "status": "ready"
}
```

Otherwise:

```text
503 Service Unavailable
```

---

## Create a Task

```bash
curl -X POST http://localhost/tasks \
-H "Content-Type: application/json" \
-d '{"title":"Learn Docker Health Checks"}'
```

---

## List Tasks

```bash
curl http://localhost/tasks
```

Health monitoring doesn't change application behavior.

It improves deployment reliability.

---

# Inspecting Health Status

Inspect a container.

```bash
docker inspect fastapi-api
```

Look for:

```text
State.Health
```

Example.

```text
healthy
```

This is how Docker tracks container health internally.

---

# Useful Docker Commands

Start.

```bash
docker compose up --build
```

Stop.

```bash
docker compose down
```

View running containers.

```bash
docker ps
```

View API logs.

```bash
docker compose logs api
```

View MySQL logs.

```bash
docker compose logs mysql
```

Inspect health.

```bash
docker inspect fastapi-api
```

---

# Running vs Healthy

| Running | Healthy |
|----------|---------|
| Process exists | Application works |
| Doesn't verify functionality | Endpoint responds successfully |
| Can still fail requests | Ready for traffic |

This distinction becomes extremely important in production.

---

# Liveness vs Readiness

| Liveness | Readiness |
|-----------|-----------|
| Is the process alive? | Is it ready for traffic? |
| Detects crashes | Detects initialization |
| May trigger restart | Delays traffic |
| Runtime check | Startup check |

Kubernetes uses these concepts extensively.

Learning them now makes Project 12 much easier.

---

# Common Issues

## Container stuck as `starting`

Inspect.

```bash
docker inspect fastapi-api
```

Check:

```text
State.Health
```

The health check may still be running.

---

## `/ready` returns 503

This usually means:

- MySQL isn't ready.
- FastAPI hasn't completed startup.

Wait until initialization finishes.

---

## API unhealthy

View logs.

```bash
docker compose logs api
```

Common causes:

- MySQL credentials
- Database unavailable
- Startup exception

---

## Nginx shows 502

This usually means FastAPI hasn't become healthy yet.

Check.

```bash
docker compose logs nginx
docker compose logs api
```

---

# Questions

### Why use Docker Health Checks?

They verify that a service is actually working—not merely running.

---

### What's the difference between Running and Healthy?

A running process may still fail requests.

A healthy container has successfully passed its health checks.

---

### What is Liveness?

Liveness determines whether the application process is still alive.

---

### What is Readiness?

Readiness determines whether the application is prepared to receive traffic.

---

### Why use `condition: service_healthy`?

It prevents dependent services from starting before required services are actually ready.

---

### Does Docker automatically restart unhealthy containers?

Not by health checks alone.

A restart policy is still required.

Health checks only report container health.

---

# Skills Demonstrated

- Docker Health Checks
- Liveness Probes
- Readiness Checks
- Startup Sequencing
- FastAPI Lifecycle
- Production Monitoring
- Docker Compose Best Practices
- Container Health Inspection
