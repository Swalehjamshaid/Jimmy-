
# app/routers/orgs.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_db, require_role, get_current_user
from ..models import Organization

router = APIRouter(prefix="/orgs", tags=["orgs"])

@router.get("/me")
def my_org(db: Session = Depends(get_db), user=Depends(get_current_user)):
    org = db.query(Organization).filter(Organization.id == user.organization_id).first()
    return {"id": org.id, "name": org.name}
