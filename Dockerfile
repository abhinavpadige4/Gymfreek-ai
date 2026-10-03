# Gymfreek-ai on Render (or anywhere Docker runs).
# Render: New Web Service -> this repo -> Docker runtime. It injects $PORT;
# shell-form CMD expands it. Health check path: /health.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py auth.py geometry.py llm.py registry.py schemas.py ./
COPY routers/ ./routers/

EXPOSE 8000

# $PORT comes from the platform (Render sets it); default 8000 locally.
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
