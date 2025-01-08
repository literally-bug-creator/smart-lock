from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from pgvector.sqlalchemy import Vector


class EmployeeImage(Base):
    __tablename__ = "employee_images"

    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))  # noqa
    file_key: Mapped[str] = mapped_column()
    image_vector = mapped_column(Vector(128))