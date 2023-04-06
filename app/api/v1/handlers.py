from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.db import get_session, storage
from app import utils
from app.es import es_client

search_router = APIRouter(prefix='/v1/documents')


@search_router.get(
    '/search',
    status_code=status.HTTP_200_OK,
    response_model=schemas.SearchResponse
)
async def search_documents(
        q: str = '',
        session: AsyncSession = Depends(get_session),
):
    documents = await utils.get_bd_search_response(q, session, es_client)
    return {'documents': documents}


@search_router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.DocumentResponse
)
async def create_document(
        post_schema: schemas.DocumentCreateRequest,
        session: AsyncSession = Depends(get_session),
):
    document = await utils.create_document(post_schema, session, es_client)
    return document


@search_router.delete(
    '/{document_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Template not found",
        },
    }
)
async def delete_document(
        document_id: int,
        session: AsyncSession = Depends(get_session),
):
    document = await storage.get_document(document_id, session)

    if document:
        await utils.delete_document(document_id, session, es_client)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
