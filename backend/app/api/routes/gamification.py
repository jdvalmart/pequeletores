"""Gamification API routes for badges and achievements."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from ..deps import get_session
from ...models import Child, Badge, ChildBadge, ReadingLog


router = APIRouter(prefix="/badges", tags=["gamification"])


class BadgeResponse(BaseModel):
    """Schema for badge response."""
    id: int
    name: str
    description: str
    icon: str
    earned_at: int | None = None

    model_config = {"from_attributes": True}


class BadgesResponse(BaseModel):
    """Schema for badges list response."""
    badges: list[BadgeResponse]
    total: int


class ChildBadgesResponse(BaseModel):
    """Schema for child's earned badges."""
    earned: list[BadgeResponse]
    unearned: list[BadgeResponse]
    total_earned: int


@router.get("", response_model=BadgesResponse)
async def get_all_badges(
    session: AsyncSession = Depends(get_session)
):
    """Get all available badges in the system."""
    result = await session.execute(
        select(Badge).order_by(Badge.requirement)
    )
    badges = result.scalars().all()
    
    badge_responses = [
        BadgeResponse(
            id=badge.id,
            name=badge.name,
            description=badge.description,
            icon=badge.icon
        )
        for badge in badges
    ]
    
    return BadgesResponse(badges=badge_responses, total=len(badge_responses))


@router.get("/{child_id}", response_model=ChildBadgesResponse)
async def get_child_badges(
    child_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Get badges earned by a specific child."""
    # Validate child exists
    result = await session.execute(
        select(Child).where(Child.id == child_id)
    )
    child = result.scalar_one_or_none()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Child with id {child_id} not found"
        )
    
    # Get all badges
    result = await session.execute(
        select(Badge).order_by(Badge.requirement)
    )
    all_badges = result.scalars().all()
    
    # Get child's earned badges
    result = await session.execute(
        select(ChildBadge).where(ChildBadge.child_id == child_id)
    )
    child_badges = result.scalars().all()
    earned_badge_ids = {cb.badge_id for cb in child_badges}
    
    earned = []
    unearned = []
    
    for badge in all_badges:
        badge_response = BadgeResponse(
            id=badge.id,
            name=badge.name,
            description=badge.description,
            icon=badge.icon
        )
        if badge.id in earned_badge_ids:
            # Find the earned_at timestamp
            for cb in child_badges:
                if cb.badge_id == badge.id:
                    badge_response.earned_at = cb.earned_at
                    break
            earned.append(badge_response)
        else:
            unearned.append(badge_response)
    
    return ChildBadgesResponse(
        earned=earned,
        unearned=unearned,
        total_earned=len(earned)
    )


@router.post("/{child_id}/check", status_code=status.HTTP_200_OK)
async def check_and_award_badges(
    child_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Check if child qualifies for any new badges and award them."""
    # Validate child exists
    result = await session.execute(
        select(Child).where(Child.id == child_id)
    )
    child = result.scalar_one_or_none()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Child with id {child_id} not found"
        )
    
    # Get child's reading stats
    result = await session.execute(
        select(
            func.count(ReadingLog.id).label("total_logs"),
            func.coalesce(func.sum(ReadingLog.pages_read), 0).label("total_pages"),
            func.count(func.distinct(ReadingLog.book_id)).label("unique_books")
        ).where(ReadingLog.child_id == child_id)
    )
    stats = result.one()
    
    total_pages = int(stats.total_pages or 0)
    unique_books = int(stats.unique_books or 0)
    
    # Get all badges
    result = await session.execute(select(Badge))
    badges = result.scalars().all()
    
    # Get already earned badges
    result = await session.execute(
        select(ChildBadge.badge_id).where(ChildBadge.child_id == child_id)
    )
    earned_ids = {row[0] for row in result.all()}
    
    # Check each badge
    new_badges = []
    now = datetime.utcnow()
    
    for badge in badges:
        if badge.id in earned_ids:
            continue
        
        # Check requirement (badge.requirement is the page count needed)
        if total_pages >= badge.requirement:
            child_badge = ChildBadge(
                child_id=child_id,
                badge_id=badge.id,
                earned_at=int(now.timestamp())
            )
            session.add(child_badge)
            new_badges.append(badge.name)
    
    if new_badges:
        await session.commit()
    
    return {
        "child_id": child_id,
        "new_badges_earned": new_badges,
        "total_pages": total_pages,
        "total_books": unique_books
    }