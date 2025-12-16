
# SaaS Web Audit Platform (Fresh Build)

This is a **fresh, runnable** FastAPI + Celery + PostgreSQL project ready for **Railway**.
It includes:
- Web API (FastAPI)
- Background audits (Celery + Redis)
- PostgreSQL (Railway managed)
- Alembic migrations
- PDF report generation (ReportLab)
- Email templates (SendGrid SMTP-ready)
- Templates stored at `templates/Reports/` and `templates/Email/`

## Quick Deploy on Railway
1. Create services:
   - **Web** (Docker): uses `Dockerfile` at repo root
   - **Worker** (Docker): uses `worker.Dockerfile` at repo root
   - *(Optional)* **Beat** (Docker): uses `beat.Dockerfile` for scheduling
   - **PostgreSQL** (Managed)
   - **Redis** (Managed)

2. Set variables on Web & Worker services:
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

3. Run migrations (Web shell):
```
cd backend
alembic upgrade head
```

4. Test:
- Health: GET `/api/v1/healthz`
- Register: POST `/api/v1/auth/register` { email, password, organization_name }
- Login: POST `/api/v1/auth/login`
- Add website: POST `/api/v1/websites` { domain }
- Trigger audit: POST `/api/v1/audits/{website_id}/run`
- Latest metrics: GET `/api/v1/audits/{website_id}/latest`
- Reports list: GET `/api/v1/reports`

## Local Dev (optional)
```
cp .env.example .env
# Requires local Postgres & Redis configured in .env
```

## Notes
- The worker generates PDFs to `templates/Reports/audit_<RUN_ID>.pdf`.
- Email templates are in `templates/Email/`.
- This build focuses on minimal reliability; extend metrics in `app/audit/registry.py`.
