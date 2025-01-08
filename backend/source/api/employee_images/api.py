from fastapi import APIRouter, Depends, status

from services.employee_images import EmployeeImageService
from schemas.employee_images import params, forms, responses
from .settings import PREFIX, Path

router = APIRouter(prefix=PREFIX, tags=["EmployeeImage"])


@router.put(
    path=Path.CREATE,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": responses.Create},
    }
)
async def create(
    params: params.Create = Depends(),
    form: forms.Create = Depends(forms.create),
    service: EmployeeImageService = Depends()
):
    return await service.create(params, form)


@router.get(
    path=Path.READ,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": responses.Read},
        status.HTTP_404_NOT_FOUND: {}
    }
)
async def read(
    params: params.Read = Depends(),
    service: EmployeeImageService = Depends()
):
    return await service.read(params)


@router.delete(
    path=Path.DELETE,
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_404_NOT_FOUND: {}
    }
)
async def delete(
    params: params.Delete = Depends(),
    service: EmployeeImageService = Depends()
):
    return await service.delete(params)


@router.get(
    path=Path.LIST,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": responses.List},
    }
)
async def list(
    params: params.List = Depends(),
    service: EmployeeImageService = Depends()
):
    return await service.list(params)
