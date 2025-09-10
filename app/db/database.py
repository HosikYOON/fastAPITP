from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.settings import settings

async_engine = create_async_engine(settings.async_db_url, echo=False)

AsyncSessionLocal = sessionmaker(
    autoflush=False, autocommit=False, bind=async_engine, class_=AsyncSession
)

sync_engine = create_engine(settings.sync_db_url, pool_pre_ping=True)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
