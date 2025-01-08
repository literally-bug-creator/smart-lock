from api.users import current_active_user
from schemas.file import params
from file_db import FileDBClient
from fastapi import Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator, TYPE_CHECKING
import os


if TYPE_CHECKING:
    from database.models import User


class FileService:
    def __init__(
        self,
        file_db_client: FileDBClient = Depends(),
        user: "User" = Depends(current_active_user),
    ):
        self.file_db_client = file_db_client

    async def read(self, params: params.Read) -> StreamingResponse:
        file = await self.file_db_client.read(params.key)
        if file is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "File not found")  # noqa
        return StreamingResponse(
            self._file_streamer(file),
            media_type="binary/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={params.key}"},
        )

    async def _file_streamer(self, file: bytes) -> AsyncGenerator[bytes, None]:
        CHUNK_SIZE = int(os.getenv("STREAMING_CHUNK_SIZE", 64 * 1024))
        for i in range(0, len(file), CHUNK_SIZE):
            yield file[i : i + CHUNK_SIZE]