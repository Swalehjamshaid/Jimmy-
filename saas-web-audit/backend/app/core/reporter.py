
# app/core/reporter.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from sqlalchemy.orm import Session
from .config import settings
from .db import SessionLocal
from .models import AuditRun, AuditMetric

def generate_pdf(run_id: str) -> str:
    db: Session = SessionLocal()
    try:
        run = db.query(AuditRun).filter(AuditRun.id == run_id).first()
        metrics = db.query(AuditMetric).filter(AuditMetric.audit_run_id == run_id).all()
        path = f"backend/app/reports/{run_id}.pdf"
        import os
        os.makedirs("backend/app/reports", exist_ok=True)
        c = canvas.Canvas(path, pagesize=A4)
        width, height = A4
        y = height - 2*cm
        c.setFont("Helvetica-Bold", 14)
        c.drawString(2*cm, y, f"Audit Report: {run_id}")
        y -= 0.8*cm
        c.setFont("Helvetica", 10)
        for m in metrics[:40]:
            c.drawString(2*cm, y, f"{m.category} / {m.metric_name}: score={m.score}")
            y -= 0.5*cm
            if y < 2*cm:
                c.showPage(); y = height - 2*cm
        c.save()
        return path
    finally:
        db.close()
