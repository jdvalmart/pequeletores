# PequeLectores Backend — Dockerfile for Railway
FROM python:3.14-slim

WORKDIR /app

# Install dependencies (cached layer)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (excludes .venv, .env, tests via .dockerignore)
COPY backend/ .

# Expose port
EXPOSE 8000

# Startup — Railway proporciona $PORT automáticamente
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}