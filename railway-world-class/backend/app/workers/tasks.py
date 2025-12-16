
from app.workers.celery_app import celery_app
from sqlalchemy import create_engine, text, insert
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.models import audit_run as ar
from app.db.models import audit_metric as am
from app.db.models import website as w
from app.db.models import report as r
from app.services.pdf import generate_report_pdf
from app.audit.registry import REGISTRY
import asyncio, subprocess, json, os

sync_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")
engine = create_engine(sync_url, pool_pre_ping=True)

# Locate Playwright-installed Chromium for Lighthouse
def find_chrome():
    base = '/root/.cache/ms-playwright'
    for d in os.listdir(base) if os.path.exists(base) else []:
        if 'chromium' in d:
            chrome_path = os.path.join(base, d, 'chrome-linux', 'chrome')
            if os.path.exists(chrome_path):
                return chrome_path
    return None

def run_lighthouse(url: str) -> dict:
    chrome = find_chrome()
    cmd = ["lighthouse", url, "--quiet", "--output=json", "--only-categories=performance"]
    if chrome:
        cmd.append(f"--chrome-path={chrome}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return {}
    try:
        return json.loads(res.stdout)
    except:
        return {}

@celery_app.task(bind=True, max_retries=3, default_retry_delay=30)
def run_audit(self, website_id: int, organization_id: int, audit_run_id: int):
    try:
        with Session(engine) as session:
            session.execute(text("SELECT set_config('app.current_organization_id', :org, false);"), {"org": str(organization_id)})
            # Fetch domain
            row = session.execute(text('SELECT domain FROM website WHERE id=:wid'), {'wid': website_id}).first()
            domain = row[0] if row else ''
            url = f"https://{domain}" if not domain.startswith('http') else domain
            # Run registry metrics
            for m in REGISTRY:
                fn = m['fn']
                if asyncio.iscoroutinefunction(fn):
                    res = asyncio.run(fn(domain))
                else:
                    res = fn(domain)
                session.execute(insert(am.AuditMetric).values(audit_run_id=audit_run_id, category=m['category'], metric_name=m['name'], value=str(res.get('value')), score=float(res.get('score', 0.0)), recommendation=res.get('recommendation')))
            session.commit()
            # Run Lighthouse
            lh = run_lighthouse(url)
            if lh:
                perf = lh.get('categories', {}).get('performance', {}).get('score', 0) * 100
                audits = lh.get('audits', {})
                for key, label in [
                    ('first-contentful-paint', 'Lighthouse FCP'),
                    ('largest-contentful-paint', 'Lighthouse LCP'),
                    ('cumulative-layout-shift', 'Lighthouse CLS'),
                    ('time-to-interactive', 'Time To Interactive'),
                    ('total-blocking-time', 'Total Blocking Time'),
                ]:
                    a = audits.get(key, {})
                    val = a.get('displayValue', a.get('numericValue'))
                    score = a.get('score', 0)
                    session.execute(insert(am.AuditMetric).values(audit_run_id=audit_run_id, category='Performance', metric_name=label, value=str(val), score=float(score or 0)*100, recommendation=''))
                # Overall Lighthouse Performance
                session.execute(insert(am.AuditMetric).values(audit_run_id=audit_run_id, category='Performance', metric_name='Lighthouse Performance Score', value=str(perf), score=float(perf), recommendation='Optimize performance'))
                session.commit()
            # Final score
            sres = session.execute(text("SELECT AVG(score) FROM auditmetric WHERE audit_run_id=:rid"), {"rid": audit_run_id})
            avg = float(sres.scalar() or 0.0)
            session.execute(text("UPDATE auditrun SET score=:s, status='completed', completed_at=NOW() WHERE id=:rid"), {"s": avg, "rid": audit_run_id})
            out_path = f"templates/Reports/audit_{audit_run_id}.pdf"
            generate_report_pdf(session, audit_run_id, out_path)
            session.execute(insert(r.Report).values(audit_run_id=audit_run_id, type='monthly', file_url=out_path))
            session.commit()
            return {"status": "completed", "score": avg}
    except Exception as e:
        raise self.retry(exc=e)

@celery_app.task
def schedule_weekly_audits():
    with Session(engine) as session:
        rows = session.execute(text("SELECT id, organization_id FROM website WHERE is_active=true")).all()
        for wid, org in rows:
            res = session.execute(text("INSERT INTO auditrun (website_id, score, status, started_at) VALUES (:wid, 0, 'queued', NOW()) RETURNING id"), {"wid": wid})
            run_id = res.scalar()
            session.commit()
            run_audit.delay(website_id=wid, organization_id=org, audit_run_id=run_id)
