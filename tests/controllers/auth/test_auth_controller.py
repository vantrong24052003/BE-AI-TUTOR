"""
Tests for AuthController.

Uses:
- pytest: Test framework
- pytest-asyncio: Async test support
- httpx: HTTP client
- faker: Fake data generation
- pytest-mock: Mocking
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.unit
@pytest.mark.auth
class TestAuthController:
    """Tests for authentication endpoints."""

    async def test_register_success(
        self,
        client: AsyncClient,
        user_data: dict,
        register_url: str,
    ):
        """Test successful user registration."""
        response = await client.post(register_url, json=user_data)

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["name"] == user_data["name"]
        assert "id" in data
        assert "password" not in data  # Password should not be returned

    async def test_register_duplicate_email(
        self,
        client: AsyncClient,
        test_user: dict,
        user_data: dict,
        register_url: str,
    ):
        """Test registration with duplicate email fails."""
        user_data["email"] = test_user["email"]
        response = await client.post(register_url, json=user_data)

        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()

    async def test_register_invalid_email(
        self,
        client: AsyncClient,
        user_data: dict,
        register_url: str,
    ):
        """Test registration with invalid email fails."""
        user_data["email"] = "invalid-email"
        response = await client.post(register_url, json=user_data)

        assert response.status_code == 422  # Validation error

    async def test_register_weak_password(
        self,
        client: AsyncClient,
        user_data: dict,
        register_url: str,
    ):
        """Test registration with weak password fails."""
        user_data["password"] = "123"
        response = await client.post(register_url, json=user_data)

        assert response.status_code == 422

    async def test_login_success(
        self,
        client: AsyncClient,
        test_user: dict,
        login_url: str,
    ):
        """Test successful login."""
        login_data = {
            "email": test_user["email"],
            "password": "Test@123456",  # Original password
        }
        response = await client.post(login_url, json=login_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    async def test_login_wrong_password(
        self,
        client: AsyncClient,
        test_user: dict,
        login_url: str,
    ):
        """Test login with wrong password fails."""
        login_data = {
            "email": test_user["email"],
            "password": "WrongPassword123",
        }
        response = await client.post(login_url, json=login_data)

        assert response.status_code == 401

    async def test_login_nonexistent_user(
        self,
        client: AsyncClient,
        faker,
        login_url: str,
    ):
        """Test login with nonexistent user fails."""
        login_data = {
            "email": faker.email(),
            "password": "SomePassword123",
        }
        response = await client.post(login_url, json=login_data)

        assert response.status_code == 401

    async def test_get_profile_authenticated(
        self,
        auth_client: AsyncClient,
        test_user: dict,
        profile_url: str,
    ):
        """Test getting profile when authenticated."""
        response = await auth_client.get(profile_url)

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user["email"]

    async def test_get_profile_unauthenticated(
        self,
        client: AsyncClient,
        profile_url: str,
    ):
        """Test getting profile without auth fails."""
        response = await client.get(profile_url)

        assert response.status_code == 401

    async def test_update_profile(
        self,
        auth_client: AsyncClient,
        faker,
        profile_url: str,
    ):
        """Test updating user profile."""
        update_data = {"name": faker.name()}
        response = await auth_client.put(profile_url, json=update_data)

        assert response.status_code == 200
        assert response.json()["name"] == update_data["name"]
