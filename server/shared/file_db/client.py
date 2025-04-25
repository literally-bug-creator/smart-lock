from .settings import FileDBSettings, get_file_db_settings
from contextlib import asynccontextmanager
from aiobotocore.session import get_session
from botocore.exceptions import ClientError
from fastapi import Depends
from uuid import uuid4


class FileDBClient:
    def __init__(self, settings: FileDBSettings = Depends(get_file_db_settings)):
        self.settings = settings
        self.config = {
            "aws_access_key_id": settings.access_key,
            "aws_secret_access_key": settings.secret_key,
            "endpoint_url": settings.endpoint_url,
        }
        self.session = get_session()

    async def save(self, file: bytes, filename: str | None = None) -> str | None:
        key = str(uuid4())
        if filename and "." in filename:
            key = f"{key}.{filename.split('.')[-1]}"
        try:
            async with self._get_client() as client:
                await client.put_object(  # type: ignore
                    Bucket=self.settings.bucket_name,
                    Key=key,
                    Body=file,
                )
        except ClientError:
            return None
        return key

    async def exists(self, key: str) -> bool:
        try:
            async with self._get_client() as client:
                await client.head_object(  # type: ignore
                    Bucket=self.settings.bucket_name,
                    Key=key,
                )
        except ClientError:
            return False
        return True

    async def read(self, key: str) -> bytes | None:
        try:
            async with self._get_client() as client:
                response = await client.get_object(  # type: ignore
                    Bucket=self.settings.bucket_name,
                    Key=key,
                )
                return await response["Body"].read()
        except ClientError:
            return None

    async def delete(self, key: str) -> bool:
        try:
            async with self._get_client() as client:
                await client.delete_object(  # type: ignore
                    Bucket=self.settings.bucket_name,
                    Key=key,
                )
        except ClientError:
            return False
        return True

    @asynccontextmanager
    async def _get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            await self._create_bucket(client)
            yield client

    async def _create_bucket(self, client):
        try:
            await client.head_bucket(Bucket=self.settings.bucket_name)
        except ClientError:
            await client.create_bucket(Bucket=self.settings.bucket_name)
