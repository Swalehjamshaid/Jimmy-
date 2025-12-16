
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean
from app.db.base import Base
class VerificationToken(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("user.id"), nullable=False)
    token = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)
