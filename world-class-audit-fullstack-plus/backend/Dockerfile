
# backend/Dockerfile
FROM python:3.11-bullseye

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends     build-essential     libpq-dev     chromium     nodejs     npm     curl     && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./backend/

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PORT=8000

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3     CMD curl -fsS http://localhost:${PORT}/health || exit 1

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
