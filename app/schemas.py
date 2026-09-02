import datetime
from app.models import Priority
from pydantic import BaseModel, Field

class CreateTask(BaseModel):
    task_title: str
    description: str = Field(max_length=250)
    priority: Priority
    is_completed: bool
    deadline: datetime.date

class UpdateTask(BaseModel):
    task_title: str | None = None
    description: str | None = None
    is_completed: bool | None = None
    deadline: datetime.date | None = None

class ResponseTask(BaseModel):
    id: int
    task_title: str
    description: str
    is_completed: bool
    created_at: datetime.datetime
    deadline: datetime.date