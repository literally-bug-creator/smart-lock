from .base import Base
from fastapi_users.db import SQLAlchemyBaseUserTable


class User(Base, SQLAlchemyBaseUserTable[int]):  # type: ignore
    __tablename__ = "users"