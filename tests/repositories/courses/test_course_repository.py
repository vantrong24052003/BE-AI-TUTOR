"""
Tests for CourseRepository.

Unit tests for data access layer using in-memory SQLite.
"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.courses.course_repository import CourseRepository
from tests.factories import CourseFactory


@pytest.mark.asyncio
@pytest.mark.unit
class TestCourseRepository:
    """Tests for CourseRepository data access."""

    async def test_create_course(
        self,
        db_session: AsyncSession,
        test_user: dict,
    ):
        """Test creating a course in database."""
        repo = CourseRepository(db_session)

        course_data = {
            "title": "Test Course",
            "description": "Test Description",
            "creator_id": test_user["id"],
            "category": "programming",
            "level": "beginner",
        }

        course = await repo.create(course_data)

        assert course.id is not None
        assert course.title == course_data["title"]
        assert course.creator_id == test_user["id"]

    async def test_get_by_id(
        self,
        db_session: AsyncSession,
        test_course: dict,
    ):
        """Test getting course by ID."""
        repo = CourseRepository(db_session)

        course = await repo.get_by_id(test_course["id"])

        assert course is not None
        assert course.id == test_course["id"]

    async def test_get_by_id_not_found(
        self,
        db_session: AsyncSession,
    ):
        """Test getting nonexistent course returns None."""
        repo = CourseRepository(db_session)

        course = await repo.get_by_id(99999)

        assert course is None

    async def test_get_all(
        self,
        db_session: AsyncSession,
        test_course: dict,
    ):
        """Test getting all courses."""
        repo = CourseRepository(db_session)

        courses = await repo.get_all(skip=0, limit=10)

        assert len(courses) >= 1

    async def test_get_by_creator(
        self,
        db_session: AsyncSession,
        test_course: dict,
        test_user: dict,
    ):
        """Test getting courses by creator ID."""
        repo = CourseRepository(db_session)

        courses = await repo.get_by_creator(test_user["id"])

        assert len(courses) >= 1
        assert all(c.creator_id == test_user["id"] for c in courses)

    async def test_update_course(
        self,
        db_session: AsyncSession,
        test_course: dict,
    ):
        """Test updating a course."""
        repo = CourseRepository(db_session)

        updated = await repo.update(test_course["id"], {"title": "Updated Title"})

        assert updated.title == "Updated Title"

    async def test_delete_course(
        self,
        db_session: AsyncSession,
        test_course: dict,
    ):
        """Test deleting a course."""
        repo = CourseRepository(db_session)

        await repo.delete(test_course["id"])

        # Verify deleted
        course = await repo.get_by_id(test_course["id"])
        assert course is None

    async def test_filter_by_category(
        self,
        db_session: AsyncSession,
        test_course: dict,
    ):
        """Test filtering courses by category."""
        repo = CourseRepository(db_session)

        courses = await repo.filter(category="programming")

        assert all(c.category == "programming" for c in courses)

    async def test_filter_by_level(
        self,
        db_session: AsyncSession,
        test_course: dict,
    ):
        """Test filtering courses by level."""
        repo = CourseRepository(db_session)

        courses = await repo.filter(level="beginner")

        assert all(c.level == "beginner" for c in courses)

    async def test_count(
        self,
        db_session: AsyncSession,
        test_course: dict,
    ):
        """Test counting courses."""
        repo = CourseRepository(db_session)

        count = await repo.count()

        assert count >= 1
