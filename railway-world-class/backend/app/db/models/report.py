
from sqlalchemy import Column, Integer, ForeignKey, String
from app.db.base import Base
class Report(Base):
    id = Column(Integer, primary_key=True)
    audit_run_id = Column(Integer, ForeignKey("auditrun.id"), nullable=False)
    type = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
