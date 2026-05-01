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
# Railway provides postgresql:// but we need postgresql+asyncpg:// for async driver
raw_url = getenv(
    "DATABASE_URL",
    None  # No default - fail early if not set
)

if not raw_url:
    raise RuntimeError(
        "DATABASE_URL environment variable is not set. "
        "Please ensure PostgreSQL is linked to your Railway service."
    )

# Convert to asyncpg format if needed
if raw_url.startswith("postgresql://"):
    DATABASE_URL = raw_url.replace("postgresql://", "postgresql+asyncpg://", 1)
else:
    DATABASE_URL = raw_url

# Debug: print truncated URL (hide password)
if "://" in DATABASE_URL:
    parts = DATABASE_URL.split("://")
    if "@" in parts[1]:
        user_pass = parts[1].split("@")[0]
        if ":" in user_pass:
            safe_url = f"{parts[0]}://****:****@{parts[1].split('@')[1]}"
        else:
            safe_url = DATABASE_URL
    else:
        safe_url = DATABASE_URL
else:
    safe_url = DATABASE_URL

print(f"Connecting to database: {safe_url}")

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