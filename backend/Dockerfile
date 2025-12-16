
# backend/Dockerfile

# 1) Base image: Python 3.11 on Debian Bullseye
FROM python:3.11-bullseye

# 2) System dependencies (adjust if you don't need some)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    chromium \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# 3) Create and set working directory inside the image
WORKDIR /app

# 4) Copy Python dependencies first (for better caching)
#    Since the build context is "backend/", this path is local to that folder.
COPY requirements.txt ./requirements.txt

# 5) Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6) Copy the rest of the backend source code into the image
#    Copies everything from the backend/ directory (build context) to /app/backend
COPY . ./COPY . ./backend/

# 7) Environment settings (example; adjust as needed)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 8) Expose a port if your app serves HTTP (example: 8000)
# EXPOSE 8000

# 9) Default command: **adjust this to your app’s entry point**
# Example for a plain Python script:
# CMD ["python", "backend/main.py"]

# Example for FastAPI with uvicorn:
# CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]

# Example for Flask:
# ENV FLASK_APP=backend/app.py
# CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]

# Example for Django:
# (Ensure manage.py is in backend/ if you intend to copy/run it)
