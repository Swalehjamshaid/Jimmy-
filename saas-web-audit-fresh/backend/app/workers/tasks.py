
from app.workers.celery_app import celery_app
from sqlalchemy import create_engine, text, insert
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.models import audit_run as ar
from app.db.models import audit_metric as am
from app.db.models import website as w
from app.db.models import report as r
from app.services.pdf import generate_report_pdf

sync_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")
engine = create_engine(sync_url, pool_pre_ping=True)

@celery_app.task(bind=True, max_retries=3, default_retry_delay=30)
def run_audit(self, website_id: int, organization_id: int, audit_run_id: int):
    try:
        with Session(engine) as session:
            session.execute(text("SELECT set_config('app.current_organization_id', :org, false);"), {"org": str(organization_id)})
            # simple three metrics example
            session.execute(insert(am.AuditMetric).values(audit_run_id=audit_run_id, category='Technical', metric_name='HTTPS / SSL Validity', value='valid', score=95.0, recommendation='SSL OK'))
            session.execute(insert(am.AuditMetric).values(audit_run_id=audit_run_id, category='SEO', metric_name='Meta Title Optimization', value='Present', score=85.0, recommendation='Length optimal'))
            session.execute(insert(am.AuditMetric).values(audit_run_id=audit_run_id, category='Performance', metric_name='Bounce Rate', value='40%', score=70.0, recommendation='Improve relevance'))
            session.commit()
            sres = session.execute(text("SELECT AVG(score) FROM auditmetric WHERE audit_run_id=:rid"), {"rid": audit_run_id})
            avg = float(sres.scalar() or 0.0)
            session.execute(text("UPDATE auditrun SET score=:s, status='completed', completed_at=NOW() WHERE id=:rid"), {"s": avg, "rid": audit_run_id})
            # PDF
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
