from .common import EmployeeImage
from schemas.common import CRUDResponse, ListResponse


Create = CRUDResponse[EmployeeImage]
Read = CRUDResponse[EmployeeImage]
List = ListResponse[EmployeeImage]
