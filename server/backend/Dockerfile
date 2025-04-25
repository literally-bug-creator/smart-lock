FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /project/source

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libboost-python-dev \
    libboost-thread-dev \
    python3-dev \
    gfortran && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

ADD . /project/source
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

ENV PATH="/project/source/.venv/bin:$PATH"
ENV PYTHONPATH /project/source:/libs:/libs/celery_service