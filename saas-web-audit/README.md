
# SaaS Web Audit Platform (FastAPI + Celery) — Railway Ready

This repository contains:
- **API service** (FastAPI) for auth, orgs, websites, audit runs, metrics, reports
- **Celery worker** (Redis broker) to run audits asynchronously
- **PostgreSQL** (Railway Managed) integration via `DATABASE_URL`
- **JWT auth** + roles (SuperAdmin/Admin/User/Viewer)
- **50 metrics** scaffold across technical/SEO/content/UX/perf/security/compliance
- **railway.toml** for API (backend context) and **railway-worker.toml** for the worker

## Services on Railway
Create **two services** from this repo:
1. **API**
   - Dockerfile Path: `backend/Dockerfile`
   - Root Directory / Build Context: `backend`
   - Variables: `DATABASE_URL`, `SECRET_KEY`, `JWT_SECRET`, `REDIS_URL`, `EMAIL_API_KEY`, `APP_NAME`, `ENV`
2. **Worker**
   - Dockerfile Path: `worker/Dockerfile`
   - Root Directory / Build Context: `/` (repo root)
   - Variables: `DATABASE_URL`, `REDIS_URL`

## Local quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
# In another terminal (requires Redis running):
celery -A worker.celery_app.celery_app worker --loglevel=INFO
```

Open http://localhost:8000/docs to explore APIs.
