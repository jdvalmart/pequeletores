"""Parent model for authentication."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from ..database import Base


class Parent(Base):
    """Parent user model for authentication and child management."""

    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships - parent can manage multiple children
    children = relationship(
        "Child",
        back_populates="parent",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Parent(id={self.id}, email={self.email})>"