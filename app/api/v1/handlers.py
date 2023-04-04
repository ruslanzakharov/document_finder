from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from elasticsearch import Elasticsearch

from app import schemas
from app.db import storage, get_session
from app.es import get_es_client
from app.utils import get_bd_search_response

search_router = APIRouter(prefix='/v1/documents')


@search_router.get(
    '/search',
    status_code=status.HTTP_200_OK,
    response_model=schemas.SearchResponse
)
async def search_documents(
        q: str = '',
        session: AsyncSession = Depends(get_session),
        es_client: Elasticsearch = Depends(get_es_client)
):
    documents = await get_bd_search_response(q, session, es_client)
    return {'documents': documents}


@search_router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.DocumentResponse
)
async def create_document(
        post_schema: schemas.DocumentCreateRequest,
        session: AsyncSession = Depends(get_session)
):
    document = await storage.create_document(post_schema, session)
    return document
