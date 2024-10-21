FROM python:3.12-alpine as builder

ENV POETRY_VERSION=1.8.3
RUN pip install "poetry==${POETRY_VERSION}"

WORKDIR /app

RUN apk update && \
    apk add --no-cache \
        python3-dev \
        build-base \
        mariadb-dev

COPY pyproject.toml poetry.lock ./
COPY README.md ./

RUN poetry config virtualenvs.in-project true && \
    poetry install --no-root && rm -rf $POETRY_CACHE_DIR


#################
FROM python:3.12-alpine

WORKDIR /app

RUN apk update && \
    apk add --no-cache mariadb-dev

COPY . .
COPY --from=builder /app/.venv .venv
COPY --from=builder /app ./
RUN pip install poetry && poetry install

ENV PATH="/app/.venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE=music_dashboard.settings \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

CMD ["poetry", "run", "uvicorn music_dashboard.asgi:application --host 0.0.0.0 --port 8000"]


