from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import storage, get_session
from app import schemas

search_router = APIRouter(prefix='/v1/documents')


@search_router.get(
    '/search',
    status_code=status.HTTP_200_OK
)
async def search_documents(
        session: AsyncSession = Depends(get_session)
):
    return {'message': 'Нашел!'}


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
