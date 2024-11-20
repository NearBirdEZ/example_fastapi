from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI, Request
from loguru import logger
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse, JSONResponse

from src import routes
from src.configuration import config, logger_init
from src.exc import ScaryException
from src.middlewares import LoggingMiddleware, UniqIdMiddleware
from src.models.schemas.exc import InternalErrorSchema, TeapotErrorSchema


async def exception_handler(_: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, ScaryException):
        return JSONResponse(
            content=TeapotErrorSchema(
                name=exc.__class__.__name__, description=f"Бу, испугался? Да ты не бойся. {str(exc)}"
            ).model_dump(),
            status_code=status.HTTP_418_IM_A_TEAPOT,
        )
    logger.exception(exc)
    return JSONResponse(
        content=InternalErrorSchema(
            name=exc.__class__.__name__, description=f"Call your administrator. Error={str(exc)}"
        ).model_dump(),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
        logger_init(config.log_level)
        logger.info(config)
        yield

    app = FastAPI(version=config.version, lifespan=lifespan)

    app.include_router(routes.health_router, prefix="/health")
    app.include_router(routes.foo_router, prefix="/v1")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors.allowed_origins,
        allow_credentials=config.cors.allowed_credentials,
        allow_methods=config.cors.allowed_methods,
        allow_headers=config.cors.allowed_headers,
    )
    app.middleware("http")(LoggingMiddleware())
    app.middleware("http")(UniqIdMiddleware())

    app.add_exception_handler(Exception, exception_handler)
    app.add_exception_handler(ScaryException, exception_handler)

    @app.get("/", include_in_schema=False)
    def docs_redirect() -> RedirectResponse:
        return RedirectResponse("/docs")

    return app


if __name__ == "__main__":
    application: FastAPI = create_app()
    uvicorn.run(application, host="0.0.0.0", port=8080, reload=False)
