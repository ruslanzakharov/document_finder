from pydantic import BaseModel
from datetime import datetime as dt

from app.db import Rubric


class DocumentCreateRequest(BaseModel):
    rubrics: list[str]
    text: str


class DocumentResponse(BaseModel):
    id: int
    text: str
    rubrics: list[Rubric]
    created_date: dt

    class Config:
        orm_mode = True
