#!/bin/sh

sleep 3

alembic upgrade head

uv run main.py

# sleep infinity
