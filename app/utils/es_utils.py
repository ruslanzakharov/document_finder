from elasticsearch import Elasticsearch
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db import Document, storage
from app.es import es_search, create_es_document
from app import schemas


async def get_bd_search_response(
        query: str, session: AsyncSession, es_client: Elasticsearch
) -> list[Document]:
    """Возвращает по поисковому запросу отсортированные объекты БД."""
    hits = es_search(query, es_client)

    documents = []
    for hit in hits:
        query = select(Document).where(Document.id == hit['id']).\
            options(selectinload(Document.rubrics))
        document = (await session.execute(query)).first()[0]

        if document is not None:
            documents.append(document)

    documents.sort(key=lambda doc: doc.created_date)

    return documents


async def create_document(
        post_schema: schemas.DocumentCreateRequest,
        session: AsyncSession,
        es_client: Elasticsearch
) -> Document:
    """Создает документ в ElastSearch и БД."""
    document = await storage.create_document(post_schema, session)
    create_es_document(
        document_id=document.id,
        text=document.text,
        es_client=es_client
    )

    return document
