from typing import Awaitable, Callable
from fastapi import Request, Response
import uuid


class UniqIdMiddleware:
    async def __call__(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        request.state.uniq_id = str(uuid.uuid4())
        return await call_next(request)
