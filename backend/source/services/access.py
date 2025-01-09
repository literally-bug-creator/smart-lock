from fastapi import Depends, HTTPException, status
from database.repos.employee_image import EmployeeImageRepo
from database.repos.employee import EmployeeRepo
from schemas.access import params, forms

from concurrent.futures import ProcessPoolExecutor
from io import BytesIO
import face_recognition
import asyncio


executor = ProcessPoolExecutor()


class AccessService:
    def __init__(
        self,
        repo: EmployeeImageRepo = Depends(),
        employee_repo: EmployeeRepo = Depends(),
    ):
        self.__repo = repo
        self.__employee_repo = employee_repo

    async def webhook(self, pms: params.Webhook, form: forms.Webhook) -> None:  # TODO: Implement service logic
        image_bytes = await form.file.read()
        try:
            loop = asyncio.get_running_loop()
            vector = await loop.run_in_executor(executor, process_image_from_memory, image_bytes)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        
        employee_image = await self.__repo.get_nearest_by_vector(vector=vector,)
        if employee_image is None:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "NO similar employee")  # noqa
        
        employee = await self.__employee_repo.get(id=employee_image.employee_id)
        if employee is None:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Database error")  # noqa
        
        if employee.access_level > pms.access_level:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied")

        return True
    

def process_image_from_memory(image_bytes: bytes):
    image = face_recognition.load_image_file(BytesIO(image_bytes))
    face_locations = face_recognition.face_locations(image)
    if not face_locations:
        raise ValueError("Лицо на изображении не найдено.")
    
    face_encodings = face_recognition.face_encodings(image, face_locations)
    if not face_encodings:
        raise ValueError("Не удалось извлечь эмбеддинг лица.")
    
    return face_encodings[0].tolist()
