from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI(title="Görev Yönetimi API", version="1.0.0")

tasks: list[dict] = []

# VULNERABLE: Passwords stored in plaintext — never do this in production
# Fix: use bcrypt/argon2 hashing (e.g. passlib)
users: list[dict] = [
    {"username": "admin", "password": "admin123"},
    {"username": "user1", "password": "pass456"},
]


class LoginRequest(BaseModel):
    username: str
    password: str


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    done: bool = False


@app.post("/login")
def login(credentials: LoginRequest):
    # VULNERABLE: plaintext comparison — exposes passwords if DB is leaked
    for user in users:
        if user["username"] == credentials.username and user["password"] == credentials.password:
            return {"message": "Giriş başarılı", "username": credentials.username}
    raise HTTPException(status_code=401, detail="Kullanıcı adı veya şifre hatalı")


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
