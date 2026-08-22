from fastapi import FastAPI
import os

app = FastAPI(
    title="Docker FastAPI Playground",
    description="Project 02 - Bind Mounts & Live Reload",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Hello from FastAPI with Bind Mounts!",
        "project": "02 - Bind Mounts & Live Reload",
        "environment": os.getenv("APP_ENV", "development")
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
