"""PequeLectores Backend - Main Application Entry Point."""

import logging
import os
from contextlib import asynccontextmanager
from datetime import date

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from .config import get_settings
from .database import engine, AsyncSessionLocal, Base
from .models import Badge, Child
from .api.routes import preferences, recommendations, reading, gamification, auth
from .middleware.errors import setup_error_handlers

# Load settings FIRST
settings = get_settings()

# Configure structlog
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(
        logging.getLevelName(settings.log_level)
    ),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=False,
)

# Get logger
logger = structlog.get_logger()


def get_cors_origins() -> list[str]:
    """Get CORS origins from environment."""
    # Use settings if available, otherwise fallback to env var
    if settings.cors_origins:
        return settings.cors_origins
    origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173")
    return [origin.strip() for origin in origins.split(",")]


# Default badges to seed on startup
DEFAULT_BADGES = [
    {
        "name": "First Pages",
        "description": "Read your first 10 pages",
        "icon": "book-open",
        "requirement": 10
    },
    {
        "name": "Chapter One",
        "description": "Read 50 pages total",
        "icon": "book",
        "requirement": 50
    },
    {
        "name": "Bookworm",
        "description": "Read 100 pages total",
        "icon": "bookmark",
        "requirement": 100
    },
    {
        "name": "Avid Reader",
        "description": "Read 500 pages total",
        "icon": "graduation-cap",
        "requirement": 500
    },
    {
        "name": "Reading Champion",
        "description": "Read 1000 pages total",
        "icon": "trophy",
        "requirement": 1000
    },
    {
        "name": "Legendary Reader",
        "description": "Read 5000 pages total",
        "icon": "crown",
        "requirement": 5000
    },
    {
        "name": "First Book",
        "description": "Finish your first book",
        "icon": "star",
        "requirement": 50
    },
    {
        "name": "Explorer",
        "description": "Read books from 3 different subjects",
        "icon": "compass",
        "requirement": 3
    },
]


async def seed_badges():
    """Seed badges into the database if they don't exist."""
    async with AsyncSessionLocal() as session:
        # Check if badges already exist
        result = await session.execute(select(Badge).limit(1))
        existing = result.scalar_one_or_none()
        
        if existing:
            return  # Badges already seeded
        
        # Create badges
        for badge_data in DEFAULT_BADGES:
            badge = Badge(**badge_data)
            session.add(badge)
        
        await session.commit()


async def seed_demo_child():
    """Seed demo child for testing."""
    async with AsyncSessionLocal() as session:
        # Check if demo child exists
        result = await session.execute(
            select(Child).where(Child.id == 1)
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            return  # Already seeded
        
        # Create demo child
        demo_child = Child(
            id=1,
            name="Demo Reader",
            birth_date=date(2015, 1, 1),
            age=10
        )
        session.add(demo_child)
        
        await session.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown events."""
    # Startup: Create tables if they don't exist
    from .database import Base
    from .models import Badge, Child, ChildPreferences, ReadingLog, ChildBadge
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("database_tables_created")
    
    # Startup: seed badges and demo child
    await seed_badges()
    await seed_demo_child()
    
    yield
    
    # Shutdown: dispose database connections
    await engine.dispose()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="PequeLectores API",
        description="API for intelligent book recommendations for children",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Setup error handlers first
    setup_error_handlers(app)

    # Configure CORS middleware - allow all for development
    cors_origins = get_cors_origins()
    
    logger.info("cors_origins", origins=cors_origins)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all for now
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API routes with /api prefix
    app.include_router(auth.router, prefix="/api")  # Auth routes (no /api prefix in route itself)
    app.include_router(preferences.router, prefix="/api")
    app.include_router(recommendations.router, prefix="/api")
    app.include_router(reading.router, prefix="/api")
    app.include_router(gamification.router, prefix="/api")

    @app.get("/")
    async def root():
        return {"message": "Welcome to PequeLectores API", "status": "running"}

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    return app


app = create_app()