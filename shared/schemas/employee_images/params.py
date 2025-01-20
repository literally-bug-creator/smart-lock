from pydantic import BaseModel
from shared.schemas.common import ListParams
from .common import EmployeeImageFilters
from fastapi import Path, Depends


class BaseParams(BaseModel):
    employee_id: int = Path()


class Create(BaseParams):
    ...


class Read(BaseParams):
    id: int = Path()


class Update(BaseParams):
    id: int = Path()


class Delete(BaseParams):
    id: int = Path()


class DeleteAll(BaseParams):
    ...


class List(ListParams):
    filters: EmployeeImageFilters = Depends()