"""
Global pytest fixtures and configuration.

Libraries used:
- pytest: Testing framework
- pytest-asyncio: Async test support
- pytest-mock: Mocking utilities
- httpx: HTTP client for API testing
- faker: Fake data generation
- freezegun: Mock datetime
- factory-boy: Test factories
- respx: Mock HTTP requests
"""
import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from faker import Faker
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from freezegun import api as freezegun

from src.main import app
from src.core.database import Base, get_db

# Initialize Faker
fake = Faker()

# Test database URL (SQLite in-memory for fast tests)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)

# Create test session factory
TestSessionLocal = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


# ============== EVENT LOOP ==============

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ============== DATABASE FIXTURES ==============

@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create database session for tests with isolated transaction."""
    # Create all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async with TestSessionLocal() as session:
        yield session

    # Drop all tables after test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# ============== HTTP CLIENT FIXTURES ==============

@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create async HTTP client for API tests."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def auth_client(client: AsyncClient, test_user: dict) -> AsyncGenerator[AsyncClient, None]:
    """Create authenticated HTTP client."""
    from src.lib.jwt import create_access_token

    token = create_access_token({"sub": str(test_user["id"])})
    client.headers["Authorization"] = f"Bearer {token}"
    yield client


# ============== FAKER FIXTURE ==============

@pytest.fixture(scope="session")
def faker() -> Faker:
    """Faker instance for generating fake data."""
    return fake


# ============== USER FIXTURES ==============

@pytest.fixture
def user_data(faker: Faker) -> dict:
    """Generate fake user registration data."""
    return {
        "email": faker.email(),
        "password": "Test@123456",
        "name": faker.name(),
    }


@pytest.fixture
def login_data(user_data: dict) -> dict:
    """Generate login credentials."""
    return {
        "email": user_data["email"],
        "password": user_data["password"],
    }


@pytest_asyncio.fixture(scope="function")
async def test_user(db_session: AsyncSession, user_data: dict) -> dict:
    """Create test user in database and return user data."""
    from src.repositories.auth.auth_repository import AuthRepository
    from src.lib.password import hash_password

    # Hash password
    hashed_password = hash_password(user_data["password"])

    # Create user via repository
    repo = AuthRepository(db_session)
    user = await repo.create({
        "email": user_data["email"],
        "password": hashed_password,
        "name": user_data["name"],
    })

    # Return user data with id
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
    }


# ============== COURSE FIXTURES ==============

@pytest.fixture
def course_data(faker: Faker) -> dict:
    """Generate fake course data."""
    return {
        "title": faker.sentence(nb_words=4),
        "description": faker.paragraph(),
        "category": faker.random_element(["programming", "design", "business", "marketing"]),
        "level": faker.random_element(["beginner", "intermediate", "advanced"]),
        "duration_hours": faker.random_int(min=5, max=50),
        "is_published": True,
    }


@pytest_asyncio.fixture(scope="function")
async def test_course(db_session: AsyncSession, course_data: dict, test_user: dict) -> dict:
    """Create test course in database."""
    from src.repositories.courses.course_repository import CourseRepository

    course_data["creator_id"] = test_user["id"]
    repo = CourseRepository(db_session)
    course = await repo.create(course_data)

    return {
        "id": course.id,
        "title": course.title,
        "creator_id": course.creator_id,
    }


# ============== LESSON FIXTURES ==============

@pytest.fixture
def lesson_data(faker: Faker) -> dict:
    """Generate fake lesson data."""
    return {
        "title": faker.sentence(nb_words=3),
        "content": faker.paragraph(nb_sentences=10),
        "video_url": faker.url(),
        "order": 1,
        "duration_minutes": faker.random_int(min=10, max=60),
    }


@pytest_asyncio.fixture(scope="function")
async def test_lesson(db_session: AsyncSession, lesson_data: dict, test_course: dict) -> dict:
    """Create test lesson in database."""
    from src.repositories.lessons.lesson_repository import LessonRepository

    lesson_data["course_id"] = test_course["id"]
    repo = LessonRepository(db_session)
    lesson = await repo.create(lesson_data)

    return {
        "id": lesson.id,
        "title": lesson.title,
        "course_id": lesson.course_id,
    }


# ============== QUIZ FIXTURES ==============

@pytest.fixture
def quiz_data(faker: Faker) -> dict:
    """Generate fake quiz data."""
    return {
        "title": faker.sentence(nb_words=4),
        "description": faker.paragraph(),
        "time_limit": faker.random_int(min=10, max=60),
        "passing_score": faker.random_int(min=50, max=80),
        "max_attempts": 3,
    }


@pytest.fixture
def question_data(faker: Faker) -> dict:
    """Generate fake question data."""
    return {
        "content": faker.sentence(),
        "type": "single_choice",
        "points": faker.random_int(min=1, max=5),
        "order": 1,
    }


@pytest.fixture
def answer_data(faker: Faker) -> list[dict]:
    """Generate fake answers data."""
    return [
        {"content": faker.sentence(), "is_correct": True, "order": 1},
        {"content": faker.sentence(), "is_correct": False, "order": 2},
        {"content": faker.sentence(), "is_correct": False, "order": 3},
        {"content": faker.sentence(), "is_correct": False, "order": 4},
    ]


# ============== CHAT FIXTURES ==============

@pytest.fixture
def conversation_data(faker: Faker, test_course: dict) -> dict:
    """Generate fake conversation data."""
    return {
        "title": faker.sentence(nb_words=3),
        "course_id": test_course["id"],
    }


@pytest.fixture
def message_data(faker: Faker) -> dict:
    """Generate fake message data."""
    return {
        "content": faker.sentence(),
        "role": "user",
    }


# ============== MOCK FIXTURES ==============

@pytest.fixture
def mock_ai_response(mocker):
    """Mock AI service response."""
    mock = mocker.patch("src.lib.ai.claude.ClaudeClient.generate")
    mock.return_value = "This is a mocked AI response."
    return mock


@pytest.fixture
def mock_email_service(mocker):
    """Mock email service."""
    mock = mocker.patch("src.lib.email.send_email")
    mock.return_value = True
    return mock


@pytest.fixture
def mock_redis(mocker):
    """Mock Redis cache."""
    mock = mocker.patch("src.lib.cache.redis_client")
    mock.get.return_value = None
    mock.set.return_value = True
    return mock


# ============== FREEZEGUN FIXTURES ==============

@pytest.fixture
def frozen_time(faker: Faker):
    """Freeze time for testing time-dependent code."""
    from freezegun import freeze_time

    frozen_date = faker.date_time()
    with freeze_time(frozen_date) as frozen:
        yield frozen
