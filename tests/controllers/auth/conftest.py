"""
Pytest fixtures for auth controller tests.
"""
import pytest
from httpx import AsyncClient


@pytest.fixture
def register_url() -> str:
    """Registration endpoint URL."""
    return "/api/v1/auth/register"


@pytest.fixture
def login_url() -> str:
    """Login endpoint URL."""
    return "/api/v1/auth/login"


@pytest.fixture
def profile_url() -> str:
    """Profile endpoint URL."""
    return "/api/v1/auth/profile"
