"""Open Library API client with caching."""

import asyncio
import time
from collections.abc import AsyncGenerator
from typing import Any

import httpx


class OpenLibraryClient:
    """Async client for Open Library API with 24-hour cache.
    
    Uses a simple in-memory cache with TTL to avoid excessive API calls.
    """
    
    BASE_URL = "https://openlibrary.org"
    SEARCH_URL = f"{BASE_URL}/search.json"
    WORKS_URL = f"{BASE_URL}/works"
    
    # Cache TTL in seconds (24 hours)
    CACHE_TTL = 24 * 60 * 60
    
    def __init__(self):
        self._cache: dict[str, tuple[Any, float]] = {}
        self._lock = asyncio.Lock()
        self._client: httpx.AsyncClient | None = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create the HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.BASE_URL,
                timeout=30.0,
                follow_redirects=True,
                headers={
                    "User-Agent": "PequeLectores/1.0 (pequelectores.app@example.com)"
                }
            )
        return self._client
    
    async def close(self):
        """Close the HTTP client."""
        if self._client is not None and not self._client.is_closed:
            await self._client.aclose()
    
    async def _get_from_cache(self, key: str) -> Any | None:
        """Get value from cache if not expired."""
        if key in self._cache:
            value, expires_at = self._cache[key]
            if time.time() < expires_at:
                return value
            else:
                del self._cache[key]
        return None
    
    async def _set_in_cache(self, key: str, value: Any):
        """Set value in cache with TTL."""
        expires_at = time.time() + self.CACHE_TTL
        self._cache[key] = (value, expires_at)
    
    async def search_books(
        self,
        query: str,
        limit: int = 10
    ) -> list[dict[str, Any]]:
        """Search for books by query/subject.
        
        Args:
            query: Search query (subject, genre, or general search)
            limit: Maximum number of results to return
            
        Returns:
            List of book dictionaries with key details
        """
        cache_key = f"search:{query}:{limit}"
        
        # Check cache
        cached = await self._get_from_cache(cache_key)
        if cached is not None:
            return cached
        
        # Make API request
        client = await self._get_client()
        
        try:
            # Open Library uses 'subject' parameter for subject searches
            response = await client.get(
                self.SEARCH_URL,
                params={
                    "q": query,
                    "limit": limit,
                    "fields": "key,title,author_name,cover_i,first_publish_year,subject"
                }
            )
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPError as e:
            # Return empty list on error instead of raising
            print(f"Open Library API error: {e}")
            return []
        
        # Parse results
        books = []
        docs = data.get("docs", [])
        
        for doc in docs:
            book = {
                "key": doc.get("key", ""),
                "title": doc.get("title", "Unknown"),
                "author": doc.get("author_name", [None])[0] if doc.get("author_name") else None,
                "cover_url": self._get_cover_url(doc.get("cover_i")),
                "first_publish_year": doc.get("first_publish_year"),
                "subject": doc.get("subject", [])[:5] if doc.get("subject") else []
            }
            books.append(book)
        
        # Cache result
        await self._set_in_cache(cache_key, books)
        
        return books
    
    async def get_book_details(self, work_key: str) -> dict[str, Any] | None:
        """Get detailed information about a book by work key.
        
        Args:
            work_key: Open Library work key (e.g., /works/OL123W)
            
        Returns:
            Dictionary with book details or None if not found
        """
        cache_key = f"work:{work_key}"
        
        # Check cache
        cached = await self._get_from_cache(cache_key)
        if cached is not None:
            return cached
        
        # Make API request
        client = await self._get_client()
        
        try:
            response = await client.get(f"{work_key}.json")
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPError as e:
            print(f"Open Library API error: {e}")
            return None
        
        # Parse details
        book = {
            "key": work_key,
            "title": data.get("title", "Unknown"),
            "description": self._extract_description(data.get("description")),
            "covers": data.get("covers", []),
            "subjects": data.get("subjects", [])[:10] if data.get("subjects") else []
        }
        
        # Cache result
        await self._set_in_cache(cache_key, book)
        
        return book
    
    def _get_cover_url(self, cover_id: int | None) -> str | None:
        """Generate cover URL from cover ID."""
        if cover_id is None:
            return None
        # Open Library cover URL format
        return f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
    
    def _extract_description(self, description: Any) -> str | None:
        """Extract text from description field (can be string or dict)."""
        if description is None:
            return None
        if isinstance(description, str):
            return description
        if isinstance(description, dict):
            return description.get("value")
        return None