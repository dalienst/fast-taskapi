from app.models import Task
from fastapi import APIRouter

router = APIRouter()


@router.get("/tasks/")
async def get_tasks():
    return {"tasks": []}
