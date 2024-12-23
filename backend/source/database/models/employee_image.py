from .base import Base
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from pgvector.sqlalchemy import Vector


class EmployeeImage(Base, SQLAlchemyBaseUserTable[int]):  # type: ignore
    __tablename__ = "employee_images"

    employee_id = Mapped[int] = mapped_column(ForeignKey("employees.id"))  # noqa
    full_name: Mapped[str] = mapped_column()
    file_id: Mapped[str] = mapped_column()
    image_vector: Mapped[Vector] = mapped_column()