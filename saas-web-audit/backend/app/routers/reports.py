
# app/routers/reports.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user
from ..models import AuditRun
from ..core.reporter import generate_pdf

router = APIRouter(prefix="/reports", tags=["reports"])

@router.post("/pdf")
def pdf(run_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    run = db.query(AuditRun).filter(AuditRun.id == run_id).first()
    if not run:
        return {"error": "run not found"}
    path = generate_pdf(run_id)
    return {"file": path}
