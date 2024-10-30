#!/bin/bash

export DJANGO_SETTINGS_MODULE=music_dashboard.settings.local
poetry shell
uvicorn music_dashboard.asgi:application --host 0.0.0.0 --port 8000