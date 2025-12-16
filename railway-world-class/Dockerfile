
# Use Python 3.11 base image
FROM python:3.11-bullseye

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    chromium \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python dependencies first for caching
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

## Copy application code
COPY backend/ ./backend/

# Optional: Install Node dependencies if needed
# COPY frontend/package.json ./frontend/
# RUN npm install --prefix ./frontend

# Default command (adjust as needed)
