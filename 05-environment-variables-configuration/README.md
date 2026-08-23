# 05 - Environment Variables & Configuration

This project builds on **Project 04** and introduces a **centralized configuration system** using **Pydantic Settings**.

Instead of reading environment variables throughout the application with `os.getenv()`, all configuration is managed from a single, typed `config.py` file.

This is the approach commonly used in production FastAPI applications.

---

## Learning Objectives

By the end of this project, you'll understand:

- Why centralized configuration matters
- How `BaseSettings` loads values from `.env`
- Type-safe environment variables
- Using `@lru_cache` for a shared configuration instance
- Docker Compose with external configuration
- Separating secrets from application code

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
| Docker | Latest |
| Docker Compose | Latest |

---

## Project Structure

```text
05-environment-variables-configuration/
├── app/
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
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
├── .dockerignore
├── requirements.txt
└── README.md
```

---

# Architecture

```
                    Browser / API Client
                           │
                           ▼
                  localhost:8000
                           │
                           ▼
              FastAPI Container
                           │
                    Pydantic Settings
                           │
                           ▼
                Docker Bridge Network
                           │
                           ▼
                 MySQL Container
                           │
                           ▼
              Named Volume (mysql_data)
```

### Configuration Flow

1. Docker Compose loads `.env`.
2. `Pydantic Settings` reads all variables.
3. `config.py` creates a typed settings object.
4. Every module imports the same cached configuration.
5. FastAPI and MySQL use identical configuration values.

---

# What's New Compared to Project 04

| Project 04 | Project 05 |
|------------|------------|
| `os.getenv()` | `BaseSettings` |
| Manual environment access | Centralized configuration |
| Variables scattered across files | Single `config.py` |
| Multiple environment reads | Cached settings object |

Nothing else changes.

The application behaves exactly the same—the improvement is entirely in **how configuration is managed**.

---

# Centralized Configuration

## `app/core/config.py`

Instead of writing this everywhere:

```python
os.getenv("MYSQL_HOST")
```

we now create a single configuration class.

```python
class Settings(BaseSettings):
    APP_NAME: str = "Docker FastAPI Playground"
    APP_ENV: str = "development"

    MYSQL_HOST: str = "mysql"
    MYSQL_PORT: int = 3306
```

Access configuration anywhere.

```python
settings = get_settings()

settings.APP_NAME
settings.MYSQL_HOST
```

---

# Why `@lru_cache`?

```python
@lru_cache
def get_settings():
    return Settings()
```

Without caching:

- `.env` is read repeatedly.
- Multiple settings objects are created.

With caching:

- One shared instance
- Faster execution
- Consistent configuration across the application

---

# Environment Variables

## `.env.example`

```env
APP_NAME=Docker FastAPI Playground
APP_ENV=development

MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_DATABASE=tasksdb
MYSQL_USER=appuser
MYSQL_PASSWORD=your_password
MYSQL_ROOT_PASSWORD=your_root_password
```

Create your local file.

```bash
cp .env.example .env
```

---

# Docker Compose

Configuration is injected using `env_file`.

```yaml
services:
  api:
    env_file:
      - .env

  mysql:
    env_file:
      - .env
```

This keeps secrets outside the application code.

---

# Running the Project

## Step 1

Create the local environment file.

```bash
cp .env.example .env
```

## Step 2

Build and start.

```bash
docker compose up --build
```

Expected behavior:

- MySQL becomes healthy.
- FastAPI starts.
- Configuration loads automatically.

---

# Available Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/` | Project information |
| `/config` | View loaded configuration |
| `/health` | Health check |
| `/docs` | Swagger UI |
| `/tasks` | List tasks |
| `POST /tasks` | Create task |

---

# Testing

## Verify configuration

```bash
curl http://localhost:8000/config
```

Example response.

```json
{
  "app_name": "Docker FastAPI Playground",
  "environment": "development",
  "mysql_host": "mysql",
  "mysql_port": 3306
}
```

Notice that values come from `.env`, not hardcoded variables.

---

## Create a task

```bash
curl -X POST http://localhost:8000/tasks \
-H "Content-Type: application/json" \
-d '{"title":"Learn Pydantic Settings"}'
```

---

## List tasks

```bash
curl http://localhost:8000/tasks
```

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

View API logs.

```bash
docker compose logs api
```

View MySQL logs.

```bash
docker compose logs mysql
```

Running containers.

```bash
docker ps
```

Volumes.

```bash
docker volume ls
```

---

# Configuration Approaches Compared

| `os.getenv()` | `BaseSettings` |
|---------------|----------------|
| Manual | Automatic |
| No validation | Type validation |
| Repeated everywhere | Centralized |
| Easy to duplicate | Single source of truth |
| Limited IDE support | Excellent autocomplete |

---

# Common Issues

## `.env` missing

Create it.

```bash
cp .env.example .env
```

---

## Configuration not updating

After changing `.env`:

```bash
docker compose down
docker compose up
```

Restarting ensures Docker reloads the environment.

---

## Wrong database credentials

Check:

- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DATABASE`

inside `.env`.

---

# Questions

### Why use Pydantic Settings?

It creates a typed configuration object from environment variables.

---

### Why not use `os.getenv()` everywhere?

Scattered configuration becomes difficult to maintain.

A centralized configuration file provides:

- validation
- defaults
- autocomplete
- easier testing

---

### Why use `@lru_cache`?

It prevents repeatedly reading `.env` and creates one shared settings instance.

---

### Does Docker Compose automatically load `.env`?

Yes. Docker Compose uses `.env` for variable substitution, while `env_file` passes those variables into the containers.

---

# Skills Demonstrated

- Environment Variable Management
- Pydantic Settings
- Typed Configuration
- FastAPI Architecture
- Docker Compose
- MySQL Integration
- Configuration Best Practices
- Modern FastAPI Development

