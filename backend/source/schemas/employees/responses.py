from .common import Employee
from schemas.common import CRUDResponse, ListResponse


Create = CRUDResponse[Employee]
Read = CRUDResponse[Employee]
Update = CRUDResponse[Employee]
List = ListResponse[Employee]
