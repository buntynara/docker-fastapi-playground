from fastapi import APIRouter, Response, status
from app.services.task_service import get_tasks, create_task
from app.schemas.task import TaskCreate
from app.core.database import app_ready

router = APIRouter()

@router.get('/')
def home(): 
    return {
        "project":"08 - Health Checks & Readiness",
        "message":"Check health, live and ready status."
    }

# ----- Health Checks Endpoints -----

@router.get("/health")
def health():
    return {"status": "healthy"}

@router.get("/live")
def live(): 
    return {"status": "alive"}

@router.get("/ready")
def ready(response:Response):
    if app_ready:
        return {"status": "ready"}

    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {"status": "not ready"}


# ----- Proxy Endpoints -----

@router.get("/proxy-info")
def proxy_info(): 
    return {
       "reverse_proxy": "nginx",
       "upstream": "api:8000"
    }

# ----- Task Endpoints -----

@router.get("/tasks")
def list_tasks():
    return get_tasks()

@router.post("/tasks")
def add_task(task: TaskCreate):
    return create_task(task)
