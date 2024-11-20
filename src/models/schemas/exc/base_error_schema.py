from pydantic import BaseModel


class BaseErrorSchema(BaseModel):
    name: str
    description: str | None = None
