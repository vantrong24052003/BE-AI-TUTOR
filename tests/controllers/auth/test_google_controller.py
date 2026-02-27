"""
Tests for Google OAuth Controller.

Uses pytest-mock for mocking OAuth flow.
"""
import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
@pytest.mark.unit
@pytest.mark.auth
class TestGoogleController:
    """Tests for Google OAuth endpoints."""

    async def test_google_auth_redirect(
        self,
        client: AsyncClient,
    ):
        """Test Google OAuth redirect."""
        response = await client.get("/api/v1/auth/google")

        assert response.status_code == 200
        # Should return redirect URL or authorization URL
        data = response.json()
        assert "authorization_url" in data or "redirect" in data

    async def test_google_callback_success(
        self,
        client: AsyncClient,
        mocker,
    ):
        """Test successful Google OAuth callback."""
        # Mock the OAuth service
        mock_service = mocker.patch(
            "src.services.auth.google_service.GoogleAuthService.authenticate"
        )
        mock_service.return_value = {
            "access_token": "test_token",
            "user": {"email": "test@gmail.com", "name": "Test User"},
        }

        response = await client.get(
            "/api/v1/auth/google/callback",
            params={"code": "test_code", "state": "test_state"},
        )

        assert response.status_code == 200
        assert "access_token" in response.json()

    async def test_google_callback_invalid_code(
        self,
        client: AsyncClient,
        mocker,
    ):
        """Test Google OAuth callback with invalid code."""
        mock_service = mocker.patch(
            "src.services.auth.google_service.GoogleAuthService.authenticate"
        )
        mock_service.side_effect = Exception("Invalid authorization code")

        response = await client.get(
            "/api/v1/auth/google/callback",
            params={"code": "invalid_code", "state": "test_state"},
        )

        assert response.status_code == 400

    async def test_google_callback_missing_state(
        self,
        client: AsyncClient,
    ):
        """Test Google OAuth callback without state parameter."""
        response = await client.get(
            "/api/v1/auth/google/callback",
            params={"code": "test_code"},
        )

        assert response.status_code == 400
