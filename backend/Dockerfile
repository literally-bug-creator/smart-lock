# FROM python:3.12-slim

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# COPY ./requirements.txt /requirements.txt

# RUN pip3 install --no-cache-dir -r /requirements.txt

# ENV PYTHONPATH /project/source:/libs

# WORKDIR /project/source

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /project/source

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

ADD . /project/source
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

ENV PATH="/project/source/.venv/bin:$PATH"