
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import text
from app.core.security import decode_token
from app.db.session import async_session_factory

http_bearer = HTTPBearer(auto_error=False)

async def get_db():
    async with async_session_factory() as session:
        yield session

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    try:
        return decode_token(credentials.credentials)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

async def get_db_with_org(user=Depends(get_current_user)):
    async with async_session_factory() as session:
        await session.execute(text("SELECT set_config('app.current_organization_id', :org, false);"), {"org": str(user.get('org_id'))})
        yield session
