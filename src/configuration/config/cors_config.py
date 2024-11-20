from pydantic_settings import BaseSettings, SettingsConfigDict


class CorsConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="cors_", extra="ignore")

    allowed_origins: list[str] = ["*"]
    allowed_methods: list[str] = ["GET", "POST"]
    allowed_headers: list[str] = ["*"]
    allowed_credentials: bool = True
