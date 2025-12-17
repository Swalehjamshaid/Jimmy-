
# app/routers/sites.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user
from ..models import Website

router = APIRouter(prefix="/sites", tags=["sites"])

@router.post("/")
def add_site(domain: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    site = Website(domain=domain, organization_id=user.organization_id)
    db.add(site)
    db.commit()
    return {"id": site.id, "domain": site.domain}

@router.get("/")
def list_sites(db: Session = Depends(get_db), user=Depends(get_current_user)):
    rows = db.query(Website).filter(Website.organization_id == user.organization_id).all()
    return [{"id": s.id, "domain": s.domain, "is_active": s.is_active} for s in rows]
