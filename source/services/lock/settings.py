from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


LOCK_ENV = ".env.lock"


class LockSettings(BaseSettings):
    PIN: int = Field(default=11)

    model_config = SettingsConfigDict(env_file=LOCK_ENV)
