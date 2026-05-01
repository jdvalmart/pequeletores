"""Child preferences model for Pequelectores."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from ..database import Base


class ChildPreferences(Base):
    """Preferences selected by a child for book recommendations."""

    __tablename__ = "child_preferences"

    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(
        Integer,
        ForeignKey("children.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )
    icon_ids = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    child = relationship("Child", back_populates="preferences")

    def __repr__(self) -> str:
        return f"<ChildPreferences(child_id={self.child_id})>"