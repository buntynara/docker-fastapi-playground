# 04 - Multi-Stage Docker Build

This project builds on **Project 03** and introduces one important production optimization:

> **Multi-Stage Docker Builds**

Everything else—FastAPI architecture, `.env`, Docker Compose, MySQL, health checks, and named volumes—remains the same so we can focus on understanding image optimization.

---

## Learning Objectives

- Understand Multi-Stage Docker Builds
- Reduce image size
- Separate build and runtime environments
- Improve container security
- Follow production deployment practices

---

## What's New Compared to Project 03

| Project 03 | Project 04 |
|------------|------------|
| Single-stage Docker build | Multi-stage Docker build |
| Build tools remain in image | Build tools removed |
| Larger runtime image | Smaller runtime image |
| Development-style image | Production-style image |

---

## How Multi-Stage Works

### Builder Stage

```dockerfile
FROM python:3.12-slim AS builder

WORKDIR /install

COPY requirements.txt .

RUN pip install --prefix=/install/python --no-cache-dir -r requirements.txt
```

This stage installs all Python dependencies.

### Runtime Stage

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /install/python /usr/local
COPY app ./app
```

Only the installed packages and application code are copied into the final image.

---

## Build Flow

```
Source Code
     │
     ▼
 Builder Stage
     │
     ▼
Install Dependencies
     │
     ▼
 Runtime Stage
     │
     ▼
 Optimized Image
```

---

## Benefits

- Smaller image
- Faster deployment
- Less storage usage
- Reduced attack surface
- Cleaner production image

---

## Build

```bash
cp .env.example .env
docker compose up --build
```

Everything behaves exactly like Project 03.

---

## Verify the Difference

Build the image.

```bash
docker images
```

Notice the runtime image contains only what is needed to run the application.

---

## Questions

### Why use a Multi-Stage Docker Build?

To separate dependency installation from the final runtime image.

### Why copy only `/install/python`?

It avoids carrying unnecessary build files into production.

### Does Multi-Stage change application behavior?

No. It changes **how the image is built**, not how the application works.

---

# Skills Demonstrated

- Multi-Stage Docker Builds
- Image Optimization
- Production Container Design
- FastAPI Deployment
- Docker Compose
