from pydantic import BaseModel
from database.models import EmployeeAccessLevel
from fastapi import Query


class Webhook(BaseModel):
    access_level: EmployeeAccessLevel = Query()
