from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


COMMON_ENV = ".env"
LOCK_ENV = ".env.lock"
CAMERA_ENV = ".env.camera"
FACE_RECOGNIZER_ENV = ".env.face_recognizer"


class CommonSettings(BaseSettings):
    BACKEND_ENDPOINT_URI: str | None = Field(default=None)
    COOLDOWN: int = Field(default=5)

    model_config = SettingsConfigDict(env_file=COMMON_ENV)


class LockSettings(BaseSettings):
    PIN: int = Field(default=11)

    model_config = SettingsConfigDict(env_file=LOCK_ENV)


class CameraSettings(BaseSettings):
    CAMERA_INDEX: int = Field(default=0, alias="INDEX")
    IMG_HEIGHT: int = Field(default=640, alias="HEIGHT")
    IMG_WIDTH: int = Field(default=480, alias="WIDTH")

    model_config = SettingsConfigDict(env_file=CAMERA_ENV)


class FaceRecognizerSettings(BaseSettings):
    CLASSIFIER: str = Field(default="haarcascade_frontalface_default.xml")
    SCALE_FACTOR: float = Field(default=1.1)
    MIN_NEIGHBORS: int = Field(default=5)
    MIN_SIZE_X: int = Field(default=30)
    MIN_SIZE_Y: int = Field(default=30)

    model_config = SettingsConfigDict(env_file=FACE_RECOGNIZER_ENV)
