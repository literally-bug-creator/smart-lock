from pydantic import BaseModel
from database.models import EmployeeAccessLevel


class Create(BaseModel):
    full_name: str
    access_level: EmployeeAccessLevel


class Update(BaseModel):
    full_name: str
    access_level: EmployeeAccessLevel
