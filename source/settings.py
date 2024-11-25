from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    BACKEND_ENDPOINT_URI: str | None = Field(default=None, alias="BACKEND_ENDPOINT_URI")
    COOLDOWN: int = Field(default=5, alias="COOLDOWN")


class LockSettings(BaseSettings):
    PIN: int = Field(default=11, alias="PIN")


class CameraSettings(BaseSettings): ...
