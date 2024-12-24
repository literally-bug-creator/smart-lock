from fastapi import APIRouter, Depends, status
from services.employee import EmployeeService
from schemas.employees import params, bodies, responses

from .settings import PREFIX, Path

router = APIRouter(prefix=PREFIX, tags=["Employee"])


@router.put(
    path=Path.CREATE,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": responses.Create},
    },
)
async def create(
    body: bodies.Create,
    service: EmployeeService = Depends(),
):
    return await service.create(body)


@router.get(
    path=Path.READ,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": responses.Read},
        status.HTTP_404_NOT_FOUND: {},
    }
)
async def read(
    params: params.Read = Depends(),
    service: EmployeeService = Depends(),
):
    return await service.read(params)


@router.patch(
    path=Path.UPDATE,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": responses.Update},
        status.HTTP_404_NOT_FOUND: {},
    }
)
async def update(
    body: bodies.Update,
    params: params.Update = Depends(),
    service: EmployeeService = Depends()
):
    return await service.update(params, body)


@router.delete(
    path=Path.DELETE,
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_404_NOT_FOUND: {},
    }
)
async def delete(
    params: params.Delete = Depends(),
    service: EmployeeService = Depends()
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
    service: EmployeeService = Depends()
):
    return await service.list(params)
