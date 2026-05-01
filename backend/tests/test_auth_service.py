"""Unit tests for the authentication service."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

import sys
import os
# Add backend directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.services import auth as auth_service


class TestPasswordHashing:
    """Test password hashing and verification using mocks."""

    @patch('app.services.auth.pwd_context')
    def test_hash_password_returns_string(self, mock_pwd_context):
        """Test that hash_password returns a hashed string."""
        # Mock the hash function
        mock_pwd_context.hash.return_value = "$2b$12$MockedHashString1234567890"
        
        result = auth_service.hash_password("testpassword123")
        
        # Should return a string (mocked hash)
        assert isinstance(result, str)
        assert result == "$2b$12$MockedHashString1234567890"
        mock_pwd_context.hash.assert_called_once_with("testpassword123")

    @patch('app.services.auth.pwd_context')
    def test_verify_password_correct(self, mock_pwd_context):
        """Test that verify_password returns True for correct password."""
        # Mock verify to return True
        mock_pwd_context.verify.return_value = True
        
        result = auth_service.verify_password("mysecretpassword", "hashed_pw")
        
        assert result is True
        mock_pwd_context.verify.assert_called_once_with("mysecretpassword", "hashed_pw")

    @patch('app.services.auth.pwd_context')
    def test_verify_password_incorrect(self, mock_pwd_context):
        """Test that verify_password returns False for incorrect password."""
        # Mock verify to return False
        mock_pwd_context.verify.return_value = False
        
        result = auth_service.verify_password("wrongpassword", "hashed_pw")
        
        assert result is False
        mock_pwd_context.verify.assert_called_once_with("wrongpassword", "hashed_pw")

    @patch('app.services.auth.pwd_context')
    def test_different_hashes_for_same_password(self, mock_pwd_context):
        """Test that same password produces different hashes (salt) with mock."""
        # Each call returns a different hash
        mock_pwd_context.hash.side_effect = ["$2b$hash1", "$2b$hash2"]
        
        password = "samepassword"
        
        hash1 = auth_service.hash_password(password)
        hash2 = auth_service.hash_password(password)
        
        # Each hash should be different due to side_effect
        assert hash1 == "$2b$hash1"
        assert hash2 == "$2b$hash2"
        assert hash1 != hash2


class TestJWT:
    """Test JWT token creation and decoding."""

    def test_create_access_token_returns_string(self):
        """Test that create_access_token returns a JWT string."""
        result = auth_service.create_access_token({"sub": "123", "email": "test@test.com"})
        
        assert isinstance(result, str)
        # JWT has 3 parts separated by dots
        assert len(result.split(".")) == 3

    def test_create_access_token_with_expiry(self):
        """Test that token can be created with custom expiry."""
        from datetime import timedelta
        
        result = auth_service.create_access_token(
            {"sub": "123"},
            expires_delta=timedelta(hours=1)
        )
        
        assert isinstance(result, str)

    def test_decode_token_returns_payload(self):
        """Test that decode_token returns the payload."""
        payload = {"sub": "123", "email": "test@test.com"}
        token = auth_service.create_access_token(payload)
        
        decoded = auth_service.decode_token(token)
        
        assert decoded is not None
        assert decoded["sub"] == "123"
        assert decoded["email"] == "test@test.com"

    def test_decode_token_invalid_returns_none(self):
        """Test that decode_token returns None for invalid token."""
        result = auth_service.decode_token("invalid.token.here")
        
        assert result is None

    def test_decode_token_tampered_returns_none(self):
        """Test that decode_token returns None for tampered token."""
        payload = {"sub": "123"}
        token = auth_service.create_access_token(payload)
        
        # Tamper with the token
        tampered_token = token[:-5] + "xxxxx"
        
        result = auth_service.decode_token(tampered_token)
        
        assert result is None


class TestTokenCreation:
    """Test token creation for parent."""

    def test_create_token_for_parent_returns_valid_token(self):
        """Test that create_token_for_parent returns a valid JWT."""
        token = auth_service.create_token_for_parent(1, "parent@test.com")
        
        assert isinstance(token, str)
        assert len(token.split(".")) == 3

    def test_token_contains_parent_id(self):
        """Test that the token contains the parent_id."""
        token = auth_service.create_token_for_parent(42, "parent@test.com")
        
        decoded = auth_service.decode_token(token)
        
        assert decoded is not None
        assert decoded["sub"] == "42"
        assert decoded["email"] == "parent@test.com"


class TestAuthServiceIntegration:
    """Integration tests for auth service functions."""

    @patch('app.services.auth.pwd_context')
    def test_password_roundtrip(self, mock_pwd_context):
        """Test that password can be hashed and verified in a roundtrip."""
        # Mock the hash to return a consistent hash
        mock_pwd_context.hash.return_value = "$2b$hashedpassword"
        mock_pwd_context.verify.return_value = True
        
        password = "SecureP@ssw0rd!"
        
        hashed = auth_service.hash_password(password)
        verified = auth_service.verify_password(password, hashed)
        
        assert verified is True

    def test_token_and_decode_roundtrip(self):
        """Test that token can be created and decoded."""
        parent_id = 100
        email = "integration@test.com"
        
        token = auth_service.create_token_for_parent(parent_id, email)
        decoded = auth_service.decode_token(token)
        
        assert decoded is not None
        assert int(decoded["sub"]) == parent_id
        assert decoded["email"] == email