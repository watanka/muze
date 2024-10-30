# Stage 1: Builder
FROM python:3.11-alpine as builder

WORKDIR /app
# Set environment variables to avoid creation of __pycache__ and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ENV POETRY_VERSION=1.8.3
RUN pip install "poetry==${POETRY_VERSION}"

# Install build dependencies
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    make

COPY pyproject.toml poetry.lock ./
COPY README.md ./

RUN poetry config virtualenvs.in-project true && \
    poetry install --no-root && rm -rf $POETRY_CACHE_DIR

# Stage 2: Final stage
FROM python:3.11-alpine

# Set work directory
WORKDIR /app

COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install runtime dependencies (minimal)
RUN apk update && apk add --no-cache \
    libffi \
    openssl \
    musl

RUN pip install poetry

# Copy installed dependencies from builder stage
COPY --from=builder /app/.venv .venv
COPY --from=builder /app ./

# Expose port (Flask default)
EXPOSE 5000

# Command to run the application
CMD ["poetry", "run", "python", "app.py"]
