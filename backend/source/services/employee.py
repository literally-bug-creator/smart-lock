from database.repos.employee import EmployeeRepo
from database.repos.employee_image import EmployeeImageRepo
from database.models.employee import Employee as EmployeeModel
from fastapi import Depends, HTTPException, status
from schemas.employees import params, bodies, responses
from schemas.employees.common import Employee as EmployeeScheme
from file_db import FileDBClient


class EmployeeService:
    def __init__(
        self,
        repo: EmployeeRepo = Depends(),
        image_repo: EmployeeImageRepo = Depends(),
        file_db: FileDBClient = Depends()
    ):
        self.__repo = repo
        self.__image_repo = image_repo
        self.__file_db = file_db

    async def create(self, body: bodies.Create) -> responses.Create:
        obj = await self.__repo.new(**body.model_dump())
        if obj is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return responses.Create(item=EmployeeScheme.model_validate(obj, from_attributes=True))

    async def read(self, params: params.Read) -> responses.Read:
        obj = await self.__get_object(params.id)
        return responses.Read(item=EmployeeScheme.model_validate(obj, from_attributes=True))

    async def update(self, params: params.Update, body: bodies.Update) -> responses.Update:
        obj = await self.__get_object(params.id)
        updated_obj = await self.__update_obj(obj, body)
        obj = await self.__repo.update(updated_obj)
        if obj is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Employee cannot be updated")  # noqa

        return responses.Update(item=EmployeeScheme.model_validate(obj, from_attributes=True))

    async def delete(self, params: params.Delete) -> None:
        obj = await self.__get_object(params.id)
        await self.__delete_images(obj.id)
        await self.__repo.delete(obj)

    async def list(self, params: params.List) -> responses.List:
        items, total = await self.__repo.list(params=params)
        return responses.List(
            items=[EmployeeScheme.model_validate(
                obj, from_attributes=True) for obj in items],
            total=total,
        )

    async def __get_object(self, id: int) -> EmployeeModel:
        obj = await self.__repo.filter_one(id=id)
        if obj is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Employee not found")  # noqa
        return obj
    
    async def __update_obj(self, obj: EmployeeModel, body: bodies.Update):
        obj.full_name = body.full_name
        obj.access_level = body.access_level
        return obj
    
    async def __delete_images(self, employee_id: int) -> None:
        images = await self.__image_repo.filter(employee_id=employee_id)

        for image in images:
            await self.__delete_file(image.file_key)
            deleted = await self.__image_repo.delete(image)
            if not deleted:
                raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "EmployeeImage repo error")  # noqa

    async def __delete_file(self, file_key: str) -> None:
        deleted = await self.__file_db.delete(file_key)
        if not deleted:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "File storage error")  # noqa

