# 06 - Docker Networks

This project builds on **Project 05** and introduces **Docker Networks**, showing how containers communicate securely using Docker's internal DNS instead of hardcoded IP addresses.

Instead of connecting to MySQL using an IP like `172.x.x.x`, the FastAPI application simply connects to `mysql`, and Docker automatically resolves it.

This is the networking model used by real Docker Compose applications.

---

## Learning Objectives

By the end of this project, you'll understand:

- Docker bridge networks
- Custom networks in Docker Compose
- Docker's internal DNS
- Service-to-service communication
- Network isolation
- Inspecting Docker networks
- Why container IP addresses should never be hardcoded

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
06-docker-networks/
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

## Current Network Architecture

```text
                 Browser / API Client
                        │
                        ▼
                localhost:8000
                        │
                        ▼
          FastAPI Container (api)
                        │
             backend-network (Bridge)
                        │
         Docker Internal DNS Resolution
                        │
                        ▼
          MySQL Container (mysql)
                        │
                        ▼
         Named Volume (mysql_data)
```

### Communication Flow

1. Docker Compose creates a custom bridge network called `backend-network`.
2. Both containers join this network.
3. Docker automatically creates a DNS entry named `mysql`.
4. FastAPI connects using `mysql:3306`.
5. MySQL stores data inside the persistent named volume.

No container IP addresses are required.

---

# What's New Compared to Project 05

| Project 05 | Project 06 |
|------------|------------|
| Default networking | Custom bridge network |
| Basic service communication | Explicit network configuration |
| Implicit DNS | Demonstrated Docker DNS |
| Standard Compose | Network isolation |

The application functionality remains the same.

The improvement is entirely in how containers communicate.

---

# Docker Network Configuration

## Creating a Custom Network

`docker-compose.yml`

```yaml
networks:
  backend-network:
    driver: bridge
```

This creates an isolated bridge network dedicated to this application.

---

## Attaching Containers

FastAPI joins the network.

```yaml
api:
  networks:
    - backend-network
```

MySQL joins the same network.

```yaml
mysql:
  networks:
    - backend-network
```

Because both containers share the same network, Docker automatically enables communication between them.

---

# Docker Internal DNS

One of Docker's most useful features is automatic DNS resolution.

Instead of this:

```text
172.18.0.2
```

FastAPI connects using:

```text
mysql
```

Docker translates `mysql` into the correct container IP.

This continues working even if:

- the container restarts
- the IP changes
- the application is recreated

The hostname stays the same.

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

Create your local configuration.

```bash
cp .env.example .env
```

---

# Running the Project

## Step 1

Create the environment file.

```bash
cp .env.example .env
```

## Step 2

Start the application.

```bash
docker compose up --build
```

Docker automatically creates:

- `backend-network`
- `mysql_data`
- FastAPI container
- MySQL container

---

# Available Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/` | Project information |
| `/network` | Network details |
| `/health` | Health check |
| `/docs` | Swagger UI |
| `/tasks` | List tasks |
| `POST /tasks` | Create task |

---

# Testing

## Verify network information

```bash
curl http://localhost:8000/network
```

Expected response.

```json
{
  "network": "backend-network",
  "api_container": "api",
  "database_container": "mysql",
  "communication": "mysql:3306"
}
```

Notice that communication happens through the service name instead of an IP address.

---

## Create a task

```bash
curl -X POST http://localhost:8000/tasks \
-H "Content-Type: application/json" \
-d '{"title":"Learn Docker Networks"}'
```

---

## List tasks

```bash
curl http://localhost:8000/tasks
```

---

# Inspecting Docker Networks

List available networks.

```bash
docker network ls
```

Example.

```text
NETWORK ID     NAME              DRIVER
abc123         backend-network   bridge
```

Inspect the network.

```bash
docker network inspect backend-network
```

You'll see:

- FastAPI container
- MySQL container
- IP addresses
- Network configuration

This confirms both containers belong to the same bridge network.

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

List networks.

```bash
docker network ls
```

Inspect network.

```bash
docker network inspect backend-network
```

View API logs.

```bash
docker compose logs api
```

View MySQL logs.

```bash
docker compose logs mysql
```

---

# Default Network vs Custom Network

| Default Network | Custom Network |
|-----------------|----------------|
| Automatically created | Explicitly defined |
| Generic naming | Meaningful name |
| Works for small projects | Better for production |
| Less organized | Clear service grouping |

Using custom networks makes larger applications much easier to understand.

---

# Why Not Use `localhost`?

This is one of the most common interview questions.

Inside the FastAPI container:

```text
localhost
```

means:

> "This FastAPI container."

It **does not** mean the MySQL container.

To reach MySQL, use:

```text
mysql
```

because Docker provides that hostname automatically.

---

# Common Issues

## Containers cannot communicate

Inspect the network.

```bash
docker network inspect backend-network
```

Verify both containers appear.

---

## Network missing

If the network was removed manually:

```bash
docker compose down
docker compose up
```

Docker recreates it automatically.

---

## MySQL connection fails

Check:

- `MYSQL_HOST=mysql`
- both services are attached to `backend-network`
- MySQL is healthy

---

# Questions

### Why create a custom Docker network?

It isolates related services and makes communication explicit.

---

### How does FastAPI find MySQL?

Docker's built-in DNS resolves the service name `mysql` to the correct container IP.

---

### Why avoid container IP addresses?

Container IPs change whenever containers are recreated.

Service names remain stable.

---

### What is the Bridge driver?

The bridge driver creates an isolated virtual network for containers running on the same Docker host.

---

### Can containers on different networks communicate?

Not by default.

They must share a common network or be connected to multiple networks.

---

# Skills Demonstrated

- Docker Networks
- Bridge Networking
- Docker Internal DNS
- Service Discovery
- Network Isolation
- Docker Compose
- FastAPI Architecture
- MySQL Integration
- Container Communication Best Practices
