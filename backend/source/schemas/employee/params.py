from pydantic import BaseModel
from fastapi import Path


class BaseParams(BaseModel):
    id: int = Path()


class Read(BaseParams):
    ...


class Update(BaseParams):
    ...


class Delete(BaseParams):
    ...