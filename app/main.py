from fastapi import FastAPI, HTTPException
from app.models import Task

app = FastAPI()


# In memory database
tasks_db: list[Task] = []


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/tasks/")
async def get_tasks():
    return tasks_db


# Create tasks
@app.post("/tasks/")
async def create_task(task: Task):
    tasks_db.append(task)
    return task


# Get task detail
@app.get("/task/{task_id}")
async def get_task(task_id: str):
    for task in tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


# Update task
@app.put("/task/{task_id}")
async def update_task(task_id: str, task: Task):
    for i in range(len(tasks_db)):
        if tasks_db[i].id == task_id:
            tasks_db[i] = task
            return task
    raise HTTPException(status_code=404, detail="Task not found")


# Delete task
@app.delete("/task/{task_id}")
async def delete_task(task_id: str):
    for i in range(len(tasks_db)):
        if tasks_db[i].id == task_id:
            task = tasks_db.pop(i)
            return task
    raise HTTPException(status_code=404, detail="Task not found")
