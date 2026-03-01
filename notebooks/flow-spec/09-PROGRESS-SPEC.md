# PROGRESS Feature Specification

> Chi tiết specification cho tính năng Learning Progress Tracking

---

## 1. TỔNG QUAN

### Mô tả
Theo dõi tiến độ học tập của user, bao gồm:
- Tiến độ từng khóa học
- Thống kê học tập tổng quan
- Activity timeline
- Achievements/badges (future)

### Business Rules
- Progress được tính dựa trên lessons completed
- Progress cập nhật real-time khi hoàn thành lesson
- Thống kê được aggregate hàng ngày
- Lưu history để vẽ biểu đồ

---

## 2. API ENDPOINTS

### 2.1 Get User Progress Overview

**Endpoint**: `GET /api/v1/progress`

**Headers**: `Authorization: Bearer <token>`

**Success Response** (200):
```json
{
  "overview": {
    "total_courses_enrolled": 5,
    "courses_completed": 2,
    "courses_in_progress": 3,
    "total_lessons_completed": 45,
    "total_time_spent_minutes": 1200,
    "current_streak_days": 7,
    "longest_streak_days": 14
  },
  "recent_activity": [
    {
      "type": "lesson_completed",
      "lesson": {
        "id": 1,
        "title": "Variables in Python",
        "course": {
          "id": 1,
          "title": "Python Basics"
        }
      },
      "completed_at": "2026-03-01T10:00:00Z"
    }
  ],
  "achievements": [
    {
      "id": "first_course",
      "name": "First Steps",
      "description": "Complete your first course",
      "earned_at": "2026-02-15T10:00:00Z"
    }
  ]
}
```

---

### 2.2 Get Course Progress

**Endpoint**: `GET /api/v1/progress/courses/:course_id`

**Headers**: `Authorization: Bearer <token>`

**Success Response** (200):
```json
{
  "course_id": 1,
  "course_title": "Python Basics",
  "progress": 65.5,
  "enrolled_at": "2026-02-01T10:00:00Z",
  "estimated_completion": "2026-03-15T00:00:00Z",
  "stats": {
    "lessons_total": 20,
    "lessons_completed": 13,
    "lessons_remaining": 7,
    "time_spent_minutes": 450,
    "quizzes_taken": 5,
    "average_quiz_score": 85
  },
  "modules": [
    {
      "id": 1,
      "title": "Introduction",
      "progress": 100,
      "lessons_completed": 5,
      "lessons_total": 5
    },
    {
      "id": 2,
      "title": "Variables & Data Types",
      "progress": 60,
      "lessons_completed": 3,
      "lessons_total": 5
    }
  ],
  "timeline": [
    {
      "date": "2026-03-01",
      "lessons_completed": 2,
      "time_spent_minutes": 45
    }
  ]
}
```

---

### 2.3 Get Learning Statistics

**Endpoint**: `GET /api/v1/progress/statistics`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
| Param | Type | Description |
|-------|------|-------------|
| period | string | week/month/year (default: month) |

**Success Response** (200):
```json
{
  "period": "month",
  "start_date": "2026-02-01",
  "end_date": "2026-03-01",
  "statistics": {
    "total_time_minutes": 1200,
    "lessons_completed": 45,
    "courses_completed": 2,
    "quizzes_taken": 15,
    "average_quiz_score": 82.5,
    "flashcards_reviewed": 200,
    "exercises_submitted": 10
  },
  "daily_breakdown": [
    {
      "date": "2026-02-28",
      "time_minutes": 45,
      "lessons": 2,
      "quizzes": 1
    },
    {
      "date": "2026-03-01",
      "time_minutes": 60,
      "lessons": 3,
      "quizzes": 0
    }
  ],
  "comparison": {
    "vs_last_period": {
      "time_change_percent": 15,
      "lessons_change_percent": 20
    }
  }
}
```

---

### 2.4 Get Streak Information

**Endpoint**: `GET /api/v1/progress/streak`

**Headers**: `Authorization: Bearer <token>`

**Success Response** (200):
```json
{
  "current_streak": 7,
  "longest_streak": 14,
  "streak_start": "2026-02-23",
  "last_activity": "2026-03-01",
  "streak_calendar": [
    {"date": "2026-02-23", "active": true},
    {"date": "2026-02-24", "active": true},
    {"date": "2026-02-25", "active": false},
    {"date": "2026-02-26", "active": true}
  ],
  "motivation": "Keep going! You're on a 7-day streak!"
}
```

---

## 3. IMPLEMENTATION

### Service

