
# World Class Web Audit — Full‑Stack PLUS (Railway‑ready)

An enhanced web + Python audit application with:
- Same‑domain crawl with configurable depth
- Security headers + HTTPS enforcement (HSTS, mixed content detection)
- SEO signals
- Accessibility basics
- Performance (TTFB + estimated page weight)
- Broken link detection
- Robots.txt + Sitemap discovery
- HTML UI, JSON API, and PDF export

## Deploy on Railway
1. Push to GitHub/GitLab.
2. In Railway, connect the repo. Railway reads `railway.toml` and builds using `backend/Dockerfile` with context `backend`.
3. Deploy. Visit `/` for the UI, `/health` for status.

## Local run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

## Docker run
```bash
docker build -f backend/Dockerfile backend -t web-audit-plus:latest
docker run -p 8000:8000 web-audit-plus:latest
```
