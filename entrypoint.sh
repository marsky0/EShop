#!/bin/bash

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting Uvicorn and Celery..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
exec celery -A app.tasks worker --loglevel=info
