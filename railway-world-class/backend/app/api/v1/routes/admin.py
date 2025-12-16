
from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from app.core.deps import get_db_with_org, get_current_user
from app.core.rbac import require_role
from app.db.models.user import User
from app.db.models.subscription import Subscription
from app.db.models.audit_threshold import AuditThreshold
from app.db.models.user_activity import UserActivity
from sqlalchemy import text
from datetime import datetime

router = APIRouter()

@router.get('/users')
async def list_users(user=Depends(get_current_user), db=Depends(get_db_with_org)):
    require_role(user, ["admin", "super_admin"])
    res = await db.execute(select(User).where(User.organization_id==user.get('org_id')))
    users = res.scalars().all()
    return [{"id": str(u.id), "email": u.email, "role": u.role} for u in users]

@router.post('/subscription')
async def set_subscription(plan: str, user=Depends(get_current_user), db=Depends(get_db_with_org)):
    require_role(user, ["admin", "super_admin"])
    await db.execute(insert(Subscription).values(organization_id=user.get('org_id'), plan=plan))
    await db.execute(text("INSERT INTO useractivity (user_id, organization_id, action, details, timestamp) VALUES (:uid, :oid, 'Set Subscription', :det, NOW())"), {"uid": user.get('sub'), "oid": user.get('org_id'), "det": f"plan={plan}"})
    await db.commit()
    return {"status": "plan updated", "plan": plan}

@router.post('/thresholds')
async def set_threshold(category: str, min_score: float, user=Depends(get_current_user), db=Depends(get_db_with_org)):
    require_role(user, ["admin", "super_admin"])
    await db.execute(insert(AuditThreshold).values(organization_id=user.get('org_id'), category=category, min_score=min_score))
    await db.execute(text("INSERT INTO useractivity (user_id, organization_id, action, details, timestamp) VALUES (:uid, :oid, 'Set Threshold', :det, NOW())"), {"uid": user.get('sub'), "oid": user.get('org_id'), "det": f"{category}={min_score}"})
    await db.commit()
    return {"status": "saved"}

@router.get('/activity')
async def activity(user=Depends(get_current_user), db=Depends(get_db_with_org)):
    require_role(user, ["admin", "super_admin"])
    rows = await db.execute(text("SELECT user_id, action, details, timestamp FROM useractivity WHERE organization_id=:oid ORDER BY timestamp DESC LIMIT 200"), {"oid": user.get('org_id')})
    return [{"user_id": r[0], "action": r[1], "details": r[2], "timestamp": str(r[3])} for r in rows]
