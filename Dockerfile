FROM python:3.12-slim

ENV POETRY_VERSION=1.8.3
RUN pip install "poetry==${POETRY_VERSION}" 

COPY pyproject.toml poetry.lock ./
COPY wait-for-it.sh /usr/local/bin/wait-for-it
RUN chmod +x /usr/local/bin/wait-for-it

RUN apt-get update && apt-get install -y \
        python3-dev \
        build-essential \
        libmariadb-dev \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*


RUN poetry config virtualenvs.create false && poetry install

WORKDIR /app
COPY . /app

ENV DJANGO_SETTINGS_MODULE=music_dashboard.settings \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

CMD ["uvicorn", "music_dashboard.asgi:application", "--host", "0.0.0.0", "--port", "8000"]


