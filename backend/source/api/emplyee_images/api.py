from fastapi import APIRouter, Depends, status
from .settings import PREFIX, Path
from ...services.employee_images import EmployeeImagesService

router = APIRouter(prefix=PREFIX, tags=["EmployeeImage"])


@router.put(
    path=Path.CREATE,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: ... # TODO add EmployeeImageModel
        }
    )
async def create(service: EmployeeImagesService = Depends()):
    return await service.create()


@router.get(
    path=Path.READ,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: ...,  # TODO add EmployeeImageModel
        status.HTTP_404_NOT_FOUND: {}
        }
    )
async def read(service: EmployeeImagesService = Depends()):
    return await service.read()


@router.delete(
    path=Path.DELETE,
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_404_NOT_FOUND: {}
    }
)
async def delete(service: EmployeeImagesService = Depends()):
    return await service.delete()

router.get(
    path=Path.LIST,
    status_code=status.HTTP_200_OK,
    response={
        status.HTTP_200_OK: {
            items: EmployeeImagesModel,
            total: int
        }
    }
)
async def list(service: EmployeeImagesService = Depends()):
    return await service.list()