```python
# app/services/progress_service.py
from datetime import datetime, timedelta
from sqlalchemy import func
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.progress_repository import ProgressRepository
from app.repositories.activity_repository import ActivityRepository

class ProgressService:
    def __init__(
        self,
        enrollment_repo: EnrollmentRepository,
        progress_repo: ProgressRepository,
        activity_repo: ActivityRepository
    ):
        self.enrollment_repo = enrollment_repo
        self.progress_repo = progress_repo
        self.activity_repo = activity_repo

    async def get_user_overview(self, user_id: int) -> dict:
        # Get enrollment stats
        enrollments = await self.enrollment_repo.get_by_user(user_id)

        total_courses = len(enrollments)
        completed_courses = sum(1 for e in enrollments if e["progress"] >= 100)
        in_progress = total_courses - completed_courses

        # Get lesson stats
        lessons_completed = await self.progress_repo.count_completed_lessons(user_id)

        # Get time spent
        time_spent = await self.activity_repo.get_total_time(user_id)

        # Get streak
        streak = await self._calculate_streak(user_id)

        # Get recent activity
        recent = await self.activity_repo.get_recent(user_id, limit=10)

        return {
            "overview": {
                "total_courses_enrolled": total_courses,
                "courses_completed": completed_courses,
                "courses_in_progress": in_progress,
                "total_lessons_completed": lessons_completed,
                "total_time_spent_minutes": time_spent,
                "current_streak_days": streak["current"],
                "longest_streak_days": streak["longest"]
            },
            "recent_activity": recent
        }

    async def get_course_progress(self, user_id: int, course_id: int) -> dict:
        enrollment = await self.enrollment_repo.get_by_user_and_course(user_id, course_id)
        if not enrollment:
            raise NotFoundError("Not enrolled in this course")

        # Get lessons with completion status
        lessons = await self.progress_repo.get_lessons_with_status(user_id, course_id)

        completed = [l for l in lessons if l["is_completed"]]
        total = len(lessons)
        progress = (len(completed) / total * 100) if total > 0 else 0

        # Get quiz stats
        quiz_stats = await self._get_quiz_stats(user_id, course_id)

        # Get timeline
        timeline = await self.activity_repo.get_course_timeline(user_id, course_id)

        return {
            "course_id": course_id,
            "progress": round(progress, 2),
            "enrolled_at": enrollment["enrolled_at"],
            "stats": {
                "lessons_total": total,
                "lessons_completed": len(completed),
                "lessons_remaining": total - len(completed),
                "time_spent_minutes": enrollment.get("time_spent", 0),
                "quizzes_taken": quiz_stats["taken"],
                "average_quiz_score": quiz_stats["average"]
            },
            "lessons": lessons,
            "timeline": timeline
        }

    async def _calculate_streak(self, user_id: int) -> dict:
        """Calculate current and longest streak."""
        activities = await self.activity_repo.get_daily_activity(user_id)

        if not activities:
            return {"current": 0, "longest": 0}

        # Group by date
        dates = set(a["date"] for a in activities)

        current_streak = 0
        longest_streak = 0
        temp_streak = 0

        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        # Sort dates
        sorted_dates = sorted(dates, reverse=True)

        for i, date in enumerate(sorted_dates):
            if i == 0:
                # First date should be today or yesterday to count current streak
                if date in [today, yesterday]:
                    temp_streak = 1
                    current_streak = 1
            else:
                # Check if consecutive
                prev_date = sorted_dates[i - 1]
                if (prev_date - date).days == 1:
                    temp_streak += 1
                    if temp_streak > longest_streak:
                        longest_streak = temp_streak
                else:
                    temp_streak = 1

        if temp_streak > longest_streak:
            longest_streak = temp_streak

        return {
            "current": current_streak,
            "longest": longest_streak
        }

    async def record_activity(self, user_id: int, activity_type: str,
                             data: dict) -> None:
        """Record user activity for progress tracking."""
        await self.activity_repo.create({
            "user_id": user_id,
            "activity_type": activity_type,
            "data": data,
            "created_at": datetime.utcnow()
        })
```

---

## 4. DATABASE SCHEMA

```sql
-- user_progress table (already defined in lessons spec)
-- Used for lesson completion tracking

-- activity_logs table
CREATE TABLE activity_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    activity_type VARCHAR(50) NOT NULL,
    data JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_activity_logs_user ON activity_logs(user_id);
CREATE INDEX idx_activity_logs_type ON activity_logs(activity_type);
CREATE INDEX idx_activity_logs_created ON activity_logs(created_at);

-- Materialized view for daily stats (refreshed daily)
CREATE MATERIALIZED VIEW daily_user_stats AS
SELECT
    user_id,
    DATE(created_at) as date,
    COUNT(*) FILTER (WHERE activity_type = 'lesson_completed') as lessons_completed,
    COUNT(*) FILTER (WHERE activity_type = 'quiz_completed') as quizzes_completed,
    SUM((data->>'time_spent')::int) FILTER (WHERE activity_type = 'time_spent') as time_minutes
FROM activity_logs
GROUP BY user_id, DATE(created_at);
```

---

## 5. SCHEDULED JOBS

### Daily Stats Aggregation

```python
# app/jobs/stats_aggregation.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler

async def aggregate_daily_stats():
    """Run daily to aggregate user statistics."""
    # Refresh materialized view
    await database.execute("REFRESH MATERIALIZED VIEW daily_user_stats")

    # Update user progress summaries
    users = await user_repo.get_all_active()
    for user in users:
        await update_user_summary(user.id)

scheduler = AsyncIOScheduler()
scheduler.add_job(aggregate_daily_stats, 'cron', hour=0, minute=5)
```

---

## 6. TESTS

```python
# tests/integration/test_progress_api.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
class TestProgressAPI:
    async def test_get_overview(self, client: AsyncClient, auth_header, user_with_activity):
        response = await client.get("/api/v1/progress", headers=auth_header)
        assert response.status_code == 200
        data = response.json()
        assert "overview" in data
        assert "total_courses_enrolled" in data["overview"]

    async def test_get_course_progress(self, client: AsyncClient, auth_header, enrolled_user):
        response = await client.get(
            f"/api/v1/progress/courses/{enrolled_user.course_id}",
            headers=auth_header
        )
        assert response.status_code == 200
        data = response.json()
        assert "progress" in data
        assert 0 <= data["progress"] <= 100

    async def test_streak_calculation(self, client: AsyncClient, auth_header, user_with_streak):
        response = await client.get("/api/v1/progress/streak", headers=auth_header)
        assert response.status_code == 200
        data = response.json()
        assert "current_streak" in data
        assert "longest_streak" in data
```

---

*Version: 1.0 - Updated: 2026-03-01*
