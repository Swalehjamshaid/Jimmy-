
# app/core/report.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from datetime import datetime

def save_pdf(path: str, data: dict):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    y = height - 2*cm
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2*cm, y, "Web Audit Report")
    y -= 0.8*cm
    c.setFont("Helvetica", 10)
    c.drawString(2*cm, y, f"Generated: {datetime.utcnow().isoformat()}Z")
    y -= 1.2*cm

    # Summary
    summ = data.get('summary', {})
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2*cm, y, "Summary")
    y -= 0.8*cm
    c.setFont("Helvetica", 10)
    for k in ["total_pages", "ok_responses"]:
        c.drawString(2*cm, y, f"{k}: {summ.get(k)}")
        y -= 0.6*cm
    robots = summ.get('robots', {})
    c.drawString(2*cm, y, f"robots.txt: {'present' if robots.get('present') else 'missing'}")
    y -= 0.6*cm
    c.save()
