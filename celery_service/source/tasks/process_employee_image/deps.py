from shared.apis.employee_images import EmployeeImagesAPI
from pydantic import BaseModel
from fastapi import Depends
import os




def get_employee_images_api() -> EmployeeImagesAPI:
    return EmployeeImagesAPI(url=os.getenv("EMPLOYEE_IMAGES_API_URL"))


class WorkerDeps(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    employee_images_api: EmployeeImagesAPI = Depends(get_employee_images_api)


def get_worker_deps() -> WorkerDeps:
    employee_images_api = get_employee_images_api()
    return WorkerDeps(employee_images_api=employee_images_api)


__all__ = [
    "WorkerDeps",
    "get_worker_deps",
]
