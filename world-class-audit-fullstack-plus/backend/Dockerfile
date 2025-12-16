
# backend/Dockerfile
FROM python:3.11-bullseye

# System dependencies (remove anything you don't need to slim the image)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    chromium \
    nodejs \
    npm \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Working directory for the app
WORKDIR /app

# Copy Python dependencies first (context is backend/)
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend source (again, context is backend/, so '.' is that folder)
COPY . ./backend/

# Environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Healthcheck hitting /health
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD curl -fsS http://localhost:${PORT}/health || exit 1

# Expose service port
EXPOSE 8000

# Start the app
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", " --port", "8000"]
