from pydantic import Field
from pydantic_settings import BaseSettings


class CelerySettings(BaseSettings):
    main: str = Field(validation_alias="CELERY_APP_NAME")
    backend: str = Field(validation_alias="CELERY_RESULT_BACKEND_URL")
    broker: str = Field(validation_alias="CELERY_BROKER_URL")
    task_serializer: str = Field(
        default="json", validation_alias="CELERY_TASK_SERIALIZER")
    result_serializer: str = Field(
        default="json", validation_alias="CELERY_RESULT_SERIALIZER")
    accept_content: list[str] = Field(
        default=["json",], validation_alias="CELERY_ACCEPT_CONTENT")
    timezone: str = Field(default="UTC", validation_alias="CELERY_TIMEZONE")
    enable_utc: bool = Field(
        default=True, validation_alias="CELERY_ENABLE_UTC")


def get_celery_settings() -> CelerySettings:
    return CelerySettings()  # type: ignore


__all__ = [
    "CelerySettings",
    "get_celery_settings",
]
