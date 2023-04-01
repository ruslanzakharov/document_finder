from fastapi import APIRouter
from starlette import status

search_router = APIRouter(prefix='/v1/documents')


@search_router.get(
    '/search',
    status_code=status.HTTP_200_OK
)
async def search():
    return {'message': 'Нашел!'}
