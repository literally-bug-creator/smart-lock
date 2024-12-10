from fastapi import APIRouter, Depends, status
from services.employee import EmployeeService

from .settings import PREFIX, Path

router = APIRouter(prefix=PREFIX, tags=["Employee"])


@router.put(
    path=Path.CREATE,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {},  # TODO: Add proper responce model
        status.HTTP_401_UNAUTHORIZED: {}
    },
)
async def create(
    service: EmployeeService = Depends(),
):  # TODO: Add proper args, responces and etc.
    return await service.create()


@router.get(
    path=Path.READ,
    status_code=status.HTTP_200_OK,
    responces={
        status.HTTP_200_OK: {},
        status.HTTP_401_UNAUTHORIZED: {}
    }
)
async def read(
    service: EmployeeService = Depends(),
):  # TODO: Add proper args, responces and etc...
    return await service.read()


@router.patch(
    path=Path.UPDATE,
    status_code=status.HTTP_202_ACCEPTED,
    responces={
        status.HTTP_202_ACCEPTED: {},
        status.HTTP_401_UNAUTHORIZED: {}
    }
)
async def update(
    service: EmployeeService = Depends()
):  # TODO: Add proper args, responces and etc.
    return await service.update()


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
