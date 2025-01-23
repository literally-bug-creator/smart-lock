from workers.get_face_vector import get_worker
from celery_app import CELERY
import asyncio


@CELERY.task(name="get_face_vector")
def get_face_vector(image_bytes: bytes) -> None:
    worker = get_worker()
    loop = asyncio.get_event_loop()
    vector = loop.run_until_complete(worker.launch(image_bytes))
    return vector
