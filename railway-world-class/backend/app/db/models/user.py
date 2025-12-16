
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base
class User(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    role = Column(String, nullable=False, default="user")
    organization_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    created_at = Column(String, nullable=False)
