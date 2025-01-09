from concurrent.futures import ProcessPoolExecutor
from io import BytesIO
import face_recognition
import asyncio

from database.repos.employee_image import EmployeeImageRepo
from database.models.employee_image import EmployeeImage as EmployeeImageModel
from fastapi import Depends, HTTPException, status
from schemas.employee_images import params, forms, responses
from schemas.employee_images.common import EmployeeImage as EmployeeImageScheme
from file_db import FileDBClient


executor = ProcessPoolExecutor()


class EmployeeImageService:
    def __init__(
        self,
        repo: EmployeeImageRepo = Depends(),
        file_db: FileDBClient = Depends()
    ):
        self.__repo = repo
        self.__file_db = file_db

    async def create(self, params: params.Create, form: forms.Create) -> responses.Create:
        image_bytes = await form.file.read()
        try:
            loop = asyncio.get_running_loop()
            vector = await loop.run_in_executor(executor, process_image_from_memory, image_bytes)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        key = await self._save_file(image_bytes)
        obj = await self.__repo.new(
            employee_id=params.employee_id,
            file_key=key,
            image_vector=vector,
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

    async def delete_all(self, params: params.Delete) -> None:
        objs = await self.__get_objects(params.employee_id)
        for obj in objs:
            await self.__delete_file(obj.file_key)
            await self.__repo.delete(obj)

    async def list(self, params: params.List) -> responses.List:
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

    async def __delete_file(self, file_key: str) -> None:
        deleted = await self.__file_db.delete(file_key)
        if not deleted:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "File storage error")  # noqa
        
def process_image_from_memory(image_bytes: bytes):
    image = face_recognition.load_image_file(BytesIO(image_bytes))
    face_locations = face_recognition.face_locations(image)
    if not face_locations:
        raise ValueError("Лицо на изображении не найдено.")
    
    face_encodings = face_recognition.face_encodings(image, face_locations)
    if not face_encodings:
        raise ValueError("Не удалось извлечь эмбеддинг лица.")
    
    return face_encodings[0].tolist()

