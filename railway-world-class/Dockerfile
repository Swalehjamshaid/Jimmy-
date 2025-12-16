
FROM python:3.11-bullseye

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev chromium nodejs npm \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy deps first for caching
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY backend/ ./backend/
# CMD ["python", "backend/main.py"]
``
