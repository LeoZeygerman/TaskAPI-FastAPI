from datetime import date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class SubjectOrm(Base):
    __tablename__ = 'subject'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    detail: Mapped[list['SubjectDetailOrm']] = relationship(back_populates='subject')

class SubjectDetailOrm(Base):
    __tablename__ = 'subject detail'

    id: Mapped[int] = mapped_column(primary_key=True)
    target: Mapped[str]
    hours_a_day: Mapped[int]
    deadline: Mapped[date]

    subject_id: Mapped[int] = mapped_column(ForeignKey('subject.id'))
    subject: Mapped['SubjectOrm'] = relationship(back_populates='detail')
