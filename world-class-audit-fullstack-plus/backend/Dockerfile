
# backend/Dockerfile
FROM python:3.11-bullseye

# System dependencies (remove any you don't need to slim the image)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    chromium \
    nodejs \
    npm \
    curl \
    && rm -rf /var/lib/apt/lists/*

## Set working directory
WORKDIR /app

# Copy Python dependencies first (context is backend/, so this file must be backend/requirements.txt)
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source (again, context is backend/)
COPY . ./backend/

# Runtime env
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD curl -fsS http://localhost:${PORT}/health || exit 1

# Expose HTTP port
EXPOSE 8000

# Start the app
