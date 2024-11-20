from pydantic import BaseModel, ConfigDict


class _Base(BaseModel):
    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)
