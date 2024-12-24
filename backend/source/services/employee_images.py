from typing import TYPE_CHECKING

from api.users import current_active_user
from database.repos.employee_image import EmployeeImageRepo
from database.models.employee_image import EmployeeImage as EmployeeImageModel
from fastapi import Depends, HTTPException, status, UploadFile
from schemas.employee_images import params, forms, responses
from schemas.employee_images.common import EmployeeImage as EmployeeImageScheme
from file_db import FileDBClient

if TYPE_CHECKING:
    from database.models import User


class EmployeeImageService:
    def __init__(
        self,
        user: "User" = Depends(current_active_user),
        repo: EmployeeImageRepo = Depends(),
        file_db: FileDBClient = Depends()
    ):
        self.__user = user
        self.__repo = repo
        self.__file_db = file_db

    async def create(self, params: params.Create, form: forms.Create) -> responses.Create:  # TODO: Implement vector calculate and etc.
        key = await self._save_file(form.file)
        obj = await self.__repo.new(
            employee_id=params.employee_id,
            file_key=key,
        )
        if obj is None:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Database error")  # noqa

        return responses.Create(item=EmployeeImageScheme.model_validate(obj, from_attributes=True,),)

    async def read(self, params: params.Read) -> responses.Read:
        obj = await self.__get_object(params.id, params.employee_id)
        return responses.Read(item=EmployeeImageScheme.model_validate(obj, from_attributes=True),)

    async def delete(self, params: params.Delete) -> None:
        obj = await self.__get_object(params.id, params.employee_id)
        await self.__delete_file(obj.file_key)
        await self.__repo.delete(obj)

    async def list(self, params: params.List) -> responses.List:
        items, total = await self.__repo.list(params=params)
        return responses.List(
            items=[EmployeeImageScheme.model_validate(
                obj, from_attributes=True) for obj in items],
            total=total,
        )
    
    async def _save_file(self, file: UploadFile) -> str:
        key = await self.__file_db.save(await file.read())
        if key is None:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "File storage error")  # noqa
        return key

    async def __get_object(self, id: int, employee_id: int) -> EmployeeImageModel:
        obj = await self.__repo.filter_one(id=id, employee_id=employee_id)
        if obj is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "EmployeeImage not found")  # noqa
        return obj

    async def __delete_file(self, file_key: str) -> None:
        deleted = await self.__file_db.delete(file_key)
        if not deleted:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "File storage error")  # noqa

