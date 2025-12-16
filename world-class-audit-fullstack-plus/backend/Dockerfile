# world-class-audit-fullstack-plus/backend/Dockerfile
FROM python:3.11-bullseye

# 1. Install system dependencies (needed for psycopg2-binary, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Copy requirements from the PROJECT ROOT (context = ".")
# The build context includes the project root, so we copy requirements.txt directly.
COPY requirements.txt ./requirements.txt

# 3. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the backend source code (app/service files)
# This copies the contents of the 'backend' directory into the container's WORKDIR (/app).
COPY backend/ .

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

EXPOSE 8000

# Healthcheck to ensure the service is running before routing traffic
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD curl -fsS http://localhost:${PORT}/health || exit 1
