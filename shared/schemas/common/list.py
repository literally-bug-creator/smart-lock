from .pagination import PaginationParams
from .sort import SortParams
from pydantic import BaseModel
from fastapi import Depends


class ListParams(BaseModel):
    pagination: PaginationParams = Depends()
    sort: SortParams = Depends()


class ListResponse[T](BaseModel):
    items: list[T]
    total: int
