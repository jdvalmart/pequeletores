"""API package for Pequelectores."""

import app.api.routes.preferences
import app.api.routes.recommendations
import app.api.routes.reading
import app.api.routes.gamification

from app.api.routes import preferences, recommendations, reading, gamification

__all__ = [
    "preferences",
    "recommendations",
    "reading",
    "gamification",
]