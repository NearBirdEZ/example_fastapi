from pydantic import Field

from .. import _BaseResponse


class Response(_BaseResponse):
    predicted_number: float = Field(..., alias="predictedNumber", examples=["0.8"], ge=0, le=1)
