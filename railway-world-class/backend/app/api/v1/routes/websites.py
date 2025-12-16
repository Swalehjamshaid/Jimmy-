
from fastapi import APIRouter, Depends
from sqlalchemy import insert, select
from app.core.deps import get_db_with_org, get_current_user
from app.db.models.website import Website

router = APIRouter()

@router.post('/')
async def create(domain: str, user=Depends(get_current_user), db=Depends(get_db_with_org)):
    wid = (await db.execute(insert(Website).values(domain=domain, organization_id=user.get('org_id'), is_active=True).returning(Website.id))).scalar()
    await db.commit()
    return {"id": wid, "domain": domain, "is_active": True}

@router.get('/')
async def list_websites(user=Depends(get_current_user), db=Depends(get_db_with_org)):
    res = await db.execute(select(Website).where(Website.organization_id==user.get('org_id')))
    items = res.scalars().all()
    return [{"id": w.id, "domain": w.domain, "is_active": w.is_active} for w in items]
