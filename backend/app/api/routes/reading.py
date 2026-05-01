"""Reading activity API routes."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from ..deps import get_session
from ...models import Child, ReadingLog


router = APIRouter(prefix="/reading", tags=["reading"])


class ReadingLogCreate(BaseModel):
    """Schema for creating a reading log entry."""
    child_id: int
    book_id: str
    pages_read: int


class ReadingLogResponse(BaseModel):
    """Schema for reading log response."""
    id: int
    child_id: int
    book_id: str
    pages_read: int
    logged_at: datetime

    model_config = {"from_attributes": True}


class ReadingStreakResponse(BaseModel):
    """Schema for streak response."""
    current_streak: int
    longest_streak: int
    total_pages: int
    total_books: int


@router.post("/log", response_model=ReadingLogResponse, status_code=status.HTTP_201_CREATED)
async def log_reading(
    log_data: ReadingLogCreate,
    session: AsyncSession = Depends(get_session)
):
    """Log reading activity for a child."""
    # Validate child exists
    result = await session.execute(
        select(Child).where(Child.id == log_data.child_id)
    )
    child = result.scalar_one_or_none()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Child with id {log_data.child_id} not found"
        )
    
    if log_data.pages_read <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="pages_read must be positive"
        )
    
    # Create reading log
    new_log = ReadingLog(
        child_id=log_data.child_id,
        book_id=log_data.book_id,
        pages_read=log_data.pages_read,
        logged_at=datetime.utcnow()
    )
    session.add(new_log)
    await session.commit()
    await session.refresh(new_log)
    
    return new_log


@router.get("/streak/{child_id}", response_model=ReadingStreakResponse)
async def get_streak(
    child_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Get current reading streak for a child."""
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
    
    # Get all reading logs for child, ordered by date
    result = await session.execute(
        select(ReadingLog).where(
            ReadingLog.child_id == child_id
        ).order_by(ReadingLog.logged_at.desc())
    )
    logs = result.scalars().all()
    
    if not logs:
        return ReadingStreakResponse(
            current_streak=0,
            longest_streak=0,
            total_pages=0,
            total_books=0
        )
    
    # Calculate totals
    total_pages = sum(log.pages_read for log in logs)
    unique_books = set(log.book_id for log in logs)
    total_books = len(unique_books)
    
    # Calculate streaks
    current_streak, longest_streak = _calculate_streaks(logs)
    
    return ReadingStreakResponse(
        current_streak=current_streak,
        longest_streak=longest_streak,
        total_pages=total_pages,
        total_books=total_books
    )


def _calculate_streaks(logs: list[ReadingLog]) -> tuple[int, int]:
    """Calculate current and longest reading streaks.
    
    A streak is consecutive days with reading activity.
    """
    if not logs:
        return 0, 0
    
    # Group logs by date (ignore time)
    dates_with_reading = set()
    for log in logs:
        date = log.logged_at.date()
        dates_with_reading.add(date)
    
    # Sort dates
    sorted_dates = sorted(dates_with_reading, reverse=True)
    
    # Calculate current streak (consecutive days from today/yesterday)
    today = datetime.now(timezone.utc).date()
    current_streak = 0
    
    check_date = today
    if today in dates_with_reading:
        current_streak = 1
        check_date = today
        while True:
            from datetime import timedelta
            check_date = check_date - timedelta(days=1)
            if check_date in dates_with_reading:
                current_streak += 1
            else:
                break
    elif sorted_dates:
        yesterday = today - timedelta(days=1)
        if yesterday in dates_with_reading:
            current_streak = 1
            check_date = yesterday
            while True:
                check_date = check_date - timedelta(days=1)
                if check_date in dates_with_reading:
                    current_streak += 1
                else:
                    break
    
    # Calculate longest streak
    longest_streak = 0
    if sorted_dates:
        current = 1
        prev_date = sorted_dates[0]
        for date in sorted_dates[1:]:
            from datetime import timedelta
            diff = (prev_date - date).days
            if diff == 1:
                current += 1
            else:
                longest_streak = max(longest_streak, current)
                current = 1
            prev_date = date
        longest_streak = max(longest_streak, current)
    
    return current_streak, longest_streak