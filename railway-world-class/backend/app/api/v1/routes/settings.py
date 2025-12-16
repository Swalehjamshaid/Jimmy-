
from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, update
from app.core.deps import get_db_with_org, get_current_user
from app.core.rbac import require_role
from app.db.models.org_settings import OrgSettings

router = APIRouter()

@router.get('/')
async def get_settings(user=Depends(get_current_user), db=Depends(get_db_with_org)):
    res = await db.execute(select(OrgSettings).where(OrgSettings.organization_id==user.get('org_id')))
    s = res.scalar_one_or_none()
    return {"brand_name": s.brand_name if s else None, "brand_color": s.brand_color if s else None}

@router.post('/')
async def update_settings(brand_name: str | None=None, brand_color: str | None=None, user=Depends(get_current_user), db=Depends(get_db_with_org)):
    require_role(user, ["admin", "super_admin"])
    res = await db.execute(select(OrgSettings).where(OrgSettings.organization_id==user.get('org_id')))
    s = res.scalar_one_or_none()
    if s:
        await db.execute(update(OrgSettings).where(OrgSettings.id==s.id).values(brand_name=brand_name, brand_color=brand_color))
    else:
        await db.execute(insert(OrgSettings).values(organization_id=user.get('org_id'), brand_name=brand_name, brand_color=brand_color))
    await db.commit()
    return {"status": "updated"}
