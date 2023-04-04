from elasticsearch import Elasticsearch
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import Document
from app.es import es_search


async def get_bd_search_response(
        query: str, session: AsyncSession, es_client: Elasticsearch
) -> list[Document]:
    """Возвращает по поисковому запросу отсортированные объекты БД."""
    hits = es_search(query, es_client)

    documents = []
    for hit in hits:
        query = select(Document).where(Document.id == hit['id'])
        document = (await session.execute(query)).first()

        if document is not None:
            documents.append(document)

    documents.sort(key=lambda doc: doc.created_date)

    return documents
