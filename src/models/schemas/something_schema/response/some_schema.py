from pydantic import Field

from ... import _Base


class SomeSchema(_Base):
    foo: str = Field(..., examples=["some string foo"])
    boo: str = Field(..., examples=["some string boo"])
