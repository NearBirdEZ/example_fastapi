from pydantic import Field

from ....enums import GenderEnum
from ... import _Base


class OuterContextItem(_Base):
    sex: GenderEnum = Field(..., alias="sex", examples=[GenderEnum.MALE])
    age: int = Field(..., alias="age", examples=[25])
    user_id: str = Field(..., alias="userId", examples=["111"])
    session_id: str = Field(..., alias="sessionId", examples=["222"])
    client_id: str = Field(..., alias="clientId", examples=["some_client"])
