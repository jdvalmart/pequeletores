"""Preferences API routes."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..deps import get_session
from ...models import Child, ChildPreferences


router = APIRouter(prefix="/preferences", tags=["preferences"])

# Valid icon IDs (from frontend icons.ts)
VALID_ICON_IDS = {
    'dinosaur', 'dragon', 'dog', 'cat', 'horse', 'butterfly',
    'rocket', 'compass', 'mountain', 'ship', 'treasure', 'map',
    'wizard', 'fairy', 'ghost', 'magic', 'castle', 'crown',
    'science', 'earth', 'star', 'robot', 'brain', 'lightbulb',
    'soccer', 'basketball', 'swimming', 'bicycle', 'trophy', 'medal',
    'laugh', 'art', 'music', 'game', 'camera', 'heart'
}


class PreferencesCreate(BaseModel):
    """Schema for creating/updating preferences."""
    child_id: int = Field(..., gt=0, description="ID of the child")
    icon_ids: list[str] = Field(
        ..., 
        min_length=1, 
        max_length=10,
        description="List of icon IDs representing preferences"
    )
    
    @field_validator('icon_ids')
    @classmethod
    def validate_icon_ids(cls, v: list[str]) -> list[str]:
        """Validate that all icon IDs are valid."""
        invalid = set(v) - VALID_ICON_IDS
        if invalid:
            raise ValueError(f"Invalid icon IDs: {invalid}. Valid icons: {VALID_ICON_IDS}")
        return v


class PreferencesResponse(BaseModel):
    """Schema for preferences response."""
    id: int
    child_id: int
    icon_ids: list[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


@router.post("", response_model=PreferencesResponse, status_code=status.HTTP_200_OK)
async def save_preferences(
    preferences: PreferencesCreate,
    session: AsyncSession = Depends(get_session)
):
    """Save or update child preferences.
    
    Creates new preferences if child_id doesn't exist,
    or updates existing preferences if they do.
    """
    # Check if child exists
    result = await session.execute(
        select(Child).where(Child.id == preferences.child_id)
    )
    child = result.scalar_one_or_none()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Child with id {preferences.child_id} not found"
        )
    
    # Check if preferences exist
    result = await session.execute(
        select(ChildPreferences).where(
            ChildPreferences.child_id == preferences.child_id
        )
    )
    existing_prefs = result.scalar_one_or_none()
    
    now = datetime.utcnow()
    
    if existing_prefs:
        # Update existing
        existing_prefs.icon_ids = preferences.icon_ids
        existing_prefs.updated_at = now
        await session.commit()
        await session.refresh(existing_prefs)
        return existing_prefs
    
    # Create new preferences
    new_prefs = ChildPreferences(
        child_id=preferences.child_id,
        icon_ids=preferences.icon_ids,
        created_at=now,
        updated_at=now
    )
    session.add(new_prefs)
    await session.commit()
    await session.refresh(new_prefs)
    return new_prefs


@router.get("/{child_id}", response_model=PreferencesResponse)
async def get_preferences(
    child_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Get preferences for a specific child."""
    result = await session.execute(
        select(ChildPreferences).where(
            ChildPreferences.child_id == child_id
        )
    )
    preferences = result.scalar_one_or_none()
    
    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Preferences for child {child_id} not found"
        )
    
    return preferences