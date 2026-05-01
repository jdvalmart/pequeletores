"""Tests for error handling middleware."""

import pytest
from unittest.mock import MagicMock, patch
from httpx import AsyncClient, ASGITransport

import sys
import os
# Add backend directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.main import app
from app.middleware.errors import (
    AppException,
    NotFoundException,
    ConflictException,
    UnauthorizedException,
    ForbiddenException,
    setup_error_handlers
)


class TestAppException:
    """Test custom application exceptions."""

    def test_app_exception_default(self):
        """Test AppException with default status code."""
        exc = AppException("Something went wrong")
        
        assert exc.message == "Something went wrong"
        assert exc.status_code == 500

    def test_app_exception_custom_status(self):
        """Test AppException with custom status code."""
        exc = AppException("Custom error", status_code=418)
        
        assert exc.message == "Custom error"
        assert exc.status_code == 418


class TestSpecificExceptions:
    """Test specific exception types."""

    def test_not_found_exception(self):
        """Test NotFoundException returns 404."""
        exc = NotFoundException("Child not found")
        
        assert exc.status_code == 404
        assert "not found" in exc.message.lower()

    def test_conflict_exception(self):
        """Test ConflictException returns 409."""
        exc = ConflictException("Email already exists")
        
        assert exc.status_code == 409
        assert "conflict" in exc.message.lower() or "exists" in exc.message.lower()

    def test_unauthorized_exception(self):
        """Test UnauthorizedException returns 401."""
        exc = UnauthorizedException("Not authenticated")
        
        assert exc.status_code == 401

    def test_forbidden_exception(self):
        """Test ForbiddenException returns 403."""
        exc = ForbiddenException("Access denied")
        
        assert exc.status_code == 403


class TestErrorHandlers:
    """Test error handlers are properly registered."""

    def test_error_handlers_registered(self):
        """Test that error handlers are registered on the app."""
        # Check that the app has exception handlers registered
        # The handlers are registered in create_app via setup_error_handlers
        assert app.exception_handlers  # Should have exception handlers
        
        # Check that our custom handlers are there
        assert AppException in app.exception_handlers
        # Note: ValidationError might not be directly in dict, depends on version


class TestErrorResponses:
    """Test error response formats."""

    @pytest.mark.asyncio
    async def test_not_found_returns_404(self):
        """Test that missing route returns 404."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/api/nonexistent")
        
        # Should return 404 for unknown route
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_validation_error_returns_422(self):
        """Test that validation error returns proper format."""
        # Create a route that will fail validation
        from fastapi import APIRouter, Depends
        from pydantic import BaseModel, Field
        from backend.app.api.deps import get_session
        
        test_router = APIRouter()
        
        @test_router.post("/test-validation")
        async def test_validation(
            data: str = Field(..., min_length=5),
            session = Depends(get_session)
        ):
            return {"data": data}
        
        app.include_router(test_router, prefix="/api")
        
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/test-validation",
                json={"data": "ab"}  # Too short
            )
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data


class TestErrorResponseFormat:
    """Test the format of error responses."""

    @pytest.mark.asyncio
    async def test_error_response_has_detail(self):
        """Test that error responses include 'detail' field."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/api/nonexistent")
        
        data = response.json()
        assert "detail" in data or "message" in data

    @pytest.mark.asyncio
    async def test_validation_error_includes_field_info(self):
        """Test that validation errors include field information."""
        # Create test endpoint
        from fastapi import APIRouter, Body
        from pydantic import BaseModel
        
        class TestModel(BaseModel):
            name: str = Field(..., min_length=3)
        
        test_router = APIRouter()
        
        @test_router.post("/test-model")
        async def test_model(data: TestModel):
            return data
        
        app.include_router(test_router, prefix="/api")
        
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/test-model",
                json={"name": "ab"}
            )
        
        assert response.status_code == 422
        data = response.json()
        # Should have errors array with field info
        assert "errors" in data or "detail" in data