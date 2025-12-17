
# app/models.py
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.types import JSON
from datetime import datetime
import uuid

Base = declarative_base()

class Organization(Base):
    __tablename__ = 'organizations'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    subscription_plan = Column(String, default='Free')

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    role = Column(String, default='User')
    organization_id = Column(String, ForeignKey('organizations.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

class Website(Base):
    __tablename__ = 'websites'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String, ForeignKey('organizations.id'))
    domain = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

class AuditRun(Base):
    __tablename__ = 'audit_runs'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    website_id = Column(String, ForeignKey('websites.id'))
    score = Column(Integer, default=0)
    status = Column(String, default='pending')
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

class AuditMetric(Base):
    __tablename__ = 'audit_metrics'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    audit_run_id = Column(String, ForeignKey('audit_runs.id'))
    category = Column(String)
    metric_name = Column(String)
    value = Column(JSON)
    score = Column(Integer)
    recommendation = Column(Text)

class Report(Base):
    __tablename__ = 'reports'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    audit_run_id = Column(String, ForeignKey('audit_runs.id'))
    type = Column(String)  # weekly/monthly
    file_url = Column(String)
