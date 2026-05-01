"""Seed initial data for Pequelectores."""

from datetime import datetime
from ..database import AsyncSessionLocal
from ..models import Child
from sqlalchemy import select


async def seed_demo_child():
    """Create a demo child for testing."""
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
            birth_date="2015-01-01",
            age=10
        )
        session.add(demo_child)
        
        await session.commit()
        print("✅ Demo child seeded successfully")


if __name__ == "__main__":
    import asyncio
    asyncio.run(seed_demo_child())