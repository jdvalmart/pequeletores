"""Badge model for Pequelectores gamification."""

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class Badge(Base):
    """Badge definition for achievement system."""

    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    icon = Column(String(100), nullable=False)
    requirement = Column(Integer, nullable=False)

    # Relationships
    children = relationship(
        "ChildBadge",
        back_populates="badge",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Badge(id={self.id}, name={self.name})>"


class ChildBadge(Base):
    """Association between child and earned badges."""

    __tablename__ = "child_badges"

    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(
        Integer,
        ForeignKey("children.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    badge_id = Column(
        Integer,
        ForeignKey("badges.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    earned_at = Column(Integer, nullable=False)

    # Relationships
    child = relationship("Child", back_populates="badges")
    badge = relationship("Badge", back_populates="children")

    def __repr__(self) -> str:
        return f"<ChildBadge(child_id={self.child_id}, badge_id={self.badge_id})>"