FROM python:3.12-alpine as builder

ENV POETRY_VERSION=1.8.3
RUN pip install "poetry==${POETRY_VERSION}"

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY README.md ./

RUN poetry config virtualenvs.in-project true && \
    poetry install --no-root && rm -rf $POETRY_CACHE_DIR


#################
FROM python:3.12-alpine

WORKDIR /app

COPY . .
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder /app/.venv .venv
COPY --from=builder /app ./

ENV DJANGO_SETTINGS_MODULE=music_dashboard.settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN python manage.py migrate && \
    python manage.py collectstatic --noinput

CMD ["uvicorn", "music_dashboard.asgi:application"]

