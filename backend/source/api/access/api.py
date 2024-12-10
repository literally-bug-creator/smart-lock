from fastapi import APIRouter, Depends, status
from services.access import AccessService

from .settings import PREFIX, Path

router = APIRouter(prefix=PREFIX, tags=["Access"])


@router.get(
    path=Path.READ,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {},
        status.HTTP_401_UNAUTHORIZED: {}
    },
)
async def read(
    service: AccessService = Depends(),
):
    return await service.read()
