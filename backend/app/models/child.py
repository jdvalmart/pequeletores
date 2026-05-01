"""Child model for Pequelectores."""

from datetime import date
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class Child(Base):
    """Child user model representing a child reader."""

    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    birth_date = Column(Date, nullable=False)
    age = Column(Integer, nullable=False)
    parent_id = Column(Integer, ForeignKey("parents.id"), nullable=True, index=True)

    # Relationships
    parent = relationship("Parent", back_populates="children")
    preferences = relationship(
        "ChildPreferences",
        back_populates="child",
        uselist=False,
        cascade="all, delete-orphan"
    )
    reading_logs = relationship(
        "ReadingLog",
        back_populates="child",
        cascade="all, delete-orphan"
    )
    badges = relationship(
        "ChildBadge",
        back_populates="child",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Child(id={self.id}, name={self.name}, age={self.age})>"