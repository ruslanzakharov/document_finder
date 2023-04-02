from sqlalchemy.ext.asyncio import AsyncSession
import datetime as dt

from app.db import Document, Rubric
from app import schemas


async def create_document(
        post_schema: schemas.DocumentCreateRequest,
        session: AsyncSession
) -> Document:
    rubrics = await create_rubrics(post_schema.rubrics, session)

    document = Document(
        text=post_schema.text,
        rubrics=rubrics,
        created_date=dt.datetime.now()
    )
    session.add(document)
    await session.commit()

    return document


async def create_rubric(
        name: str,
        session: AsyncSession
) -> Rubric:
    rubric = session.query(Rubric).filter_by(name=name).first()

    if rubric is None:
        rubric = Rubric(name=name)
        session.add(rubric)
        await session.commit()

    return rubric


async def create_rubrics(
        names: list[Rubric],
        session: AsyncSession
) -> list[Rubric]:
    return [await create_rubric(name, session) for name in names]
