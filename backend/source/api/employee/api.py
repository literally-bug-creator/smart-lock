from fastapi import APIRouter, Depends, status
from services.employee import EmployeeService
from schemas.employee import params, bodies, responses

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
    responces={
        status.HTTP_200_OK: {"model": responses.Read},
        status.HTTP_404_NOT_FOUND: {},
    }
)
async def read(
    params: params.Read,
    service: EmployeeService = Depends(),
):
    return await service.read(params)


@router.patch(
    path=Path.UPDATE,
    status_code=status.HTTP_200_OK,
    responces={
        status.HTTP_200_OK: {"model": responses.Update},
        status.HTTP_404_NOT_FOUND: {},
    }
)
async def update(
    params: params.Update,
    body: bodies.Update,
    service: EmployeeService = Depends()
):
    return await service.update(params, body)


@router.delete(
    path=Path.DELETE,
    status_code=status.HTTP_204_NO_CONTENT,
    responces={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_404_NOT_FOUND: {},
    }
)
async def delete(
    params: params.Delete,
    service: EmployeeService = Depends()
):
    return await service.delete(params)


@router.get(
    path=Path.LIST,
    status_code=status.HTTP_200_OK,
    responces={
        status.HTTP_200_OK: {},
        status.HTTP_401_UNAUTHORIZED: {}
    }
)
async def list(
    service: EmployeeService = Depends()
):  # TODO: Add proper args, responces and etc.
    return await service.list()
