
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import insert, select, text
from datetime import datetime
from app.core.deps import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.db.models.organization import Organization
from app.db.models.user import User

router = APIRouter()

@router.post('/register', response_model=TokenResponse)
async def register(payload: RegisterRequest, db=Depends(get_db)):
    org_id = (await db.execute(insert(Organization).values(name=payload.organization_name, subscription_plan='Free').returning(Organization.id))).scalar()
    await db.execute(text("SELECT set_config('app.current_organization_id', :org, false)").bindparams(org=str(org_id)))
    now = datetime.utcnow().isoformat()
    try:
        uid = (await db.execute(insert(User).values(email=payload.email, password_hash=hash_password(payload.password), is_verified=False, role='admin', organization_id=org_id, created_at=now).returning(User.id))).scalar()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists')
    await db.commit()
    token = create_access_token(sub=str(uid), org_id=org_id, role='admin')
    return TokenResponse(access_token=token)

@router.post('/login', response_model=TokenResponse)
async def login(payload: LoginRequest, db=Depends(get_db)):
    user = (await db.execute(select(User).where(User.email==payload.email))).scalar_one_or_none()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    token = create_access_token(sub=str(user.id), org_id=user.organization_id, role=user.role)
    return TokenResponse(access_token=token)
