
from fastapi import APIRouter, Depends
from sqlalchemy import insert, select, update
from datetime import datetime
from app.core.deps import get_db_with_org, get_current_user
from app.db.models.audit_run import AuditRun
from app.db.models.audit_metric import AuditMetric
from app.db.models.website import Website

router = APIRouter()

@router.post('/{website_id}/run')
async def trigger_run(website_id: int, user=Depends(get_current_user), db=Depends(get_db_with_org)):
    website = (await db.execute(select(Website).where(Website.id==website_id))).scalar_one_or_none()
    if not website:
        return {"error": "Website not found"}
    run_id = (await db.execute(insert(AuditRun).values(website_id=website_id, score=0.0, status='completed', started_at=datetime.utcnow(), completed_at=datetime.utcnow()).returning(AuditRun.id))).scalar()
    # sample metrics
    await db.execute(insert(AuditMetric).values(audit_run_id=run_id, category='Technical', metric_name='HTTPS / SSL Validity', value='valid', score=95.0, recommendation='SSL OK'))
    await db.execute(insert(AuditMetric).values(audit_run_id=run_id, category='SEO', metric_name='Meta Title Optimization', value='Present', score=85.0, recommendation='Length optimal'))
    await db.execute(insert(AuditMetric).values(audit_run_id=run_id, category='Performance', metric_name='Bounce Rate', value='40%', score=70.0, recommendation='Improve relevance'))
    await db.execute(update(AuditRun).where(AuditRun.id==run_id).values(score=83.3))
    await db.commit()
    return {"audit_run_id": run_id, "status": "completed"}

@router.get('/{website_id}/latest')
async def latest(website_id: int, user=Depends(get_current_user), db=Depends(get_db_with_org)):
    run = (await db.execute(select(AuditRun).where(AuditRun.website_id==website_id).order_by(AuditRun.id.desc()))).scalar_one_or_none()
    if not run:
        return {"error": "No runs yet"}
    metrics = (await db.execute(select(AuditMetric).where(AuditMetric.audit_run_id==run.id))).scalars().all()
    return {"id": run.id, "website_id": website_id, "score": run.score, "status": run.status, "metrics": [{"id": m.id, "category": m.category, "metric_name": m.metric_name, "value": m.value, "score": m.score, "recommendation": m.recommendation} for m in metrics]}
