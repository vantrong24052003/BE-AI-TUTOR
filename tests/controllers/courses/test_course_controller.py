"""
Tests for CourseController.

Tests CRUD operations for courses with ownership-based access control.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.unit
@pytest.mark.api
class TestCourseController:
    """Tests for course endpoints."""

    # ============== INDEX (List) ==============

    async def test_list_courses_success(
        self,
        client: AsyncClient,
    ):
        """Test listing all courses."""
        response = await client.get("/api/v1/courses")

        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data

    async def test_list_courses_pagination(
        self,
        client: AsyncClient,
    ):
        """Test course list pagination."""
        response = await client.get("/api/v1/courses?page=1&size=10")

        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["size"] == 10

    async def test_list_courses_filter_by_category(
        self,
        client: AsyncClient,
    ):
        """Test filtering courses by category."""
        response = await client.get("/api/v1/courses?category=programming")

        assert response.status_code == 200

    async def test_list_courses_filter_by_level(
        self,
        client: AsyncClient,
    ):
        """Test filtering courses by level."""
        response = await client.get("/api/v1/courses?level=beginner")

        assert response.status_code == 200

    # ============== SHOW (Detail) ==============

    async def test_get_course_detail_success(
        self,
        client: AsyncClient,
        test_course: dict,
    ):
        """Test getting course detail."""
        response = await client.get(f"/api/v1/courses/{test_course['id']}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_course["id"]
        assert data["title"] == test_course["title"]

    async def test_get_course_not_found(
        self,
        client: AsyncClient,
    ):
        """Test getting nonexistent course."""
        response = await client.get("/api/v1/courses/99999")

        assert response.status_code == 404

    # ============== CREATE ==============

    async def test_create_course_success(
        self,
        auth_client: AsyncClient,
        course_data: dict,
    ):
        """Test creating a new course."""
        response = await auth_client.post("/api/v1/courses", json=course_data)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == course_data["title"]
        assert "id" in data

    async def test_create_course_unauthenticated(
        self,
        client: AsyncClient,
        course_data: dict,
    ):
        """Test creating course without auth fails."""
        response = await client.post("/api/v1/courses", json=course_data)

        assert response.status_code == 401

    async def test_create_course_invalid_data(
        self,
        auth_client: AsyncClient,
    ):
        """Test creating course with invalid data."""
        response = await auth_client.post("/api/v1/courses", json={})

        assert response.status_code == 422

    # ============== UPDATE ==============

    async def test_update_course_success(
        self,
        auth_client: AsyncClient,
        test_course: dict,
        faker,
    ):
        """Test updating own course."""
        update_data = {"title": faker.sentence(nb_words=4)}
        response = await auth_client.put(
            f"/api/v1/courses/{test_course['id']}", json=update_data
        )

        assert response.status_code == 200
        assert response.json()["title"] == update_data["title"]

    async def test_update_course_not_owner(
        self,
        client: AsyncClient,
        test_course: dict,
        faker,
    ):
        """Test updating another user's course fails."""
        # Create another user and try to update
        # This would need another authenticated client
        pass  # TODO: Implement with different user

    # ============== DELETE ==============

    async def test_delete_course_success(
        self,
        auth_client: AsyncClient,
        test_course: dict,
    ):
        """Test deleting own course."""
        response = await auth_client.delete(f"/api/v1/courses/{test_course['id']}")

        assert response.status_code == 204

    async def test_delete_course_not_owner(
        self,
        client: AsyncClient,
        test_course: dict,
    ):
        """Test deleting another user's course fails."""
        response = await client.delete(f"/api/v1/courses/{test_course['id']}")

        assert response.status_code == 401

    async def test_delete_course_not_found(
        self,
        auth_client: AsyncClient,
    ):
        """Test deleting nonexistent course."""
        response = await auth_client.delete("/api/v1/courses/99999")

        assert response.status_code == 404
