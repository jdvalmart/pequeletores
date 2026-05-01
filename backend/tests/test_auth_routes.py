"""Integration tests for authentication API routes."""

import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport

import sys
import os
# Add backend directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.main import app
from app.models import Parent
from app.services import auth as auth_service


class TestRegisterEndpoint:
    """Test POST /api/auth/register endpoint."""

    @pytest.fixture
    def mock_parent(self):
        """Create a mock parent object."""
        parent = MagicMock(spec=Parent)
        parent.id = 1
        parent.email = "test@test.com"
        parent.password_hash = "hashed"
        return parent

    @pytest.mark.asyncio
    async def test_register_success(self, mock_parent):
        """Test successful parent registration."""
        with patch('backend.app.services.auth.get_parent_by_email', new_callable=AsyncMock) as mock_get, \
             patch('backend.app.services.auth.create_parent', new_callable=AsyncMock) as mock_create, \
             patch('backend.app.services.auth.create_token_for_parent', return_value='test_token'):
            
            # No existing parent
            mock_get.return_value = None
            mock_create.return_value = mock_parent
            
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.post(
                    "/api/auth/register",
                    json={"email": "test@test.com", "password": "password123"}
                )
            
            assert response.status_code == 201
            data = response.json()
            assert "access_token" in data
            assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, mock_parent):
        """Test registration with existing email returns 409."""
        with patch('backend.app.services.auth.get_parent_by_email', new_callable=AsyncMock) as mock_get:
            # Parent already exists
            mock_get.return_value = mock_parent
            
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.post(
                    "/api/auth/register",
                    json={"email": "test@test.com", "password": "password123"}
                )
            
            assert response.status_code == 409
            data = response.json()
            assert "detail" in data
            assert "already registered" in data["detail"]

    @pytest.mark.asyncio
    async def test_register_invalid_email(self):
        """Test registration with invalid email returns 422."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/auth/register",
                json={"email": "not-an-email", "password": "password123"}
            )
        
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_register_short_password(self):
        """Test registration with short password returns 422."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/auth/register",
                json={"email": "test@test.com", "password": "short"}
            )
        
        assert response.status_code == 422


class TestLoginEndpoint:
    """Test POST /api/auth/login endpoint."""

    @pytest.fixture
    def mock_parent(self):
        """Create a mock parent object."""
        parent = MagicMock(spec=Parent)
        parent.id = 1
        parent.email = "test@test.com"
        parent.password_hash = auth_service.hash_password("correctpassword")
        return parent

    @pytest.mark.asyncio
    async def test_login_success(self, mock_parent):
        """Test successful login."""
        with patch('backend.app.services.auth.authenticate_parent', new_callable=AsyncMock) as mock_auth, \
             patch('backend.app.services.auth.create_token_for_parent', return_value='test_token'):
            
            mock_auth.return_value = mock_parent
            
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.post(
                    "/api/auth/login",
                    json={"email": "test@test.com", "password": "correctpassword"}
                )
            
            assert response.status_code == 200
            data = response.json()
            assert "access_token" in data
            assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self):
        """Test login with invalid credentials returns 401."""
        with patch('backend.app.services.auth.authenticate_parent', new_callable=AsyncMock) as mock_auth:
            mock_auth.return_value = None  # No parent found
            
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.post(
                    "/api/auth/login",
                    json={"email": "test@test.com", "password": "wrongpassword"}
                )
            
            assert response.status_code == 401
            data = response.json()
            assert "detail" in data

    @pytest.mark.asyncio
    async def test_login_nonexistent_email(self):
        """Test login with nonexistent email returns 401."""
        with patch('backend.app.services.auth.authenticate_parent', new_callable=AsyncMock) as mock_auth:
            mock_auth.return_value = None
            
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.post(
                    "/api/auth/login",
                    json={"email": "nonexistent@test.com", "password": "anypassword"}
                )
            
            assert response.status_code == 401


class TestMeEndpoint:
    """Test GET /api/auth/me endpoint."""

    @pytest.fixture
    def mock_parent(self):
        """Create a mock parent object."""
        parent = MagicMock(spec=Parent)
        parent.id = 1
        parent.email = "test@test.com"
        return parent

    @pytest.mark.asyncio
    async def test_me_without_token(self):
        """Test /me endpoint without token returns 403."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/api/auth/me")
        
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_me_with_valid_token(self, mock_parent):
        """Test /me endpoint with valid token returns parent data."""
        with patch('backend.app.services.auth.decode_token', return_value={"sub": "1", "email": "test@test.com"}), \
             patch('backend.app.api.deps.get_current_parent', return_value=mock_parent):
            
            # Create a valid token
            token = auth_service.create_token_for_parent(1, "test@test.com")
            
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.get(
                    "/api/auth/me",
                    headers={"Authorization": f"Bearer {token}"}
                )
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == 1
            assert data["email"] == "test@test.com"

    @pytest.mark.asyncio
    async def test_me_with_invalid_token(self):
        """Test /me endpoint with invalid token returns 401."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get(
                "/api/auth/me",
                headers={"Authorization": "Bearer invalid_token"}
            )
        
        assert response.status_code == 401