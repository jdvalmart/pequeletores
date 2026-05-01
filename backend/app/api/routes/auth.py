"""Authentication API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

from sqlalchemy.ext.asyncio import AsyncSession

from ...models import Parent
from ...services import auth as auth_service
from ..deps import get_session

router = APIRouter(prefix="/auth", tags=["authentication"])


# Pydantic schemas
class ParentRegisterRequest(BaseModel):
    """Request schema for parent registration."""
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)


class ParentLoginRequest(BaseModel):
    """Request schema for parent login."""
    email: EmailStr
    password: str = Field(min_length=1)


class TokenResponse(BaseModel):
    """Response schema for authentication token."""
    access_token: str
    token_type: str = "bearer"


class ParentResponse(BaseModel):
    """Response schema for parent data."""
    id: int
    email: str

    model_config = {"from_attributes": True}


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: ParentRegisterRequest,
    session: AsyncSession = Depends(get_session)
):
    """Register a new parent account."""
    # Check if email already exists
    existing = await auth_service.get_parent_by_email(session, request.email)
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    # Create new parent
    parent = await auth_service.create_parent(
        session,
        request.email,
        request.password
    )
    
    # Generate token
    token = auth_service.create_token_for_parent(parent.id, parent.email)
    
    return TokenResponse(access_token=token, token_type="bearer")


@router.post("/login", response_model=TokenResponse)
async def login(
    request: ParentLoginRequest,
    session: AsyncSession = Depends(get_session)
):
    """Login with email and password."""
    # Authenticate parent
    parent = await auth_service.authenticate_parent(
        session,
        request.email,
        request.password
    )
    
    if not parent:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Generate token
    token = auth_service.create_token_for_parent(parent.id, parent.email)
    
    return TokenResponse(access_token=token, token_type="bearer")


@router.get("/me", response_model=ParentResponse)
async def get_current_parent(
    current_parent: Parent = Depends(get_session)
):
    """Get the current authenticated parent."""
    return current_parent