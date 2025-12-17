
# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, Any

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    organization_name: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class WebsiteCreate(BaseModel):
    domain: str

class AuditTrigger(BaseModel):
    website_id: str
    max_pages: int = 25
    timeout: int = 15

class MetricOut(BaseModel):
    category: str
    metric_name: str
    value: Any
    score: int
    recommendation: str
