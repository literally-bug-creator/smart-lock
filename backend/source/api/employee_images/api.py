from fastapi import APIRouter, Depends, status

from services.employee_images import EmployeeImageService
from shared.schemas.employee_images import params, bodies, forms, responses
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


@router.patch(
    path=Path.UPDATE,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": responses.Update},
        status.HTTP_404_NOT_FOUND: {}
    }
)
async def update(
    body: bodies.Update,
    params: params.Update = Depends(),
    service: EmployeeImageService = Depends()
):
    return await service.update(params, body)


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


@router.delete(
    path=Path.DELETE_ALL,
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_404_NOT_FOUND: {}
    }
)
async def delete_all(
    params: params.DeleteAll = Depends(),
    service: EmployeeImageService = Depends()
):
    return await service.delete_all(params)


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
