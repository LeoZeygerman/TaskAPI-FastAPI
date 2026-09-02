from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.database import SessionDep
from app.models import TaskOrm
from app.schemas import CreateTask, ResponseTask, UpdateTask

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
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail='Задача не найдена')
    return task

@router.get('/get_all', summary='Показать все задачи', response_model=list[ResponseTask])
async def get_all(session: SessionDep):
    query = select(TaskOrm)
    result = await session.execute(query)
    task = result.scalars().all()
    return task

@router.patch('/edit/{task_id}', summary='Изменить задачу')
async def edit_task(session: SessionDep, task_id: int, task: UpdateTask):
    query = select(TaskOrm).where(TaskOrm.id == task_id)
    result = await session.execute(query)
    task_db = result.scalar_one_or_none()

    if task_db is None:
        raise HTTPException(status_code=404, detail='Задача не найдена')
    elif task.task_title is not None:
        task_db.task_title = task.task_title
    elif task.description is not None:
        task_db.description = task.description
    elif task.is_completed is not None:
        task_db.is_completed = task.is_completed
    elif task.deadline is not None:
        task_db.deadline = task.deadline

    await session.commit()
    return task_db

@router.delete('/delete/{task_id}', summary='Удаление задачи')
async def delete_task(session: SessionDep, task_id: int):
    query = select(TaskOrm).where(TaskOrm.id == task_id)
    result = await session.execute(query)
    task_db = result.scalar_one_or_none()

    if task_db is None:
        raise HTTPException(status_code=404, detail='Задача не найдена')

    await session.delete(task_db)
    await session.commit()
    return {'msg': f'Задача {task_db.task_title} удалена!'}