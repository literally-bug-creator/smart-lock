from fastapi import APIRouter, File, UploadFile, status

from .settings import PREFIX, Paths

router = APIRouter(prefix=PREFIX, tags=["Identification"])


@router.post(
    Paths.READ,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {},
        status.HTTP_401_UNAUTHORIZED: {},
    },
    description="Идентифицировать изображение с лицом",
)
async def indetify_person(file: UploadFile = File()): ...
