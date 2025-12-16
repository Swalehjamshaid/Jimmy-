
FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONPATH=/app/backend
# System deps + Node + Lighthouse + Chromium via Playwright
RUN apt-get update && apt-get install -y --no-install-recommends curl gnupg build-essential libpq-dev &&     curl -fsSL https://deb.nodesource.com/setup_20.x | bash - &&     apt-get install -y nodejs &&     npm install -g lighthouse &&     rm -rf /var/lib/apt/lists/*
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r ./backend/requirements.txt &&     python -m playwright install --with-deps chromium
COPY . .
WORKDIR /app/backend
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
