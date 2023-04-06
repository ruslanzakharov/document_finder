from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db import Document, Rubric
from app import schemas, utils


async def create_document(
        post_schema: schemas.DocumentCreateRequest,
        session: AsyncSession
) -> Document:
    rubrics = await create_rubrics(post_schema.rubrics, session)

    if post_schema.created_date is None:
        created_date = utils.cur_datetime()
    else:
        created_date = utils.str_to_dt_obj(post_schema.created_date)

    document = Document(
        text=post_schema.text,
        rubrics=rubrics,
        created_date=created_date
    )
    session.add(document)
    await session.commit()

    return document


async def create_rubric(
        name: str,
        session: AsyncSession
) -> Rubric:
    query = select(Rubric).where(Rubric.name == name)
    rubric = (await session.execute(query)).scalar()

    if rubric is None:
        rubric = Rubric(name=name)
        session.add(rubric)
        await session.commit()

    return rubric


async def create_rubrics(
        names: list[str],
        session: AsyncSession
) -> list[Rubric]:
    return [await create_rubric(name, session) for name in names]


async def get_document(
        document_id: int, session: AsyncSession
) -> Document | None:
    query = select(Document).where(Document.id == document_id). \
        options(selectinload(Document.rubrics))
    document = (await session.execute(query)).first()

    if document is not None:
        return document[0]


async def delete_document(
        document_id: int,
        session: AsyncSession
) -> None:
    document = await get_document(document_id, session)

    if document:
        document.rubrics.clear()
        await session.delete(document)
        await session.commit()
