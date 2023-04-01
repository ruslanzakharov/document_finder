from fastapi import FastAPI
import uvicorn

from app.api.v1 import routers


def bind_routers(application: FastAPI) -> None:
    for router in routers:
        application.include_router(router)


def get_application() -> FastAPI:
    application = FastAPI()
    bind_routers(application)

    return application


app = get_application()


if __name__ == '__main__':
    uvicorn.run('app.__main__:app', port=8000, host='0.0.0.0', reload=True)
