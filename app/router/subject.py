from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import SessionDep
from app.schemas import CreateSubject, ResponseDetail, CreateDetail, ResponseSubjectsWithDetail, UpdateDetail
from app.models import SubjectDetailOrm, SubjectOrm

router = APIRouter(prefix='/subject', tags=['Предметы'])

@router.post('/', summary='Добавить предмет', response_model=ResponseDetail)
async def add_subject(session: SessionDep, subject: CreateDetail):
    new_subject = SubjectOrm(title = subject.title)
    new_subject_detail = SubjectDetailOrm(
        subject = new_subject,
        target = subject.target,
        hours_a_day = subject.hours_a_day,
        deadline = subject.deadline
    )

    session.add(new_subject)
    session.add(new_subject_detail)
    await session.commit()
    await session.refresh(new_subject_detail)
    print('Предмет добавлен!')
    return new_subject_detail


@router.get('/all', summary='Показать все предметы', response_model=list[ResponseSubjectsWithDetail])
async def get_all_subjects(session: SessionDep):
    query = (select(SubjectDetailOrm)
             .options(selectinload(SubjectDetailOrm.subject)))
    result = await session.execute(query)
    subjects = result.scalars().all()
    if not subjects:
        raise HTTPException(status_code=404, detail='Предметов нет!')
    return subjects


@router.get('/{subject_name}', summary='Найти предмет', response_model=list[ResponseDetail])
async def get_one_by_name(session: SessionDep, subject_name: str):
    query = (select(SubjectDetailOrm)
             .join(SubjectDetailOrm.subject)
             .where(SubjectOrm.title == subject_name)
             .options(selectinload(SubjectDetailOrm.subject)))
    result = await session.execute(query)
    subjects = result.scalars().all()
    if not subjects:
        raise HTTPException(status_code=404, detail='Предмет не найден!')
    return subjects


@router.patch('/patch/{subject_id}', summary='Изменить предмет', response_model=ResponseDetail)
async def patch_subject(session: SessionDep, subject_id: int, subject: UpdateDetail):
    query = (select(SubjectDetailOrm)
             .join(SubjectDetailOrm.subject)
             .where(SubjectOrm.id == subject_id)
             .options(selectinload(SubjectDetailOrm.subject)))
    result = await session.execute(query)
    db_subject = result.scalar_one_or_none()
    if not db_subject:
        raise HTTPException(status_code=404, detail='Предмет не найден!')

    if subject.title is not None:
        db_subject.title = subject.title
    if subject.target is not None:
        db_subject.target = subject.target
    if subject.hours_a_day is not None:
        db_subject.hours_a_day = subject.hours_a_day
    if subject.deadline is not None:
        db_subject.deadline = subject.deadline

    await session.commit()
    await session.refresh(db_subject)
    return db_subject