# 07 - Nginx Reverse Proxy

This project builds on **Project 06** and introduces **Nginx as a Reverse Proxy**, a common production pattern where a web server sits in front of an application server.

Instead of exposing FastAPI directly to users, all incoming requests first reach **Nginx**, which then forwards them to the FastAPI container.

This architecture is used by many production deployments because it provides a single entry point for routing, security, and future scalability.

---

## Learning Objectives

By the end of this project, you'll understand:

- What a reverse proxy is
- Why Nginx is used with FastAPI
- Upstream server configuration
- Request forwarding
- Forwarding HTTP headers
- Keeping application containers private
- Preparing applications for load balancing

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
07-nginx-reverse-proxy/
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

## Current Production Flow

```text
                Browser / API Client
                       │
                       ▼
                 localhost:80
                       │
                       ▼
            Nginx Container (Public)
                       │
             backend-network (Bridge)
                       │
                 Docker Internal DNS
                       │
                       ▼
           FastAPI Container (api)
                       │
                       ▼
            MySQL Container (mysql)
                       │
                       ▼
         Named Volume (mysql_data)
```

### Request Flow

1. A client sends a request to `http://localhost`.
2. Nginx receives the request on port **80**.
3. Nginx forwards the request to the FastAPI container (`api:8000`).
4. FastAPI processes the request.
5. FastAPI communicates with MySQL.
6. The response travels back through Nginx to the client.

The client never communicates directly with FastAPI.

---

# What's New Compared to Project 06

| Project 06 | Project 07 |
|------------|------------|
| Client → FastAPI | Client → Nginx → FastAPI |
| Direct API exposure | Reverse proxy |
| No upstream server | Nginx upstream |
| Basic routing | Request forwarding |
| Internal networking | Production-style entry point |

The application functionality remains unchanged.

Only the request path changes.

---

# Why Use Nginx?

Nginx acts as a **traffic controller** for your application.

Instead of exposing multiple services directly, one server handles incoming traffic and decides where it should go.

Benefits include:

- Single public entry point
- SSL termination
- Load balancing
- Request routing
- Static file serving
- Security improvements

In real production environments, users usually connect to Nginx—not directly to FastAPI.

---

# Nginx Configuration

## Upstream Server

```nginx
upstream fastapi_backend {
    server api:8000;
}
```

`api` is not an IP address.

Docker automatically resolves the service name using its internal DNS.

---

## Reverse Proxy

```nginx
location / {
    proxy_pass http://fastapi_backend;
}
```

Every request arriving at Nginx is forwarded to FastAPI.

---

## Forwarded Headers

```nginx
proxy_set_header Host $host;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
```

These headers preserve useful information.

| Header | Purpose |
|---------|----------|
| `Host` | Original hostname |
| `X-Forwarded-For` | Client IP |
| `X-Forwarded-Proto` | HTTP/HTTPS |

Many production applications rely on these headers.

---

# Docker Compose Configuration

Nginx joins the same Docker network.

```yaml
nginx:
  image: nginx:1.29-alpine
  networks:
    - backend-network
```

FastAPI also joins the same network.

```yaml
api:
  networks:
    - backend-network
```

Because both containers share the network, Nginx reaches FastAPI using:

```text
api:8000
```

No manual IP configuration is required.

---

# Running the Project

## Step 1

Create the environment file.

```bash
cp .env.example .env
```

## Step 2

Build and start.

```bash
docker compose up --build
```

Docker starts:

- Nginx
- FastAPI
- MySQL
- Named volume
- Custom bridge network

---

# Available Endpoints

Notice these are accessed through **Nginx**.

| URL | Purpose |
|-----|---------|
| `http://localhost/` | Welcome |
| `http://localhost/docs` | Swagger UI |
| `http://localhost/health` | Health |
| `http://localhost/proxy-info` | Proxy details |
| `http://localhost/tasks` | Task API |

The browser never connects directly to port **8000**.

---

# Testing

## Verify Reverse Proxy

```bash
curl http://localhost/proxy-info
```

Expected response.

```json
{
  "reverse_proxy": "nginx",
  "upstream": "api:8000"
}
```

This confirms traffic passes through Nginx.

---

## Verify Swagger

Open:

```text
http://localhost/docs
```

Nginx forwards the request automatically.

---

## Create a Task

```bash
curl -X POST http://localhost/tasks \
-H "Content-Type: application/json" \
-d '{"title":"Learn Nginx Reverse Proxy"}'
```

---

## List Tasks

```bash
curl http://localhost/tasks
```

Everything still works because Nginx simply forwards requests.

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

View Nginx logs.

```bash
docker compose logs nginx
```

View FastAPI logs.

```bash
docker compose logs api
```

View MySQL logs.

```bash
docker compose logs mysql
```

Inspect the network.

```bash
docker network inspect backend-network
```

---

# Direct Access vs Reverse Proxy

| Direct FastAPI | Nginx Reverse Proxy |
|----------------|----------------------|
| Client reaches API | Client reaches Nginx |
| Port 8000 exposed | Port 80 exposed |
| Limited routing | Advanced routing |
| No SSL termination | SSL ready |
| Harder scaling | Easy load balancing |

This is why production systems usually place Nginx in front of application servers.

---

# Common Issues

## Nginx returns 502 Bad Gateway

This usually means FastAPI is not ready.

Check:

```bash
docker compose logs api
docker compose logs nginx
```

Wait until the API finishes starting.

---

## Swagger doesn't load

Use:

```text
http://localhost/docs
```

Nginx automatically forwards the request.

---

## Nginx cannot find FastAPI

Verify:

- both containers belong to `backend-network`
- upstream uses `api:8000`

Inspect the network.

```bash
docker network inspect backend-network
```

---

## Port 80 already in use

Another application may already be using port 80.

Either stop it or change the host port.

Example:

```yaml
ports:
  - "8080:80"
```

---

# Questions

### What is a Reverse Proxy?

A reverse proxy receives client requests and forwards them to backend services.

Clients communicate with the proxy instead of the application directly.

---

### Why use Nginx with FastAPI?

- SSL termination
- Load balancing
- Security
- Centralized routing
- Static file serving

---

### What is an Upstream Server?

An upstream server is the backend server that Nginx forwards requests to.

Example:

```nginx
upstream fastapi_backend {
    server api:8000;
}
```

---

### Why use `api` instead of an IP address?

Docker's internal DNS automatically resolves service names.

Container IPs can change.

Service names remain stable.

---

### Does Nginx replace FastAPI?

No. FastAPI still handles the application logic.

Nginx only manages incoming traffic.

---

# Skills Demonstrated

- Nginx Reverse Proxy
- Upstream Configuration
- HTTP Header Forwarding
- Docker Networking
- Docker Internal DNS
- FastAPI Deployment
- Production Architecture
- Docker Compose Best Practices

