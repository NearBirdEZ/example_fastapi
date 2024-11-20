import os

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

from . import CorsConfig
from ...models.enums import LogLevelEnum

_ENV_FILE: str = os.getenv("ENV_FILE", ".env")

load_dotenv(_ENV_FILE)


class Config(BaseSettings):
    cors: CorsConfig = CorsConfig()
    chance: float = Field(0.1, ge=0, le=1)
    log_level: LogLevelEnum = LogLevelEnum.INFO
    version: str = "dev"


config = Config()
