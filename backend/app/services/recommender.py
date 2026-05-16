"""Keyword-based recommender service for book recommendations."""

from typing import Any


class TFIDFRecommender:
    """Content-based recommender for books.
    
    Scores books by matching user preference keywords against
    book titles, authors, and subjects.
    """
    
    def __init__(self):
        """Initialize the recommender."""
        pass
    
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