from fastapi import FastAPI
from app.core.database import lifespan
from app.api.routes import router

app = FastAPI(
    title = 'Docker FastAPI Playground',
    description = 'Project 04 - Multi-Stage Build',
    version = '1.0.0',
    lifespan = lifespan
)

app.include_router(router)
