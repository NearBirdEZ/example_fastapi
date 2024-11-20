from uuid import UUID

from pydantic import Field

from . import _Base


class _BaseResponse(_Base):
    uniq_id: str = Field(..., alias="uniqId", examples=[str(UUID(int=583231))])
