from fastapi import APIRouter, Depends, status
from schemas.file import params
from services.file import FileService

from .settings import Paths, PREFIX

router = APIRouter(prefix=PREFIX, tags=["File"])


@router.get(
    path=Paths.Read,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {},
        status.HTTP_404_NOT_FOUND: {},
    },
    description="Получить ссылку для загрузки шаблона.",
)
async def read(
    params: params.Read = Depends(),
    service: FileService = Depends(),
):
    return await service.read(params)
