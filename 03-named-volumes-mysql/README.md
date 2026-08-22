# 03 - Named Volumes with MySQL

A production-style FastAPI project demonstrating how **Docker Named Volumes** keep database data persistent even after containers are recreated.

This project also introduces a scalable FastAPI folder structure, environment-based configuration, and Docker Compose with health checks.

---

## Learning Objectives

By the end of this project, you'll understand:

- Docker Named Volumes
- FastAPI production folder structure
- Environment variables with `.env`
- Docker Compose for multi-container applications
- MySQL integration
- Health checks
- Service-based application architecture

---

## Tech Stack

| Technology | Version |
|------------|----------|
| Python | 3.12 |
| FastAPI | 0.141.1 |
| Uvicorn | 0.52.4 |
| MySQL Connector | 9.7.0 |
| MySQL | 9.7 |
| Docker | Latest |
| Docker Compose | Latest |

---

## Project Structure

```text
03-named-volumes-mysql/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── routes.py
│   ├── core/
│   │   └── database.py
│   ├── schemas/
│   │   └── task.py
│   └── services/
│       └── task_service.py
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
├── .dockerignore
├── requirements.txt
└── README.md
```

---

## Architecture

```
                    Browser / API Client
                           │
                           ▼
                  localhost:8000
                           │
                           ▼
              FastAPI (Docker Container)
                           │
                 Docker Bridge Network
                           │
                           ▼
               MySQL (Docker Container)
                           │
                           ▼
            Named Volume (mysql_data)
```

---

## What You'll Learn in Project 03

| Feature | Purpose |
|---------|---------|
| Named Volume | Persistent database storage |
| `.env` | Environment-based configuration |
| Docker Compose | Multi-container orchestration |
| Health Checks | Safe startup sequencing |
| Layered Architecture | Production-ready code organization |

---

# Environment Variables

## `.env.example`

```env
MYSQL_HOST=mysql
MYSQL_DATABASE=tasksdb
MYSQL_USER=appuser
MYSQL_PASSWORD=your_password
MYSQL_ROOT_PASSWORD=your_root_password
```

Create your local file:

```bash
cp .env.example .env
```

---

# Docker Compose

```yaml
services:
  api:
    env_file:
      - .env

  mysql:
    env_file:
      - .env
    volumes:
      - mysql_data:/var/lib/mysql
```

---

# Running the Project

## Step 1

```bash
cp .env.example .env
```

## Step 2

```bash
docker compose up --build
```

FastAPI waits until MySQL becomes healthy before starting.

---

## Available Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/` | Welcome |
| `/health` | Health check |
| `/docs` | Swagger UI |
| `/tasks` | List tasks |
| `POST /tasks` | Create task |

---

# Testing

Create a task.

```bash
curl -X POST http://localhost:8000/tasks \
-H "Content-Type: application/json" \
-d '{"title":"Learn Docker Named Volumes"}'
```

List tasks.

```bash
curl http://localhost:8000/tasks
```

---

## Verify Persistence

Stop everything.

```bash
docker compose down
```

Start again.

```bash
docker compose up
```

Your task still exists because MySQL stores data inside the **named volume**.

---

# Useful Docker Commands

```bash
docker volume ls
docker volume inspect mysql_data
docker compose logs
docker ps
docker images
```

---

# Named Volume vs Bind Mount

| Named Volume | Bind Mount |
|--------------|-----------|
| Managed by Docker | Uses host folder |
| Ideal for databases | Ideal for source code |
| Survives container recreation | Mirrors local files |

---

# Common Issues

## MySQL isn't ready

The project already includes:

- Health checks
- `depends_on`
- Startup sequencing

---

## `.env` missing

Create it first.

```bash
cp .env.example .env
```

---

# Questions

### Why use Named Volumes for databases?

They preserve database files even when containers are recreated.

### Why use `.env`?

It separates configuration from source code.

### Why use a layered FastAPI structure?

It separates routing, business logic, schemas, and database access, making the application easier to maintain.

### Why use `lifespan`?

It is the modern FastAPI lifecycle API and avoids deprecated startup/shutdown event hooks.

---

# Docker Image Size Comparison

A multi-stage Docker build reduces the final image size by copying only the app runtime dependencies and code into the final stage.

```text
REPOSITORY                               TAG       IMAGE ID       CREATED          SIZE
04-multi-stage-build_api                 latest    16aa978c5563   30 minutes ago   201MB
03-named-volumes-mysql_api               latest    7b5840a720d9   4 hours ago      209MB
```

This shows a reduction of about 8MB:

- Before: 209MB
- After: 201MB

That improvement comes from using a leaner final image and avoiding unnecessary build dependencies in the runtime stage.

---

# Skills Demonstrated

- Docker Named Volumes
- Docker Compose
- Environment Variable Management
- FastAPI Architecture
- MySQL Integration
- Health Checks
- Service Layer Pattern
- Modern FastAPI

