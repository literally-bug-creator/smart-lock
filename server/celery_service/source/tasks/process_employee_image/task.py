from .worker import get_worker
from celery_app import CELERY
import asyncio


@CELERY.task(name="process_employee_image")
def process_employee_image(employee_id: int, image_id: int, image_bytes: bytes) -> None:
    worker = get_worker()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(worker.launch(employee_id, image_id, image_bytes))
