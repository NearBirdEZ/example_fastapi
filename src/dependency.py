from fastapi import Request

from .services.foo_service import FooService


def create_foo_service(request: Request) -> FooService:
    return FooService(request.state.uniq_id)
