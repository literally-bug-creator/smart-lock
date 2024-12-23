#!/bin/sh

sleep 3

uv run alembic upgrade head

uv run main.py

# sleep infinity
