from fastapi import APIRouter
from app.database import SessionDep
from app.schemas import CreateSubject, ResponseDetail, CreateDetail
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