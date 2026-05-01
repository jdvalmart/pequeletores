"""Database configuration and session management."""

from collections.abc import AsyncGenerator
from os import getenv
from dotenv import load_dotenv

# Load .env first
load_dotenv()

from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import AsyncAdaptedQueuePool


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


# Database URL from environment
DATABASE_URL = getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://pequena_users:pequena_secret@localhost:5433/pequena_lectores"
)

# Create async engine with connection pool
engine = create_async_engine(
    DATABASE_URL,
    echo=getenv("SQL_ECHO", "false").lower() == "true",
    poolclass=AsyncAdaptedQueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async database sessions.
    
    Usage:
        @app.get("/items")
        async def get_items(session: AsyncSession = Depends(get_session)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Alternative dependency name for database sessions."""
    async for session in get_session():
        yield session