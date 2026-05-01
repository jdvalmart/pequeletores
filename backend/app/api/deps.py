"""Dependencies for API routes."""

from collections.abc import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import AsyncSessionLocal
from ..models import Parent
from ..services import auth as auth_service

# Security scheme
security = HTTPBearer()


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


async def get_current_parent(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
) -> Parent:
    """Get the current authenticated parent from JWT token.
    
    Usage:
        @app.get("/protected")
        async def protected_route(current_parent: Parent = Depends(get_current_parent)):
            ...
    """
    token = credentials.credentials
    
    # Decode token
    payload = auth_service.decode_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get parent_id from token
    parent_id = payload.get("sub")
    
    if not parent_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Fetch parent from database
    result = await session.execute(
        select(Parent).where(Parent.id == int(parent_id))
    )
    parent = result.scalar_one_or_none()
    
    if not parent:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Parent not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return parent


async def get_current_parent_optional(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
) -> Parent | None:
    """Get current parent if authenticated, None otherwise.
    
    Usage:
        @app.get("/optional-auth")
        async def optional_route(current_parent: Parent | None = Depends(get_current_parent_optional)):
            ...
    """
    try:
        return await get_current_parent(credentials, session)
    except HTTPException:
        return None