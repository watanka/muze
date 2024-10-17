FROM python:3.12-alpine as builder

ENV POETRY_VERSION=1.8.3
RUN pip install "poetry==${POETRY_VERSION}"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.in-project true && \
    poetry install --no-root --no-dev


## execute
RUN poetry build

FROM python:3.12-alpine

COPY --from=builder /app/.venv ./.venv
COPY --from=builder /app/dist .
COPY . .

ENV DJANGO_SETTINGS_MODULE=your_project_name.settings
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

RUN python manage.py migrate && \
    python manage.py collectstatic --noinput

CMD ["uvicorn", "music_dashboard.asgi:application"]

