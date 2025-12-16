
# backend/Dockerfile

# 1) Base image: Python 3.11 (Debian Bullseye)
FROM python:3.11-bullseye

# 2) Install system dependencies (remove any you don't need to slim the image)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    chromium \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# 3) Set working directory inside the container
WORKDIR /app

# 4) Copy Python dependencies first (leverages Docker layer cache)
COPY requirements.txt ./requirements.txt

# 5) Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6) Copy the backend source code (context is 'backend/')
COPY . ./backend/

# # 7) Environment variables for Python runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 8) Expose the HTTP port (adjust if your app uses a different port)
EXPOSE 8000

# 9) Start command — choose ONE that matches your app
# --- Plain Python script (e.g., backend/main.py):
CMD ["python", "backend/main.py"]

# --- If using FastAPI with uvicorn (uncomment and adjust app path):
# CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]

# --- If using Flask (uncomment and set FLASK_APP properly):
# ENV FLASK_APP=backend/app.py
# CMD ["flask", "run", "--host=0.0.0.0", "--port", "8000"]

# --- If using Django (ensure manage.py is inside backend/):
