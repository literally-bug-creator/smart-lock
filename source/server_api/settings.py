from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


SERVER_API_ENV = ".env.server-api"


class ServerAPISettings(BaseSettings):
    URL: str = Field()

    model_config = SettingsConfigDict(env_file=SERVER_API_ENV)
