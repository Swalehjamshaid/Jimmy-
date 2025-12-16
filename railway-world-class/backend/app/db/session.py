
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
async_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(async_url, pool_pre_ping=True)
async_session_factory = sessionmaker(engine, class_=AsyncSession, autocommit=False, autoflush=False, expire_on_commit=False)
