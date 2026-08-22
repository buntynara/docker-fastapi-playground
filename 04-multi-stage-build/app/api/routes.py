from fastapi import APIRouter
from app.services.task_service import get_tasks, create_task
from app.schemas.task import TaskCreate

router = APIRouter()

@router.get("/")
def home():
    return {
        "project": "04 - Multi-Stage Build",
        "message": "Production-style FastAPI architecture."
    }

@router.get("/health")
def health():
    return {"status": "healthy"}


# ----- Task Endpoints -----

@router.get("/tasks")
def list_tasks():
    return get_tasks()

@router.post("/tasks")
def add_task(task: TaskCreate):
    return create_task(task)

