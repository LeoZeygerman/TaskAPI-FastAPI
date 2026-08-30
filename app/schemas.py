import datetime

from pydantic import BaseModel, Field

class CreateTask(BaseModel):
    task_title: str
    description: str = Field(max_length=250)
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
    desctiption: str
    is_completed: bool
    created_at: datetime.date
    deadline: datetime.date