from shared.apis.employee_images import EmployeeImagesAPI
from pydantic import BaseModel
from fastapi import Depends
import os
from shared.file_db import FileDBClient, get_file_db_settings


def get_employee_images_api() -> EmployeeImagesAPI:
    return EmployeeImagesAPI(url=os.getenv("EMPLOYEE_IMAGES_API_URL"))


class WorkerDeps(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    employee_images_api: EmployeeImagesAPI = Depends(get_employee_images_api)
    file_db_client: FileDBClient


def get_worker_deps() -> WorkerDeps:
    file_db_settings = get_file_db_settings()
    file_db_client = FileDBClient(file_db_settings)
    employee_images_api = get_employee_images_api()
    return WorkerDeps(file_db_client=file_db_client, employee_images_api=employee_images_api)


__all__ = [
    "WorkerDeps",
    "get_worker_deps",
]
