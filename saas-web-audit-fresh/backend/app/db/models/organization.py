
from sqlalchemy import Column, Integer, String
from app.db.base import Base
class Organization(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    subscription_plan = Column(String, nullable=False, default="Free")
