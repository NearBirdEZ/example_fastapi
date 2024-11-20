from pydantic import Field

from ... import _BaseResponse
from . import SomeSchema


class Response(_BaseResponse):
    some: SomeSchema
    boo: str = Field(..., examples=["some string"])
    doo: int = Field(..., examples=[81])
