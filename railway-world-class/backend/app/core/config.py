
import os
from pydantic import BaseModel
class Settings(BaseModel):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://localhost:5432/appdb")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-jwt-secret")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    ENV: str = os.getenv("ENV", "development")
settings = Settings()
