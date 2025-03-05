import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List


# Task Model
class Task(BaseModel):
    id: str = str(uuid.uuid4())
    title: str
    description: Optional[str] = None
    completed: bool = False