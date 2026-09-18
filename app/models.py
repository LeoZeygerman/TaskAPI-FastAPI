from datetime import date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class SubjectOrm(Base):
    __tablename__ = 'subject'

    id: Mapped[int] = mapped_column(primary_key=True)
    subject_title: Mapped[str]

    detail: Mapped['SubjectDetailOrm'] = relationship(back_populates='subjects')

class SubjectDetailOrm(Base):
    __tablename__ = 'subject_detail'

    id: Mapped[int] = mapped_column(primary_key=True)
    target: Mapped[str]
    hours_a_day: Mapped[int]
    deadline: Mapped[date]

    subject_id: Mapped[int] = mapped_column(ForeignKey('subject.id'))
    subjects: Mapped['SubjectOrm'] = relationship(back_populates='detail')
