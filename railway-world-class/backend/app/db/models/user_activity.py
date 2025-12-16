
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from app.db.base import Base
class UserActivity(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    organization_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    action = Column(String, nullable=False)
    details = Column(String, nullable=True)
    timestamp = Column(DateTime, nullable=False)
