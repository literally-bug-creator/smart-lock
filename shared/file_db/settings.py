from pydantic_settings import BaseSettings
from pydantic import Field


class FileDBSettings(BaseSettings):
    endpoint_url: str = Field(validation_alias="FILE_DB_ENDPOINT_URL")
    access_key: str = Field(validation_alias="FILE_DB_ACCESS_KEY")
    secret_key: str = Field(validation_alias="FILE_DB_SECRET_KEY")
    bucket_name: str = Field(validation_alias="FILE_DB_BUCKET_NAME")


def get_file_db_settings() -> FileDBSettings:
    return FileDBSettings()  # type: ignore
