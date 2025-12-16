
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, text
from datetime import datetime, timedelta
from app.core.deps import get_db
from app.services.email import send_email
from app.db.models.user import User
from app.db.models.verification_token import VerificationToken

router = APIRouter()

@router.post('/send')
async def send_verification(email: str, db=Depends(get_db)):
    user = (await db.execute(select(User).where(User.email==email))).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    token = f"v-{user.id}-{int(datetime.utcnow().timestamp())}"
    expires = datetime.utcnow() + timedelta(hours=24)
    await db.execute(insert(VerificationToken).values(user_id=str(user.id), token=token, expires_at=expires))
    await db.commit()
    send_email(email, "Verify your email", f"<p>Your verification token: <b>{token}</b></p>")
    return {"status": "sent"}

@router.post('/confirm')
async def confirm(token: str, db=Depends(get_db)):
    vt = (await db.execute(select(VerificationToken).where(VerificationToken.token==token))).scalar_one_or_none()
    if not vt:
        raise HTTPException(status_code=404, detail='Invalid token')
    if vt.used:
        raise HTTPException(status_code=400, detail='Already used')
    await db.execute(update(User).where(User.id==vt.user_id).values(is_verified=True))
    await db.execute(update(VerificationToken).where(VerificationToken.id==vt.id).values(used=True))
    await db.execute(text("INSERT INTO useractivity (user_id, organization_id, action, details, timestamp) VALUES (:uid, (SELECT organization_id FROM "user" WHERE id=:uid), 'Email Verified', '', NOW())"), {"uid": str(vt.user_id)})
    await db.commit()
    return {"status": "verified"}
