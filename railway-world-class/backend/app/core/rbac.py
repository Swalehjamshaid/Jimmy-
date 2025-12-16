
from fastapi import HTTPException, status

def require_role(user_payload: dict, allowed: list[str]):
    role = user_payload.get("role")
    if role not in allowed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
