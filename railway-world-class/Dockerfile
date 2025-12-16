
# railway-world-class/Dockerfile

# 1) Base image
FROM python:3.11-bullseye

# 2) System dependencies (no stray backticks; clean multiline RUN)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    chromium \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

## 3) Workdir
WORKDIR /app

# 4) Copy Python dependencies first for caching
#    This path must exist inside the build context (repo root)
COPY backend/requirements.txt ./requirements.txt

# 5) Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# 6) Copy application code
COPY backend/ ./backend/

# 7) (Optional) expose a port if your app serves HTTP
# EXPOSE 8000

# 8) Default command — adjust to your app’s entry point
#    e.g., uvicorn, flask, django, or a plain script
