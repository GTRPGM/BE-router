# 1단계: 빌드 스테이지
FROM python:3.11-slim-bookworm AS builder

COPY --from=ghcr.io/astral-sh/uv:0.5.7 /uv /bin/uv

ENV UV_PROJECT_ENVIRONMENT="/usr/local"
WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

FROM python:3.11-slim-bookworm

ARG APP_PORT
ENV APP_PORT=${APP_PORT}
ENV PYTHONPATH="/app"

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY src /app/src
COPY pyproject.toml /app/pyproject.toml

LABEL authors="elian118"

EXPOSE ${APP_PORT}

HEALTHCHECK --start-period=20s --interval=30s --timeout=3s --retries=3 \
    CMD ["python", "-c", "import os, urllib.request; port=os.environ.get('APP_PORT'); urllib.request.urlopen(f'http://localhost:{port}/health')"]

CMD ["python", "src/main.py"]
