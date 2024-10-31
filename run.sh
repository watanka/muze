#!/bin/bash

export DJANGO_SETTINGS_MODULE=music_dashboard.settings
# 데이터베이스 마이그레이션 및 정적 파일 수집
poetry run python manage.py migrate && 
poetry run python manage.py collectstatic --noinput &&

# Uvicorn 실행
poetry run uvicorn music_dashboard.asgi:application --host 0.0.0.0 --port 8000