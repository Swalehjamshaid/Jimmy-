
FROM python:3.11-bullseye
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONPATH=/app/backend \
    CHROME_PATH=/usr/bin/chromium
# Install system dependencies, Chromium, Node.js, and Lighthouse
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    chromium \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*
# Install Python dependencies
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r ./backend/requirements.txt
# Install Lighthouse globally
RUN npm install -g lighthouse@11
# Copy project files
COPY . .
WORKDIR /app/backend
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host
