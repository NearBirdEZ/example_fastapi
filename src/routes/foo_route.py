from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from starlette import status

from ..configuration import config
from ..dependency import create_foo_service
from ..models.schemas import something_schema, predict_schema
from ..models.schemas.exc import InternalErrorSchema, TeapotErrorSchema
from ..services.foo_service import FooService

foo_router = APIRouter(
    tags=["Foo v1"],
    responses={
        status.HTTP_418_IM_A_TEAPOT: {"model": TeapotErrorSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": InternalErrorSchema},
    },
)


@foo_router.post("/do_something")
async def do_something(
    schema: something_schema.Request,
    service: Annotated[FooService, Depends(create_foo_service)],
) -> something_schema.Response:
    return await service.do_something(schema)


@foo_router.post("/predict")
async def predict(
    schema: predict_schema.Request,
    service: Annotated[FooService, Depends(create_foo_service)],
) -> predict_schema.Response:
    return await service.predict(schema)


@foo_router.get("/try_luck", description=f"{config.chance * 100}% выигрыша")
def try_luck(service: Annotated[FooService, Depends(create_foo_service)]) -> str:
    return service.try_luck(config.chance)
