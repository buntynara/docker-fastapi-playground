# 01 - Hello FastAPI Container

A production-style starter project demonstrating how to containerize a FastAPI application with Docker.

## What you'll learn

- Docker Images vs Containers
- Dockerfile fundamentals
- Building and running containers
- Port mapping
- FastAPI with Uvicorn
- Interactive Swagger documentation

## Tech Stack

- FastAPI
- Uvicorn
- Python 3.13
- Docker

## Folder Structure

```text
01-hello-fastapi-container/
├── main.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md
```

## Build

```bash
docker build -t hello-fastapi:v1 .
```

## Run

```bash
docker run -d -p 8000:8000 --name hello-fastapi hello-fastapi:v1
```

## Endpoints

- `/`
- `/health`
- `/docs`
- `/openapi.json`

Visit `http://localhost:8000/docs` for interactive Swagger UI.

## Notes

- Automatic OpenAPI docs
- Async-ready framework
- Popular for AI and microservices
- `0.0.0.0` exposes the app outside the container
