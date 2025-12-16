
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models.audit_run import AuditRun
from app.db.models.audit_metric import AuditMetric
from app.db.models.website import Website
import os

def generate_report_pdf(session: Session, audit_run_id: int, out_path: str):
    run = session.execute(select(AuditRun).where(AuditRun.id==audit_run_id)).scalar_one()
    website = session.execute(select(Website).where(Website.id==run.website_id)).scalar_one()
    metrics = session.execute(select(AuditMetric).where(AuditMetric.audit_run_id==audit_run_id)).scalars().all()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    c = canvas.Canvas(out_path, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2*cm, height-2*cm, "Website Audit Report")
    c.setFont("Helvetica", 12)
    c.drawString(2*cm, height-3*cm, f"Domain: {website.domain}")
    c.drawString(2*cm, height-3.7*cm, f"Run ID: {audit_run_id} | Score: {run.score:.2f}")
    y = height - 5*cm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2*cm, y, "Metrics")
    y -= 0.7*cm
    c.setFont("Helvetica", 10)
    for m in metrics:
        line = f"[{m.category}] {m.metric_name}: value={m.value}, score={m.score:.1f}"
        c.drawString(2*cm, y, line[:120])
        y -= 0.5*cm
        if y < 2*cm:
            c.showPage()
            y = height - 2*cm
    c.showPage()
    c.save()
