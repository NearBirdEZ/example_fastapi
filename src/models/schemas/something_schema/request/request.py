from pydantic import Field

from . import OuterContextItem
from ... import _Base


class Request(_Base):
    text: str = Field(..., alias="text")
    outer_context: OuterContextItem = Field(..., alias="outerContext")
