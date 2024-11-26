from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


FACE_RECOGNIZER_ENV = ".env.face_recognizer"


class FaceRecognizerSettings(BaseSettings):
    CLASSIFIER: str = Field(default="haarcascade_frontalface_default.xml")
    SCALE_FACTOR: float = Field(default=1.1)
    MIN_NEIGHBORS: int = Field(default=5)
    MIN_SIZE_X: int = Field(default=30)
    MIN_SIZE_Y: int = Field(default=30)

    model_config = SettingsConfigDict(env_file=FACE_RECOGNIZER_ENV)
