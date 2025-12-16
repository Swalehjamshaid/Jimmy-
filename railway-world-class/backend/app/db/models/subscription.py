
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from app.db.base import Base
class Subscription(Base):
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    plan = Column(String, nullable=False)
    stripe_customer_id = Column(String)
    stripe_subscription_id = Column(String)
    valid_until = Column(DateTime)
