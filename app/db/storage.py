from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import Document, Rubric
from app import schemas, utils


async def create_document(
        post_schema: schemas.DocumentCreateRequest,
        session: AsyncSession
) -> Document:
    rubrics = await create_rubrics(post_schema.rubrics, session)

    document = Document(
        text=post_schema.text,
        rubrics=rubrics,
        created_date=utils.cur_datetime()
    )
    session.add(document)
    await session.commit()

    return document


async def create_rubric(
        name: str,
        session: AsyncSession
) -> Rubric:
    query = select(Rubric).where(Rubric.name == name)
    rubric = (await session.execute(query)).first()

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
