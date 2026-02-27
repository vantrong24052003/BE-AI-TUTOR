"""
Tests for AuthService.

Unit tests for business logic layer.
Uses pytest-mock for mocking repository calls.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock

from src.services.auth.auth_service import AuthService
from src.exceptions.auth import InvalidCredentialsError, UserAlreadyExistsError


@pytest.mark.asyncio
@pytest.mark.unit
class TestAuthService:
    """Tests for AuthService business logic."""

    async def test_register_new_user_success(
        self,
        db_session,
        user_data: dict,
        mocker,
    ):
        """Test successful user registration."""
        # Arrange
        mock_repo = MagicMock()
        mock_repo.get_by_email = AsyncMock(return_value=None)
        mock_repo.create = AsyncMock(return_value=MagicMock(
            id=1,
            email=user_data["email"],
            name=user_data["name"],
        ))

        service = AuthService(db_session, mock_repo)

        # Act
        result = await service.register(user_data)

        # Assert
        assert result.email == user_data["email"]
        mock_repo.get_by_email.assert_called_once_with(user_data["email"])
        mock_repo.create.assert_called_once()

    async def test_register_duplicate_user_fails(
        self,
        db_session,
        user_data: dict,
        mocker,
    ):
        """Test registration fails for duplicate email."""
        # Arrange
        mock_repo = MagicMock()
        mock_repo.get_by_email = AsyncMock(return_value=MagicMock())

        service = AuthService(db_session, mock_repo)

        # Act & Assert
        with pytest.raises(UserAlreadyExistsError):
            await service.register(user_data)

    async def test_login_success(
        self,
        db_session,
        test_user: dict,
        mocker,
    ):
        """Test successful login."""
        # Arrange
        mock_repo = MagicMock()
        mock_user = MagicMock()
        mock_user.email = test_user["email"]
        mock_user.password = test_user.get("hashed_password")
        mock_repo.get_by_email = AsyncMock(return_value=mock_user)

        mock_password = mocker.patch("src.lib.password.verify_password")
        mock_password.return_value = True

        mock_jwt = mocker.patch("src.lib.jwt.create_access_token")
        mock_jwt.return_value = "test_token"

        service = AuthService(db_session, mock_repo)

        # Act
        result = await service.login(test_user["email"], "Test@123456")

        # Assert
        assert result["access_token"] == "test_token"
        assert result["token_type"] == "bearer"

    async def test_login_wrong_password_fails(
        self,
        db_session,
        test_user: dict,
        mocker,
    ):
        """Test login fails with wrong password."""
        # Arrange
        mock_repo = MagicMock()
        mock_user = MagicMock()
        mock_user.email = test_user["email"]
        mock_repo.get_by_email = AsyncMock(return_value=mock_user)

        mock_password = mocker.patch("src.lib.password.verify_password")
        mock_password.return_value = False

        service = AuthService(db_session, mock_repo)

        # Act & Assert
        with pytest.raises(InvalidCredentialsError):
            await service.login(test_user["email"], "WrongPassword")

    async def test_login_nonexistent_user_fails(
        self,
        db_session,
        faker,
        mocker,
    ):
        """Test login fails for nonexistent user."""
        # Arrange
        mock_repo = MagicMock()
        mock_repo.get_by_email = AsyncMock(return_value=None)

        service = AuthService(db_session, mock_repo)

        # Act & Assert
        with pytest.raises(InvalidCredentialsError):
            await service.login(faker.email(), "SomePassword")
