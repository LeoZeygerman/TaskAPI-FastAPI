from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.database import SessionDep
from app.models import TaskOrm
from app.schemas import CreateTask, ResponseTask

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

@router.get('/get_task/{task_id}', summary= 'Получить одну задачу', response_model=ResponseTask)
async def get_one_task(session: SessionDep, task_id: int):
    query = select(TaskOrm).where(task_id = TaskOrm.id)
    result = await session.execute(query)
    book = result.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404, detail='Книга не найдена')
    return book