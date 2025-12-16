
from sqlalchemy import Column, Integer, ForeignKey, String
from app.db.base import Base
class OrgSettings(Base):
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    brand_name = Column(String)
    brand_color = Column(String)
