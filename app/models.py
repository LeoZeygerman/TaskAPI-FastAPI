import datetime

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import enum 
from typing import Annotated

created_at = Annotated[datetime.datetime, mapped_column(server_default=text("CURRENT_TIMESTAMP('utc', now())"))]

class Base(DeclarativeBase):
    pass

class Priority(enum.Enum):
    low = 'Low priority'
    mid = 'Mid priority'
    high = 'High priority'

class TaskOrm(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key = True)
    task_title: Mapped[str]
    description: Mapped[str | None]
    is_completed: Mapped[bool] = mapped_column(default=False)
    priority: Priority
    created_at: Mapped[created_at]
    deadline: Mapped[datetime.date | None]