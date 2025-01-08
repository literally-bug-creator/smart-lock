from pydantic import BaseModel
from schemas.common import ListParams
from .common import EmployeeImageFilters
from fastapi import Path, Query, Depends


class BaseParams(BaseModel):
    id: int = Path()
    employee_id: int = Path()


class Create(BaseModel):
    employee_id: int = Path()


class Read(BaseParams):
    ...


class Delete(BaseParams):
    ...


class List(ListParams):
    filters: EmployeeImageFilters = Depends()