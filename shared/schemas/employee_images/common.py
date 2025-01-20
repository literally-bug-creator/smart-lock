from pydantic import BaseModel, Field, AliasChoices
from fastapi import Query


class EmployeeImage(BaseModel):
    id: int
    employee_id: int = Field(
        serialization_alias="employeeId",
        validation_alias=AliasChoices("employeeId", "employee_id"),
    )
    file_key: str | None = Field(
        serialization_alias="fileKey",
        validation_alias=AliasChoices("fileKey", "file_key"),
    )


class EmployeeImageFilters(BaseModel):
    employee_id: int | None = Query(
        None,
        validation_alias="employeeId",
    )
