import os
from io import BytesIO
import face_recognition
import logging


class Worker:
    def __init__(
        self,
    ):
        self.timeout = float(os.environ["PROCESS_FILE_TASK_TIMEOUT"])

    async def launch(self, image_bytes: bytes) -> None:
        try:
            return await self._launch(image_bytes)
        except Exception as e:
            logging.error(e)
            return None

    async def _launch(self, image_bytes: bytes) -> None:
        image_vector = self.process_image_from_memory(image_bytes)
        return image_vector

    def process_image_from_memory(self, image_bytes: bytes):
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
