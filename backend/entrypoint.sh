#!/bin/sh

sleep 3

alembic upgrade head

python3 main.py

# sleep infinity
