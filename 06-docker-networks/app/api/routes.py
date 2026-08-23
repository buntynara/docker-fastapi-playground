from fastapi import APIRouter
from app.services.task_service import get_tasks, create_task
from app.schemas.task import TaskCreate
from app.core.config import get_settings

router = APIRouter()
settings = get_settings()

@router.get("/")
def home():
    return {
        "project": "06 - Docker Networks",
        "environment": settings.APP_ENV,
        "application": settings.APP_NAME,
        "mysql_host": settings.MYSQL_HOST
    }

@router.get("/health")
def health():
    return {"status": "healthy"}

# ----- Network Endpoints -----

@router.get('/network')
def network():
    return {'network':'backend-network','communication':'mysql:3306'}

# ----- Config Endpoints -----

@router.get("/config")
def config():
    return {
        "app_name": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "mysql_host": settings.MYSQL_HOST,
        "mysql_port": settings.MYSQL_PORT
    }

# ----- Task Endpoints -----

@router.get("/tasks")
def list_tasks():
    return get_tasks()

@router.post("/tasks")
def add_task(task: TaskCreate):
    return create_task(task)
