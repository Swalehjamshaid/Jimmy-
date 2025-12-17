
# worker/Dockerfile
FROM python:3.11-bullseye

RUN apt-get update && apt-get install -y --no-install-recommends     build-essential     libpq-dev     curl     && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install deps (reuse backend/requirements.txt)
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code for tasks
COPY backend/ ./backend/
COPY worker/ ./worker/

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1

CMD ["celery", "-A", "worker.celery_app.celery_app", "worker", "--loglevel=INFO"]
