"""TF-IDF recommender service for book recommendations."""

from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class TFIDFRecommender:
    """TF-IDF based content recommender for books.
    
    Uses TF-IDF vectorization to score books based on their
    textual features (title, author, subjects) against
    user preference queries.
    """
    
    def __init__(self):
        """Initialize the recommender."""
        self._vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=5000,
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95
        )
        self._fitted = False
    
    def _prepare_text(self, book: dict[str, Any], queries: list[str]) -> str:
        """Prepare text features from a book for vectorization.
        
        Combines title, author, and subjects into a single text string.
        """
        parts = []
        
        # Add title
        if book.get("title"):
            parts.append(book["title"])
        
        # Add author
        if book.get("author"):
            parts.append(book["author"])
        
        # Add subjects as they are important for matching
        if book.get("subject"):
            parts.extend(book["subject"])
        
        # Combine with queries for context
        if queries:
            parts.extend(queries)
        
        return " ".join(parts)
    
    def score_books(
        self,
        books: list[dict[str, Any]],
        queries: list[str]
    ) -> list[dict[str, Any]]:
        """Score books based on keyword matching with user preferences.
        
        Args:
            books: List of book dictionaries
            queries: List of user preference queries
            
        Returns:
            List of books with added 'score' field
        """
        if not books or not queries:
            return books
        
        # Normalize queries to lowercase for matching
        query_terms = set(q.lower() for q in queries)
        
        scored_books = []
        for book in books:
            book_copy = book.copy()
            score = 0.0
            
            # Get book's subjects (lowercase for comparison)
            subjects = book.get("subject", [])
            subjects_lower = [s.lower() for s in subjects]
            
            # Score based on keyword matches in subjects
            for term in query_terms:
                for subject in subjects_lower:
                    if term in subject or subject in term:
                        score += 1.0
            
            # Bonus for title match
            title = book.get("title", "").lower()
            for term in query_terms:
                if term in title:
                    score += 0.5
            
            # Bonus for author match
            author = book.get("author", "").lower() if book.get("author") else ""
            for term in query_terms:
                if term in author:
                    score += 0.25
            
            book_copy["score"] = score
            scored_books.append(book_copy)
        
        return scored_books
    
    def get_top_recommendations(
        self,
        books: list[dict[str, Any]],
        queries: list[str],
        top_n: int = 10
    ) -> list[dict[str, Any]]:
        """Get top N book recommendations.
        
        Args:
            books: List of book dictionaries
            queries: List of user preference queries
            top_n: Number of recommendations to return
            
        Returns:
            List of top N scored books
        """
        scored = self.score_books(books, queries)
        scored.sort(key=lambda x: x.get("score", 0), reverse=True)
        return scored[:top_n]