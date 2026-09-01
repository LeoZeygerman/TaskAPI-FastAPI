from fastapi import APIRouter
from app.database import SessionDep
from app.models import TaskOrm
from app.schemas import CreateTask

router = APIRouter(prefix='/tasks', tags=['Задачи'])

@router.post('/', summary = 'Добавить задачу')
async def add_task(session: SessionDep, task: CreateTask):
    new_task = TaskOrm(
        title = task.task_title,
        descriptiom = task.description,
        is_completed = task.is_completed,
        deadline = task.deadline
    )

    session.add(new_task)
    await session.commit()

    return {'msg': f'Задача {task.task_title} добавлена!'}