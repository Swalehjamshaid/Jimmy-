
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.db.base import Base
class Website(Base):
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    domain = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
