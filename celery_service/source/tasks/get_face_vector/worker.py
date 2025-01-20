import asyncio
from concurrent.futures import ProcessPoolExecutor
import os
from io import BytesIO
import face_recognition
from shared.schemas import employee_images


executor = ProcessPoolExecutor(max_workers=int(os.getenv("MAX_WORKERS", 2)))


class Worker:
    def __init__(
        self,
    ):
        self.timeout = float(os.environ["PROCESS_FILE_TASK_TIMEOUT"])

    async def launch(self, employee_id: int, image_id: int, image_bytes: bytes) -> None:
        try:
            return await self._launch(employee_id, image_id, image_bytes)
        
        finally: return None

    async def _launch(self, employee_id: int, image_id: int, image_bytes: bytes) -> None:
        loop = asyncio.get_running_loop()
        image_vector = await asyncio.wait_for(
            loop.run_in_executor(executor, self.process_image_from_memory, image_bytes),
            timeout=self.timeout,
        )
        return image_vector

    def process_image_from_memory(image_bytes: bytes):
        image = face_recognition.load_image_file(BytesIO(image_bytes))
        face_locations = face_recognition.face_locations(image)
        if not face_locations:
            raise ValueError("Лицо на изображении не найдено.")
        
        face_encodings = face_recognition.face_encodings(image, face_locations)
        if not face_encodings:
            raise ValueError("Не удалось извлечь эмбеддинг лица.")
        
        return face_encodings[0].tolist()


def get_worker() -> Worker:
    return Worker()
