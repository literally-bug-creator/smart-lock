#!/bin/sh

sleep 3

uv run celery -A main.CELERY worker --pool=prefork --loglevel=info
