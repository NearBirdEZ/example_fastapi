import asyncio
import random

from loguru import logger

from ..exc import ScaryException
from ..models.schemas import predict_schema, something_schema
from ..models.schemas.something_schema import SomeSchema


class FooService:
    __slots__ = ("_uniq_id",)

    def __init__(self, uniq_id: str) -> None:
        self._uniq_id: str = uniq_id

    async def do_something(self, request: something_schema.Request) -> something_schema.Response:
        logger.debug(request)
        logger.info("Some process request")
        await asyncio.sleep(0.3)
        logger.info("Wakeup")
        return something_schema.Response(
            some=SomeSchema(
                foo=f"{request.outer_context.user_id=}",
                boo=f"{request.outer_context.session_id=}",
            ),
            uniq_id=self._uniq_id,
            boo=request.text,
            doo=random.randint(0, 10),
        )

    async def predict(self, request: predict_schema.Request) -> predict_schema.Response:
        logger.debug(request)
        rand_gen = random.Random(request.seed)
        logger.info("Some predict")
        await asyncio.sleep(0.3)
        return predict_schema.Response(uniq_id=self._uniq_id, predicted_number=rand_gen.random())

    def try_luck(self, chance: float) -> str:
        if random.random() >= chance:  # Всегда в пользу казино
            logger.info(f"User lose with chance {chance}")
            raise ScaryException("You lose ha-ha-ha")
        logger.info(f"User win with chance {chance}")
        return f"You are lucky ass. Your ticket is '{self._uniq_id}'"
