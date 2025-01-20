from fastapi import Depends, HTTPException, status

from shared.database.repos.employee_image import EmployeeImageRepo
from shared.database.models.employee_image import EmployeeImage as EmployeeImageModel
from shared.schemas.employee_images import params, bodies, forms, responses
from shared.schemas.employee_images.common import EmployeeImage as EmployeeImageScheme

from shared.file_db import FileDBClient
from celery_service.tasks import process_employee_image


class EmployeeImageService:
    def __init__(
        self,
        repo: EmployeeImageRepo = Depends(),
        file_db: FileDBClient = Depends()
    ):
        self.__repo = repo
        self.__file_db = file_db

    async def create(self, params: params.Create, form: forms.Create) -> responses.Create: # type: ignore
        image_bytes = await form.file.read()
        obj = await self.__repo.new(
            employee_id=params.employee_id,
            file_key=None,
            image_vector=None,
        )

        if obj is None:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Database error")  # noqa
        
        process_employee_image.delay(obj.employee_id, obj.id, image_bytes)
        return responses.Create(item=EmployeeImageScheme.model_validate(obj, from_attributes=True,),)
    
    async def update(self, params: params.Update, body: bodies.Update) -> responses.Update: # type: ignore
        obj = await self.__get_object(params.id, params.employee_id)
        updated_obj = await self.__update_obj(obj, body)
        obj = await self.__repo.update(updated_obj)
        if obj is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "EmployeeImage cannot be updated")  # noqa

        return responses.Update(item=EmployeeImageScheme.model_validate(obj, from_attributes=True))

    async def read(self, params: params.Read) -> responses.Read: # type: ignore
        obj = await self.__get_object(params.id, params.employee_id)
        return responses.Read(item=EmployeeImageScheme.model_validate(obj, from_attributes=True),)

    async def delete(self, params: params.Delete) -> None:
        obj = await self.__get_object(params.id, params.employee_id)
        if obj.file_key is not None:
            await self.__delete_file(obj.file_key)
        await self.__repo.delete(obj)

    async def delete_all(self, params: params.Delete) -> None:
        objs = await self.__get_objects(params.employee_id)
        for obj in objs:
            if obj.file_key is not None:
                await self.__delete_file(obj.file_key)
            await self.__repo.delete(obj)

    async def list(self, params: params.List) -> responses.List: # type: ignore
        items, total = await self.__repo.list(params=params)
        return responses.List(
            items=[EmployeeImageScheme.model_validate(
                obj, from_attributes=True) for obj in items],
            total=total,
        )
    
    async def _save_file(self, file_bytes) -> str:
        key = await self.__file_db.save(file_bytes)
        if key is None:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "File storage error")  # noqa
        return key

    async def __get_object(self, id: int, employee_id: int) -> EmployeeImageModel:
        obj = await self.__repo.filter_one(id=id, employee_id=employee_id)
        if obj is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "EmployeeImage not found")  # noqa
        return obj
    
    async def __get_objects(self, employee_id: int) -> EmployeeImageModel:
        objs = await self.__repo.filter(employee_id=employee_id)
        if objs is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "EmployeeImages not found")  # noqa
        return objs
    
    async def __update_obj(self, obj: EmployeeImageModel, body: bodies.Update) -> EmployeeImageModel:
        obj.image_vector = body.image_vector
        obj.file_key = body.file_key
        return obj

    async def __delete_file(self, file_key: str) -> None:
        deleted = await self.__file_db.delete(file_key)
        if not deleted:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "File storage error")  # noqa
