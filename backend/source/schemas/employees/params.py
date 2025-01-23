from pydantic import BaseModel
from shared.schemas.common import ListParams
from .common import EmployeeFilters
from fastapi import Path, Depends


class BaseParams(BaseModel):
    id: int = Path()


class Read(BaseParams): ...


class Update(BaseParams): ...


class Delete(BaseParams): ...


class List(ListParams):
    filters: EmployeeFilters = Depends()
