
import bcrypt, jwt, datetime
from app.core.config import settings
ALGO = "HS256"

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def create_access_token(sub: str, org_id: int, role: str, minutes=30):
    payload = {"sub": sub, "org_id": org_id, "role": role, "exp": datetime.datetime.utcnow()+datetime.timedelta(minutes=minutes)}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=ALGO)

def decode_token(token: str):
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGO])
