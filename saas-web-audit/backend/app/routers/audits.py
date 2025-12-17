
# app/routers/audits.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user
from ..models import AuditRun, AuditMetric, Website
from ..workers.tasks import enqueue_audit

router = APIRouter(prefix="/audits", tags=["audits"])

@router.post("/run")
def run_audit(website_id: str, max_pages: int = 25, timeout: int = 15, db: Session = Depends(get_db), user=Depends(get_current_user)):
    # ensure website belongs to user's org
    site = db.query(Website).filter(Website.id == website_id, Website.organization_id == user.organization_id).first()
    if not site:
        return {"error": "site not found"}
    # create AuditRun row
    run = AuditRun(website_id=website_id, status='queued')
    db.add(run)
    db.commit()
    # enqueue background task
    enqueue_audit(run.id, site.domain, max_pages, timeout, user.organization_id)
    return {"audit_run_id": run.id, "status": "queued"}

@router.get("/")
def list_audits(db: Session = Depends(get_db), user=Depends(get_current_user)):
    # join by website/org
    runs = db.query(AuditRun).join(Website, Website.id == AuditRun.website_id).filter(Website.organization_id == user.organization_id).order_by(AuditRun.started_at.desc()).all()
    return [{"id": r.id, "website_id": r.website_id, "status": r.status, "score": r.score, "started_at": r.started_at, "completed_at": r.completed_at} for r in runs]

@router.get("/{run_id}")
def get_audit(run_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    metrics = db.query(AuditMetric).filter(AuditMetric.audit_run_id == run_id).all()
    return [{"category": m.category, "metric_name": m.metric_name, "value": m.value, "score": m.score, "recommendation": m.recommendation} for m in metrics]
