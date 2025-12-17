
# app/security.py
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGO = "HS256"
ACCESS_TTL_MIN = 30
REFRESH_TTL_MIN = 1440

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_token(sub: str, scope: str = "access") -> str:
    ttl = ACCESS_TTL_MIN if scope == "access" else REFRESH_TTL_MIN
    payload = {"sub": sub, "scope": scope, "exp": datetime.utcnow() + timedelta(minutes=ttl)}
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGO)
