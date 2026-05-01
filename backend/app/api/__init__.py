"""API package for Pequelectores."""

from . import deps
from .routes import preferences, recommendations, reading, gamification

__all__ = [
    "deps",
    "preferences",
    "recommendations",
    "reading",
    "gamification",
]