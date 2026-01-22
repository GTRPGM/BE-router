FROM python:3.11-slim-bookworm AS builder

COPY --from=ghcr.io/astral-sh/uv:0.5.7 /uv /bin/uv

ENV UV_PROJECT_ENVIRONMENT="/usr/local"
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

FROM python:3.11-slim-bookworm

WORKDIR /app
ENV PYTHONPATH="/app"

COPY --from=builder /usr/local/lib/python3.11/site-packages \
                    /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY src /app/src
COPY pyproject.toml /app/pyproject.toml

LABEL authors="elian118"
EXPOSE 8010

CMD ["python", "src/main.py"]
