from .base import BaseRepo
from database.models import Employee


class EmployeeRepo(BaseRepo[Employee]):
    MODEL = Employee
