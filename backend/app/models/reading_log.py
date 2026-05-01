"""Reading log model for Pequelectores."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class ReadingLog(Base):
    """Reading activity log for tracking pages read."""

    __tablename__ = "reading_logs"

    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(
        Integer,
        ForeignKey("children.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    book_id = Column(String(255), nullable=False, index=True)
    pages_read = Column(Integer, nullable=False, default=0)
    logged_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    child = relationship("Child", back_populates="reading_logs")

    def __repr__(self) -> str:
        return f"<ReadingLog(child_id={self.child_id}, book_id={self.book_id})>"