
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "SaaS Web Audit"
    env: str = "development"
    log_level: str = "info"
    secret_key: str = "change_me"
    jwt_secret: str = "change_me"
    database_url: str = "sqlite:///backend/app/audit.db"
    redis_url: str | None = None
    email_api_key: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
