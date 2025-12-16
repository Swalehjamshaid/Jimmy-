
from sqlalchemy import Column, Integer, ForeignKey, String, Float, Text
from app.db.base import Base
class AuditMetric(Base):
    id = Column(Integer, primary_key=True)
    audit_run_id = Column(Integer, ForeignKey("auditrun.id"), nullable=False)
    category = Column(String, nullable=False)
    metric_name = Column(String, nullable=False)
    value = Column(String)
    score = Column(Float, default=0.0)
    recommendation = Column(Text)
