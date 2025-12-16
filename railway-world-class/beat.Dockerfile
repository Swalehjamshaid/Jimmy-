
FROM python:3.11-bullseye
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONPATH=/app/backend \
    CHROME_PATH=/usr/bin/chromium
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    chromium \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r ./backend/requirements.txt
RUN npm install -g lighthouse@11
COPY . .
WORKDIR /app/backend
CMD ["celery", "-A", "app.workers.celery_app.celery_app", "worker", "--loglevel=INFO", "-Q", "audits"]
