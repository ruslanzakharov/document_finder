from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from app.api.v1 import routers
from app.db import create_db
from app.es import init_es


def bind_routers(application: FastAPI) -> None:
    for router in routers:
        application.include_router(router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_es()
    await create_db()
    yield


def get_application() -> FastAPI:
    application = FastAPI(lifespan=lifespan)
    bind_routers(application)

    return application


app = get_application()


if __name__ == '__main__':
    uvicorn.run('app.__main__:app', port=8000, host='0.0.0.0', reload=True)
