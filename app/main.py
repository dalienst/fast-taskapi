from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import TaskCreate, TaskResponse
from app.database import models, db
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

# Initialize database
models.Base.metadata.create_all(bind=db.engine)

app = FastAPI()


def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Create tasks
@app.post("/tasks/", response_model=TaskResponse)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    task = models.Task(**task.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


# Get all tasks
@app.get("/tasks/", response_model=List[TaskResponse])
async def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()


# Get task detail
@app.get("/task/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# Update task
@app.patch("/task/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str, task_data: TaskCreate, db: Session = Depends(get_db)
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update task attributes with new data
    task.title = task_data.title
    task.description = task_data.description
    task.completed = task_data.completed

    db.commit()
    db.refresh(task)
    return task


# Delete task
@app.delete("/task/{task_id}")
async def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}
