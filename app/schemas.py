from pydantic import BaseModel
from datetime import datetime as dt
from typing import Optional


class DocumentCreateRequest(BaseModel):
    rubrics: list[str]
    text: str
    created_date: Optional[str] = None


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
