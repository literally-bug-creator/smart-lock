from celery import Celery
from .settings import get_celery_settings


_settings = get_celery_settings()

CELERY = Celery(**_settings.model_dump())

CELERY.conf.update(_settings.model_dump())
