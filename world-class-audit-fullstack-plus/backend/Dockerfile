# world-class-audit-fullstack-plus/backend/Dockerfile
FROM python:3.11-bullseye

# 1. Install system dependencies (needed for libpq-dev, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Copy requirements from the PROJECT ROOT (context = ".")
COPY requirements.txt ./requirements.txt

# 3. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 4. CRITICAL FIX: Copy the source code directory (app/) into the container (./app)
COPY app/ ./app 

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD curl -fsS http://localhost:${PORT}/health || exit 1
