# Docker FastAPI Playground

A **production-focused Docker + FastAPI learning series** containing 12 hands-on projects that progressively evolve from a simple containerized API to a production-ready, Kubernetes-ready application.

Instead of isolated examples, this repository builds the **same FastAPI application step by step**, introducing one major Docker concept in each project.

---

## What You'll Learn

By completing this series, you'll gain practical experience with:

- Docker Images and Containers
- Dockerfiles
- Bind Mounts
- Named Volumes
- Docker Compose
- Environment Variables
- Multi-Stage Builds
- Container Networking
- Nginx Reverse Proxy
- Health Checks
- Image Optimization
- Container Security
- Kubernetes-ready deployment patterns

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

## Repository Structure

```text
docker-fastapi-playground/
├── 01-hello-fastapi-container/
├── 02-bind-mounts-live-reload/
├── 03-named-volumes-mysql/
├── 04-multi-stage-build/
├── 05-environment-variables/
├── 06-docker-networks/
├── 07-nginx-reverse-proxy/
├── 08-health-checks/
├── 09-multi-service-compose/
├── 10-production-optimization/
├── 11-container-security/
└── 12-kubernetes-ready-stack/
```

---

# Learning Roadmap

| Project | Status | Concept |
|---------|--------|---------|
| 01 | ✅ | Hello FastAPI Container |
| 02 | ✅ | Bind Mounts & Live Reload |
| 03 | ✅ | Named Volumes + MySQL |
| 04 | ✅ | Multi-Stage Docker Build |
| 05 | 🚧 | Environment Variables & Configuration |
| 06 | 🚧 | Docker Networks |
| 07 | 🚧 | Nginx Reverse Proxy |
| 08 | 🚧 | Health Checks |
| 09 | 🚧 | Multi-Service Compose |
| 10 | 🚧 | Production Optimization |
| 11 | 🚧 | Container Security |
| 12 | 🚧 | Kubernetes-ready Stack |

---

## Learning Progression

This repository follows a real-world development journey.

### Projects 1–2

Learn Docker fundamentals.

- Build Docker images
- Run containers
- Use Bind Mounts for live development

### Projects 3–4

Move toward production architecture.

- Named Volumes
- MySQL integration
- Environment-based configuration
- Multi-Stage Docker builds

### Upcoming Projects

We'll continue evolving the application with:

- Docker Networks
- Nginx Reverse Proxy
- Health Checks
- Production image optimization
- Security hardening
- Kubernetes-ready deployment

---

## Architecture Evolution

The application grows naturally throughout the series.

### Initial Architecture

```text
Client
  │
  ▼
FastAPI
```

### Current Architecture (Project 04)

```text
Client
  │
  ▼
FastAPI Container
  │
Docker Network
  │
  ▼
MySQL Container
  │
Named Volume
```

By Project 12, this will become a production-ready container stack suitable for Kubernetes deployment.

---

# Getting Started

Clone the repository.

```bash
git clone https://github.com/buntynara/docker-fastapi-playground.git
cd docker-fastapi-playground
```

Each project is completely self-contained.

For example:

```bash
cd 04-multi-stage-build
cp .env.example .env
docker compose up --build
```

---

## Repository Highlights

Every project includes:

- Production-style project structure
- Modern FastAPI (`lifespan`)
- Docker Compose
- Interactive Swagger UI (`/docs`)
- Health endpoints
- Interview questions
- Troubleshooting tips
- GitHub-ready documentation

---

## Skills Demonstrated

### Docker

- Dockerfile
- Multi-Stage Builds
- Bind Mounts
- Named Volumes
- Docker Compose
- Health Checks
- Networking
- Image Optimization

### FastAPI

- Layered Architecture
- Routers
- Services
- Schemas
- Lifespan Events
- Environment Configuration

### DevOps

- Production-ready containers
- Environment management
- Persistent storage
- Service orchestration
- Deployment best practices

---

## Who is this repository for?

- Developers learning Docker
- FastAPI developers
- DevOps beginners
- Engineers preparing for Docker interviews
- Anyone moving toward Kubernetes and microservices

---

## Roadmap

- [x] Project 01
- [x] Project 02
- [x] Project 03
- [x] Project 04
- [ ] Project 05
- [ ] Project 06
- [ ] Project 07
- [ ] Project 08
- [ ] Project 09
- [ ] Project 10
- [ ] Project 11
- [ ] Project 12

---

## License

This repository is released under the **MIT License**.

Feel free to use these projects for learning, experimentation, and interview preparation.