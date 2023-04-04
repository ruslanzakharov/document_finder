from pydantic import BaseModel
from datetime import datetime as dt


class DocumentCreateRequest(BaseModel):
    rubrics: list[str]
    text: str


class RubricResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class DocumentResponse(BaseModel):
    id: int
    text: str
    rubrics: list[RubricResponse]
    created_date: dt

    class Config:
        orm_mode = True


class SearchResponse(BaseModel):
    documents: list[DocumentResponse]
