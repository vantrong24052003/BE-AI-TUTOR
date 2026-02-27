"""
Integration Tests for Auth Flow.

End-to-end tests that verify complete user flows.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.slow
class TestAuthFlow:
    """End-to-end authentication flow tests."""

    async def test_complete_registration_and_login_flow(
        self,
        client: AsyncClient,
        user_data: dict,
    ):
        """Test complete flow: register -> login -> access protected route."""
        # Step 1: Register
        register_response = await client.post(
            "/api/v1/auth/register",
            json=user_data,
        )
        assert register_response.status_code == 201
        user = register_response.json()
        assert user["email"] == user_data["email"]

        # Step 2: Login
        login_response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": user_data["email"],
                "password": user_data["password"],
            },
        )
        assert login_response.status_code == 200
        token_data = login_response.json()
        assert "access_token" in token_data

        # Step 3: Access protected route
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        profile_response = await client.get(
            "/api/v1/auth/profile",
            headers=headers,
        )
        assert profile_response.status_code == 200
        profile = profile_response.json()
        assert profile["email"] == user_data["email"]

    async def test_registration_to_course_creation_flow(
        self,
        client: AsyncClient,
        user_data: dict,
        course_data: dict,
    ):
        """Test flow: register -> login -> create course -> verify."""
        # Register
        await client.post("/api/v1/auth/register", json=user_data)

        # Login
        login_response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": user_data["email"],
                "password": user_data["password"],
            },
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create course
        create_response = await client.post(
            "/api/v1/courses",
            json=course_data,
            headers=headers,
        )
        assert create_response.status_code == 201
        course = create_response.json()

        # Verify course exists
        get_response = await client.get(f"/api/v1/courses/{course['id']}")
        assert get_response.status_code == 200
        assert get_response.json()["title"] == course_data["title"]


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.slow
class TestCourseLearningFlow:
    """End-to-end course learning flow tests."""

    async def test_enroll_and_complete_lesson_flow(
        self,
        auth_client: AsyncClient,
        test_course: dict,
        test_lesson: dict,
    ):
        """Test flow: enroll -> view lesson -> mark complete -> check progress."""
        course_id = test_course["id"]
        lesson_id = test_lesson["id"]

        # Step 1: Enroll in course
        enroll_response = await auth_client.post(
            f"/api/v1/courses/{course_id}/enroll"
        )
        assert enroll_response.status_code in [200, 201]

        # Step 2: View lesson
        lesson_response = await auth_client.get(
            f"/api/v1/courses/{course_id}/lessons/{lesson_id}"
        )
        assert lesson_response.status_code == 200

        # Step 3: Mark lesson as complete
        complete_response = await auth_client.post(
            f"/api/v1/progress/lessons/{lesson_id}/complete"
        )
        assert complete_response.status_code in [200, 201]

        # Step 4: Check progress
        progress_response = await auth_client.get(
            f"/api/v1/progress/courses/{course_id}"
        )
        assert progress_response.status_code == 200
        progress = progress_response.json()
        assert progress["completed_lessons"] >= 1


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.slow
class TestQuizFlow:
    """End-to-end quiz flow tests."""

    async def test_take_quiz_flow(
        self,
        auth_client: AsyncClient,
        test_course: dict,
        test_lesson: dict,
        quiz_data: dict,
    ):
        """Test flow: create quiz -> take quiz -> view results."""
        course_id = test_course["id"]
        lesson_id = test_lesson["id"]

        # Create quiz (as course creator)
        quiz_data["lesson_id"] = lesson_id
        create_quiz_response = await auth_client.post(
            f"/api/v1/courses/{course_id}/lessons/{lesson_id}/quizzes",
            json=quiz_data,
        )
        assert create_quiz_response.status_code in [200, 201]
        quiz = create_quiz_response.json()

        # Take quiz
        submit_response = await auth_client.post(
            f"/api/v1/quizzes/{quiz['id']}/submit",
            json={"answers": []},  # Would have actual answers
        )
        assert submit_response.status_code in [200, 201]

        # View results
        results_response = await auth_client.get(
            f"/api/v1/quizzes/{quiz['id']}/results"
        )
        assert results_response.status_code == 200
