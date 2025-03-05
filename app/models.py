import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List


class TaskCreate(BaseModel):

    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskResponse(TaskCreate):
    id: str = str(uuid.uuid4())

    class Config:
        from_attributes = True
