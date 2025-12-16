
from fastapi import APIRouter, Depends
from sqlalchemy import insert, select
from datetime import datetime
from app.core.deps import get_db_with_org, get_current_user
from app.db.models.audit_run import AuditRun
from app.db.models.audit_metric import AuditMetric
from app.db.models.website import Website
from app.workers.tasks import run_audit

router = APIRouter()

@router.post('/{website_id}/run')
async def trigger_run(website_id: int, user=Depends(get_current_user), db=Depends(get_db_with_org)):
    website = (await db.execute(select(Website).where(Website.id==website_id))).scalar_one_or_none()
    if not website:
        return {"error": "Website not found"}
    run_id = (await db.execute(insert(AuditRun).values(website_id=website_id, score=0.0, status='queued', started_at=datetime.utcnow()).returning(AuditRun.id))).scalar()
    await db.commit()
    run_audit.delay(website_id=website_id, organization_id=user.get('org_id'), audit_run_id=run_id)
    return {"audit_run_id": run_id, "status": "queued"}

@router.get('/{website_id}/latest')
async def latest(website_id: int, user=Depends(get_current_user), db=Depends(get_db_with_org)):
    run = (await db.execute(select(AuditRun).where(AuditRun.website_id==website_id).order_by(AuditRun.id.desc()))).scalar_one_or_none()
    if not run:
        return {"error": "No runs yet"}
    metrics = (await db.execute(select(AuditMetric).where(AuditMetric.audit_run_id==run.id))).scalars().all()
    return {"id": run.id, "website_id": website_id, "score": run.score, "status": run.status, "metrics": [{"id": m.id, "category": m.category, "metric_name": m.metric_name, "value": m.value, "score": m.score, "recommendation": m.recommendation} for m in metrics]}
