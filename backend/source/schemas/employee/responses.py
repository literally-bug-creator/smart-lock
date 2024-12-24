from .common import Employee
from schemas.common import CRUDResponse


Create = CRUDResponse[Employee]
Read = CRUDResponse[Employee]
Update = CRUDResponse[Employee]
