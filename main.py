from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI(title="Görev Yönetimi API", version="1.0.0")

tasks: list[dict] = []


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    done: bool = False


@app.get("/tasks")
def get_tasks():
    return {"tasks": tasks, "count": len(tasks)}


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    new_task = {
        "id": str(uuid.uuid4()),
        "title": task.title,
        "description": task.description,
        "done": task.done,
    }
    tasks.append(new_task)
    return new_task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: str):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return
    raise HTTPException(status_code=404, detail="Görev bulunamadı")
