"""Recommendations API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..deps import get_session
from ...models import Child, ChildPreferences
from ...services.recommender import TFIDFRecommender
from ...services.openlibrary import OpenLibraryClient


router = APIRouter(prefix="/recommendations", tags=["recommendations"])


class BookRecommendation(BaseModel):
    """Schema for a book recommendation."""
    key: str
    title: str
    author: str | None
    cover_url: str | None
    first_publish_year: int | None
    subject: list[str]
    score: float


class RecommendationsResponse(BaseModel):
    """Schema for recommendations response."""
    recommendations: list[BookRecommendation]
    total: int


@router.get("", response_model=RecommendationsResponse)
async def get_recommendations(
    child_id: int,
    limit: int = 10,
    session: AsyncSession = Depends(get_session)
):
    """Get book recommendations for a child based on their preferences."""
    # Get child's preferences
    result = await session.execute(
        select(ChildPreferences).where(
            ChildPreferences.child_id == child_id
        )
    )
    preferences = result.scalar_one_or_none()
    
    if not preferences or not preferences.icon_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Child has no preferences set. Please set preferences first."
        )
    
    # Get recommender and client
    recommender = TFIDFRecommender()
    ol_client = OpenLibraryClient()
    
    # Get recommendation queries from preferences
    queries = _icon_ids_to_queries(preferences.icon_ids)
    
    # Fetch books for each query
    all_books = []
    seen_keys = set()
    
    for query in queries:
        books = await ol_client.search_books(query, limit=20)
        for book in books:
            if book["key"] not in seen_keys:
                seen_keys.add(book["key"])
                all_books.append(book)
    
    if not all_books:
        return RecommendationsResponse(recommendations=[], total=0)
    
    # Calculate TF-IDF scores
    scored_books = recommender.score_books(all_books, queries)
    
    # Sort by score and take top N
    scored_books.sort(key=lambda x: x["score"], reverse=True)
    top_books = scored_books[:limit]
    
    # Convert to response models
    recommendations = [
        BookRecommendation(
            key=book["key"],
            title=book["title"],
            author=book.get("author"),
            cover_url=book.get("cover_url"),
            first_publish_year=book.get("first_publish_year"),
            subject=book.get("subject", []),
            score=book["score"]
        )
        for book in top_books
    ]
    
    return RecommendationsResponse(recommendations=recommendations, total=len(recommendations))


def _icon_ids_to_queries(icon_ids: list[str]) -> list[str]:
    """Convert icon IDs to search queries for Open Library.
    
    Maps visual icons to book genres/subjects for search.
    Handles both old format (animal-dog) and new format (dog, dinosaur).
    """
    # Mapping for all icon formats
    icon_to_genre = {
        # Animals - new format
        "dog": ["dogs", "pets", "animal stories"],
        "cat": ["cats", "pets", "animal stories"],
        "dinosaur": ["dinosaurs", "prehistoric", "animal stories"],
        "horse": ["horses", "animal fiction"],
        "dragon": ["dragons", "fantasy"],
        "butterfly": ["butterflies", "nature"],
        
        # Adventure - new format
        "rocket": ["space", "astronauts", "science fiction"],
        "compass": ["explorers", "adventure"],
        "mountain": ["mountains", "nature", "adventure"],
        "ship": ["ships", "pirates", "adventure"],
        "treasure": ["treasure", "adventure"],
        "map": ["maps", "explorers"],
        
        # Fantasy - new format  
        "wizard": ["wizards", "magic", "fantasy"],
        "fairy": ["fairies", "fantasy"],
        "ghost": ["ghosts", "horror", "mystery"],
        "magic": ["magic", "fantasy"],
        "castle": ["castles", "fantasy"],
        "crown": ["kings", "queens", "fantasy"],
        
        # Science - new format
        "science": ["science", "educational"],
        "earth": ["earth", "nature", "science"],
        "star": ["stars", "space", "astronomy"],
        "robot": ["robots", "science fiction"],
        "brain": ["brain", "science", "thinking"],
        "lightbulb": ["ideas", "inventions"],
        
        # Sports - new format
        "soccer": ["soccer", "sports"],
        "basketball": ["basketball", "sports"],
        "swimming": ["swimming", "sports"],
        "bicycle": ["bicycling", "sports"],
        "trophy": ["trophies", "sports"],
        "medal": ["olympics", "sports"],
        
        # Fun - new format
        "laugh": ["humor", "comedy", "funny"],
        "art": ["art", "creative"],
        "music": ["music", "songs"],
        "game": ["games", "video games"],
        "camera": ["photography", "art"],
        "heart": ["love", "friendship", "family"],
        
        # Old format (backup)
        "animal-dog": ["dogs", "pets"],
        "animal-cat": ["cats", "pets"],
        "animal-horse": ["horses", "animal fiction"],
        "animal-dino": ["dinosaurs", "prehistoric animals"],
        "fantasy-dragon": ["dragons", "fantasy"],
        "fantasy-magic": ["magic", "fantasy fiction"],
    }
    
    queries = []
    for icon_id in icon_ids:
        if icon_id in icon_to_genre:
            queries.extend(icon_to_genre[icon_id])
    
    # Return unique queries, limit to avoid too many API calls
    return list(dict.fromkeys(queries))[:5]