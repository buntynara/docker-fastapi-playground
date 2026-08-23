from fastapi import FastAPI
from app.core.database import lifespan
from app.core.config import get_settings
from app.api.routes import router

settings = get_settings()

app = FastAPI(
    title = settings.APP_NAME,
    description = "Project 08 - Health Checks & Readiness",
    version = "1.0.0",
    lifespan = lifespan
)

app.include_router(router)
