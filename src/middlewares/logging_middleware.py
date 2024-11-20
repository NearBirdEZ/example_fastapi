from typing import Awaitable, Callable
from fastapi import Request, Response
from loguru import logger


class LoggingMiddleware:
    async def __call__(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        with logger.contextualize(uuid=request.state.uniq_id):
            # W1203 в loguru не работает
            logger.info(f"Request: path={request.url.path}, method={request.method}")
            response: Response = await call_next(request)
            logger.info(
                f"Response: path={request.url.path}, method={request.method}, status code={response.status_code}"
            )
            return response
