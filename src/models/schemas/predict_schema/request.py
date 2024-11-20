from pydantic import ConfigDict, BaseModel, Field


class Request(BaseModel):
    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    seed: int = Field(..., examples=[154])
