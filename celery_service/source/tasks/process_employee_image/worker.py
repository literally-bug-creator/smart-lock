import asyncio
from .deps import WorkerDeps, get_worker_deps
from concurrent.futures import ProcessPoolExecutor
import os
from io import BytesIO
import face_recognition
from shared.schemas import employee_images
import logging
from fastapi import UploadFile
from io import BytesIO


#executor = ProcessPoolExecutor(max_workers=int(os.getenv("MAX_WORKERS", 2)))


class Worker:
    def __init__(
        self,
        deps: WorkerDeps | None = None,
    ):
        self.deps: WorkerDeps = deps or get_worker_deps()
        self.timeout = float(os.environ["PROCESS_FILE_TASK_TIMEOUT"])

    async def launch(self, employee_id: int, image_id: int, image_bytes: bytes) -> None:
        #try:
        logging.error(f"Launch task! {employee_id=}")
        await self._launch(employee_id, image_id, image_bytes)

        # except Exception as e:
        #     logging.error(str(e))
        #     try:
        #         params = employee_images.params.Delete(
        #             employee_id=employee_id,
        #             id=image_id,
        #         )
        #         await self.deps.employee_images_api.delete(params)
        #     except Exception as e:
        #         logging.error(str(e))

    async def _launch(self, employee_id: int, image_id: int, image_bytes: bytes) -> None:
        # loop = asyncio.get_running_loop()
        # image_vector = await asyncio.wait_for(
        #     loop.run_in_executor(executor, self.process_image_from_memory, image_bytes),
        #     timeout=self.timeout,
        # )
        image_vector = self.process_image_from_memory(image_bytes)
        await self._update_image(image_id, image_bytes, image_vector, employee_id)

    def process_image_from_memory(self, image_bytes: bytes):
        image = face_recognition.load_image_file(BytesIO(image_bytes))
        face_locations = face_recognition.face_locations(image)
        if not face_locations:
            raise ValueError("Лицо на изображении не найдено.")
        
        face_encodings = face_recognition.face_encodings(image, face_locations)
        if not face_encodings:
            raise ValueError("Не удалось извлечь эмбеддинг лица.")
        
        return face_encodings[0].tolist()

    async def _update_image(self, id: int, bytes: bytes, vector, employee_id: int):
        params = employee_images.params.Update(
            employee_id=employee_id,
            id=id,
        )
        # body = employee_images.bodies.Update(
        #     image_vector=vector,
        # )
        form = employee_images.forms.Update(file=UploadFile(BytesIO(bytes)), vector=vector)
        return await self.deps.employee_images_api.update(params, form)


def get_worker() -> Worker:
    return Worker()
