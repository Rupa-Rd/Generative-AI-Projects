from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    user_name: str
    email: str
    password: str
    created_at: datetime = datetime.now()


class UserLogin(BaseModel):
    email: str
    password: str

class UserTasks(BaseModel):
    user_id: str

class Task(BaseModel):
    user_id: str
    task: str
    completed: bool
    created_at: datetime = datetime.now()
    due_date: str
    notes: str