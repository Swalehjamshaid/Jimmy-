
# app/workers/tasks.py
import os
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import AuditRun, AuditMetric
from .metrics.catalog import ALL_METRICS

# Enqueue via Redis/Celery by calling worker service HTTP or Celery broker
# Here we assume Celery worker is set with REDIS_URL and registered task name 'worker.tasks.run_audit_task'
from celery import Celery

broker_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
cel = Celery('web_audit_api', broker=broker_url, backend=broker_url)

def enqueue_audit(run_id: str, domain: str, max_pages: int, timeout: int, organization_id: str):
    cel.send_task('worker.tasks.run_audit_task', args=[run_id, domain, max_pages, timeout, organization_id])

# Actual audit implementation used by worker
def run_audit_task(run_id: str, domain: str, max_pages: int, timeout: int, organization_id: str):
    db: Session = SessionLocal()
    try:
        run = db.query(AuditRun).filter(AuditRun.id == run_id).first()
        if not run:
            return {'error': 'run not found'}
        run.status = 'running'
        db.commit()

        total_score = 0
        metrics_count = 0
        for metric in ALL_METRICS:
            result = metric.check(domain, max_pages=max_pages, timeout=timeout)
            row = AuditMetric(audit_run_id=run_id,
                              category=metric.category,
                              metric_name=metric.name,
                              value=result['value'],
                              score=result['score'],
                              recommendation=result.get('recommendation',''))
            db.add(row)
            total_score += result['score']
            metrics_count += 1
        run.status = 'completed'
        run.score = int(total_score / max(metrics_count,1))
        db.commit()
        return {'ok': True, 'score': run.score}
    finally:
        db.close()
