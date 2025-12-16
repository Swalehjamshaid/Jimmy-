
# World-Class Web Audit SaaS (Railway-Ready)

A **world-class** audit platform: FastAPI + Celery + PostgreSQL + Redis + Lighthouse + Real-time dashboards + Admin + Activity logs.

## Services on Railway
- **Web (Docker)** → `Dockerfile`
- **Worker (Docker)** → `worker.Dockerfile`
- **Beat (Docker)** → `beat.Dockerfile` (optional weekly scheduling)
- **PostgreSQL** (Railway managed)
- **Redis** (Railway managed)

## Environment Variables (Web & Worker)
```
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DBNAME?sslmode=require
SECRET_KEY=your-fastapi-secret
JWT_SECRET=your-jwt-secret
REDIS_URL=redis://:PASSWORD@HOST:PORT/0
EMAIL_API_KEY=your-sendgrid-api-key
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
ENV=production
```

## Migrations
```
cd backend
alembic upgrade head   # applies 0001, 0002 (RLS), 0003 (advanced tables), 0004_activity
```

## Quick Test
- Health: `GET /api/v1/healthz`
- Register → Login → Create Website → Trigger audit: `POST /api/v1/audits/{website_id}/run`
- Watch **real-time dashboard** (frontend): shows metrics streaming in.
- Reports: `GET /api/v1/reports` → PDFs in `templates/Reports/`.

## Notes
- Dockerfiles install **Node.js** and **Lighthouse** globally, and **Playwright Chromium**. The worker runs Lighthouse and merges metrics with registry.
- RLS is enabled; API and worker set org context per request/run.
