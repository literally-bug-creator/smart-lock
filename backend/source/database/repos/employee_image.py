from .base import BaseRepo
from database.models import EmployeeImage


class EmployeeImageRepo(BaseRepo[EmployeeImage]):
    MODEL = EmployeeImage