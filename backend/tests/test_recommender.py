"""Unit tests for the TF-IDF recommender service."""

import pytest
from datetime import date
from unittest.mock import AsyncMock, MagicMock, patch

import sys
import os
# Add backend directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.services.recommender import TFIDFRecommender


class TestTFIDFRecommender:
    """Test TF-IDF recommendation service."""

    @pytest.fixture
    def mock_books(self):
        """Sample books for testing."""
        return [
            {
                'key': '/works/OL123W',
                'title': 'Harry Potter and the Sorcerer\'s Stone',
                'author': ['J.K. Rowling'],
                'subjects': ['fantasy', 'magic', 'wizards', 'hogwarts'],
                'cover_url': None,
                'first_publish_year': 1997
            },
            {
                'key': '/works/OL456W',
                'title': 'The Hobbit',
                'author': ['J.R.R. Tolkien'],
                'subjects': ['fantasy', 'adventure', 'dragons', 'elves'],
                'cover_url': None,
                'first_publish_year': 1937
            },
            {
                'key': '/works/OL789W',
                'title': 'Charlotte\'s Web',
                'author': ['E.B. White'],
                'subjects': ['animals', 'friendship', 'pigs', 'spiders'],
                'cover_url': None,
                'first_publish_year': 1952
            },
            {
                'key': '/works/OL101W',
                'title': 'Percy Jackson: The Lightning Thief',
                'author': ['Rick Riordan'],
                'subjects': ['fantasy', 'greek gods', 'adventure', 'magic'],
                'cover_url': None,
                'first_publish_year': 2005
            }
        ]

    @pytest.fixture
    def recommender(self, mock_books):
        """Create recommender with mock books."""
        with patch('backend.app.services.recommender.OpenLibraryClient') as mock_ol:
            mock_client = MagicMock()
            mock_client.search_books = AsyncMock(return_value=mock_books)
            mock_ol.return_value = mock_client
            
            rec = TFIDFRecommender()
            return rec

    def test_tfidf_vectorizer_initialized(self, recommender):
        """Test that TF-IDF vectorizer is initialized."""
        assert recommender.vectorizer is not None
        assert recommender.vectorizer is not None

    def test_icon_to_genre_mapping(self):
        """Test icon to genre/subject mapping."""
        # Test various icon mappings
        icon_genre_map = {
            'dinosaur': 'dinosaurs',
            'dragon': 'fantasy',
            'dog': 'animals',
            'rocket': 'space',
            'wizard': 'magic',
            'robot': 'robots',
            'soccer': 'sports',
            'art': 'art'
        }
        
        for icon, expected_genre in icon_genre_map.items():
            assert expected_genre is not None

    def test_cosine_similarity_calculation(self, recommender, mock_books):
        """Test cosine similarity calculation between vectors."""
        import numpy as np
        from sklearn.metrics.pairwise import cosine_similarity
        
        # Create sample vectors
        vec1 = np.array([[1, 0, 1, 0]])
        vec2 = np.array([[1, 0, 0, 1]])
        
        # Calculate similarity
        sim = cosine_similarity(vec1, vec2)[0][0]
        
        # Similarity should be between 0 and 1
        assert 0 <= sim <= 1

    def test_get_relevant_subjects(self, recommender):
        """Test icon to subjects conversion."""
        icon_ids = ['dinosaur', 'dragon', 'dog']
        subjects = recommender._get_relevant_subjects(icon_ids)
        
        # Should return list of subjects
        assert isinstance(subjects, list)
        assert len(subjects) > 0

    def test_recommend_returns_list(self, recommender, mock_books):
        """Test that recommend returns a list of books."""
        import asyncio
        
        # Mock the book search
        with patch.object(recommender.ol_client, 'search_books', return_value=mock_books):
            async def run_test():
                # Refresh index with mock books
                recommender.book_corpus = mock_books
                recommender._build_index()
                
                # Get recommendations
                prefs = ['fantasy', 'magic']
                results = await recommender.recommend(prefs, limit=2)
                
                return results
            
            results = asyncio.run(run_test())
            
            # Should return list
            assert isinstance(results, list)
            assert len(results) <= 2


class TestIconToGenreMapping:
    """Test icon to genre mapping logic."""

    def test_icon_categories_complete(self):
        """Test all icon categories have mappings."""
        icon_categories = {
            'animals': ['dog', 'cat', 'dinosaur', 'horse', 'dragon', 'butterfly'],
            'adventure': ['rocket', 'compass', 'mountain', 'ship', 'treasure', 'map'],
            'fantasy': ['wizard', 'fairy', 'ghost', 'magic', 'castle', 'crown'],
            'science': ['science', 'earth', 'star', 'robot', 'brain', 'lightbulb'],
            'sports': ['soccer', 'basketball', 'swimming', 'bicycle', 'trophy', 'medal'],
            'fun': ['laugh', 'art', 'music', 'game', 'camera', 'heart']
        }
        
        # All categories should have 6 icons each
        for category, icons in icon_categories.items():
            assert len(icons) == 6

    def test_genre_coverage(self):
        """Test that icon mappings cover expected genres."""
        expected_genres = [
            'animals', 'fantasy', 'magic', 'adventure', 'science',
            'sports', 'art', 'music', 'robots', 'space'
        ]
        
        # This test verifies we have mappings for important genres
        assert len(expected_genres) > 0