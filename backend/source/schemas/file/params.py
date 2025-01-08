from pydantic import BaseModel
from fastapi import Path


class Read(BaseModel):
    key: str = Path()