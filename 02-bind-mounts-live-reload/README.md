# 02 - Bind Mounts & Live Reload

A production-style FastAPI project demonstrating how Docker Bind Mounts enable live code updates without rebuilding the image.

## Learning Objectives

- Docker Bind Mounts
- FastAPI live reload with Uvicorn
- Docker Compose for development
- Bind Mounts vs Named Volumes

## Tech Stack

- FastAPI
- Uvicorn
- Python 3.13
- Docker

## Folder Structure

```text
02-bind-mounts-live-reload/
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
└── README.md
```

## Run

```bash
docker compose up --build
```

Visit:
- http://localhost:8000
- http://localhost:8000/docs
- http://localhost:8000/health

## Live Reload

Edit `main.py` and refresh the browser. Changes appear immediately because Docker mounts your local folder into `/app`.

## Bind Mount Configuration

```yaml
volumes:
  - .:/app
```

## Notes

- Bind Mounts are ideal for development.
- `--reload` automatically restarts Uvicorn when source files change.
