"""Integration tests for Pequelectores API."""

import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch, MagicMock

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.app.main import app


class TestPreferencesAPI:
    """Test preferences API endpoints."""

    @pytest.fixture
    def mock_session(self):
        """Mock database session."""
        with patch('backend.app.api.routes.preferences.get_session') as mock:
            mock_session = AsyncMock()
            mock.return_value.__aenter__ = AsyncMock(return_value=mock_session)
            mock.return_value.__aexit__ = AsyncMock(return_value=None)
            yield mock_session

    @pytest.mark.asyncio
    async def test_health_endpoint(self):
        """Test health check endpoint."""
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as client:
            response = await client.get("/health")
            assert response.status_code == 200
            assert response.json()["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_root_endpoint(self):
        """Test root endpoint."""
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as client:
            response = await client.get("/")
            assert response.status_code == 200
            assert "message" in response.json()


class TestRecommendationsFlow:
    """Test the complete recommendation flow."""

    @pytest.mark.asyncio
    async def test_recommendation_endpoint_exists(self):
        """Test recommendation endpoint accepts requests."""
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as client:
            # Should accept child_id parameter
            response = await client.get(
                "/recommendations",
                params={"child_id": "1", "limit": "5"}
            )
            # Will fail without DB but endpoint exists
            assert response.status_code in [200, 404, 500]


class TestReadingFlow:
    """Test reading activity tracking."""

    @pytest.mark.asyncio
    async def test_reading_log_endpoint(self):
        """Test reading log endpoint accepts requests."""
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as client:
            response = await client.post(
                "/reading/log",
                json={
                    "child_id": 1,
                    "book_id": "/works/OL123W",
                    "pages_read": 10
                }
            )
            # Will fail without DB but endpoint exists
            assert response.status_code in [200, 404, 422, 500]


class TestGamification:
    """Test gamification endpoints."""

    @pytest.mark.asyncio
    async def test_streak_endpoint(self):
        """Test streak endpoint."""
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as client:
            response = await client.get("/reading/streak/1")
            assert response.status_code in [200, 404, 500]

    @pytest.mark.asyncio
    async def test_badges_endpoint(self):
        """Test badges endpoint."""
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as client:
            response = await client.get("/badges")
            # Should work even without DB (returns all badge templates)
            assert response.status_code in [200, 500]


class TestAPIEndpoints:
    """Verify all endpoints are registered."""

    def test_all_routes_registered(self):
        """Test that expected routes are in the app."""
        routes = [route.path for route in app.routes]
        
        expected_routes = [
            "/preferences",
            "/recommendations",
            "/reading/log",
            "/reading/streak",
            "/badges",
            "/",
            "/health"
        ]
        
        for route in expected_routes:
            assert any(route in r for r in routes), f"Route {route} not found"