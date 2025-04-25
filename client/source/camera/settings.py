from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


CAMERA_ENV = ".env.camera"


class CameraSettings(BaseSettings):
    INDEX: int = Field(default=0)
    WIDTH: int = Field(default=480)
    HEIGHT: int = Field(default=640)
    IMG_PATH: str = Field(default="img.png")

    model_config = SettingsConfigDict(env_file=CAMERA_ENV)
