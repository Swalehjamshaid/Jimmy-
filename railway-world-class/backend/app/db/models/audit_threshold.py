
from sqlalchemy import Column, Integer, ForeignKey, String, Float
from app.db.base import Base
class AuditThreshold(Base):
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    category = Column(String, nullable=False)
    min_score = Column(Float, nullable=False, default=70.0)
