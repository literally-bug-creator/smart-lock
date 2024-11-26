from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


COMMON_ENV = ".env"


class CommonSettings(BaseSettings):
    BACKEND_ENDPOINT_URI: str | None = Field(default=None)
    COOLDOWN: int = Field(default=5)

    model_config = SettingsConfigDict(env_file=COMMON_ENV)
