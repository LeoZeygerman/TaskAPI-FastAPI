from datetime import date
from pydantic import BaseModel, ConfigDict, Field

class CreateSubject(BaseModel):
    title: str


class CreateDetail(BaseModel):
    title: CreateSubject
    target: str = Field(min_length=10, max_length=100)
    hours_a_day: int = Field(gt=0, lt=24)
    deadline: date

    model_config = ConfigDict(from_attributes=True)

class ResponseSubject(BaseModel):
    title: str

    model_config = ConfigDict(from_attributes=True)    


class ResponseDetail(BaseModel):
    id: int
    title: ResponseSubject
    target: str
    hours_a_day: int 
    deadline: date

    model_config = ConfigDict(from_attributes=True)    


class ResponseDetailShort(BaseModel):
    title: str
    target: str


class ResponseSubjectsWithDetail(BaseModel):
    id: int
    title: str
    detail: list[ResponseDetailShort]

    model_config = ConfigDict(from_attributes=True)


class UpdateDetail(BaseModel):
    title: str | None = None
    target: str | None = None
    hours_a_day: int | None = None
    deadline: date | None = None
