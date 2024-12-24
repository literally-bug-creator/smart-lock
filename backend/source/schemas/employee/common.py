from pydantic import BaseModel, Field, AliasChoices
from database.models import EmployeeAccessLevel


class Employee(BaseModel):
    id: int
    full_name: str = Field(
        serialization_alias="fullName",
        validation_alias=AliasChoices("fullName", "full_name"),
    )
    access_level: EmployeeAccessLevel = Field(
        serialization_alias="accessLevel",
        validation_alias=AliasChoices("accessLevel", "access_level"),
    )