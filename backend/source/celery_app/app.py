from celery import Celery
from .settings import get_celery_settings


_settings = get_celery_settings()

client = Celery(**_settings.model_dump())

client.conf.update(_settings.model_dump())
