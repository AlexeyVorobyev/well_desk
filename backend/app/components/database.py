from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.settings import get_settings


class Base(DeclarativeBase):
    """Base class for declarative models."""


settings = get_settings()
engine = create_async_engine(settings.database_url_async, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncIterator[AsyncSession]:
    """Yield an async SQLAlchemy session for dependency injection."""

    async with SessionLocal() as session:
        yield session
