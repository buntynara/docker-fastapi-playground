from fastapi import APIRouter
from app.services.task_service import get_tasks, create_task
from app.schemas.task import TaskCreate

router = APIRouter()

@router.get('/')
def home(): 
    return {
        "project":"07 - Nginx Reverse Proxy",
        "message":"Traffic now flows through Nginx."
    }

@router.get("/health")
def health():
    return {"status": "healthy"}

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
