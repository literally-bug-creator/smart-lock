from .base import BaseRepo
from shared.database.models import Employee


class EmployeeRepo(BaseRepo[Employee]):
    MODEL = Employee