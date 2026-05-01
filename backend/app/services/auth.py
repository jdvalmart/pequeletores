"""Authentication service with JWT and password handling."""

from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import get_settings
from ..models import Parent

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Settings
settings = get_settings()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        return payload
    except JWTError:
        return None


async def get_parent_by_email(session: AsyncSession, email: str) -> Optional[Parent]:
    """Get a parent by email address."""
    result = await session.execute(
        select(Parent).where(Parent.email == email)
    )
    return result.scalar_one_or_none()


async def create_parent(session: AsyncSession, email: str, password: str) -> Parent:
    """Create a new parent with hashed password."""
    password_hash = hash_password(password)
    parent = Parent(
        email=email,
        password_hash=password_hash
    )
    session.add(parent)
    await session.commit()
    await session.refresh(parent)
    return parent


async def authenticate_parent(
    session: AsyncSession, 
    email: str, 
    password: str
) -> Optional[Parent]:
    """Authenticate a parent by email and password."""
    parent = await get_parent_by_email(session, email)
    
    if not parent:
        return None
    
    if not verify_password(password, parent.password_hash):
        return None
    
    return parent


def create_token_for_parent(parent_id: int, email: str) -> str:
    """Create a JWT token for a parent."""
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    token_data = {
        "sub": str(parent_id),
        "email": email
    }
    return create_access_token(token_data, access_token_expires)