from .common import EmployeeImage
from shared.schemas.common import CRUDResponse, ListResponse


Create = CRUDResponse[EmployeeImage]
Read = CRUDResponse[EmployeeImage]
Update = CRUDResponse[EmployeeImage]
List = ListResponse[EmployeeImage]
