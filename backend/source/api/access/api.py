from fastapi import APIRouter, Depends, status

from .settings import PREFIX, Paths
from services.access import AccessService


router = APIRouter(prefix=PREFIX, tags=["Access", ],)


@router.get(
    path=Paths.READ,
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