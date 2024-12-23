from .base import Base
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column
from enum import IntEnum


class EmployeeAccessLevel(IntEnum):
    ADMIN = 0
    DEFAULT = 1


class Employee(Base, SQLAlchemyBaseUserTable[int]):  # type: ignore
    __tablename__ = "employees"

    full_name: Mapped[str] = mapped_column()    
    access_level: Mapped[EmployeeAccessLevel] = mapped_column()