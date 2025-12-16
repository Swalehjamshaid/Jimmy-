
from sqlalchemy import Column, Integer, ForeignKey, Float, String, DateTime
from app.db.base import Base
class AuditRun(Base):
    id = Column(Integer, primary_key=True)
    website_id = Column(Integer, ForeignKey("website.id"), nullable=False)
    score = Column(Float, default=0.0)
    status = Column(String, default="pending")
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
