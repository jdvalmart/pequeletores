#!/usr/bin/env python3
"""Script to initialize the database and create all tables."""

import asyncio
from sqlalchemy import text
from app.database import engine, AsyncSessionLocal
from app.models import Parent, Child, ChildPreferences, ReadingLog, Badge, ChildBadge
from app.database import Base


async def init_db():
    """Create all tables in the database."""
    print("Creating database tables...")
    
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    print("Tables created successfully!")
    
    # Verify tables
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        tables = result.fetchall()
        print(f"\nTables in database: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")


if __name__ == "__main__":
    asyncio.run(init_db())