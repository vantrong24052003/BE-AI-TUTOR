# ADMIN Feature Specification

> Chi tiết specification cho tính năng Admin Panel

---

## 1. TỔNG QUAN

### Mô tả
Admin dashboard với các chức năng quản lý:
- User management
- Category management
- Course moderation
- System statistics

### Business Rules
- Chỉ admin role mới có quyền truy cập
- Admin có thể xem/edit tất cả data
- Actions được log lại trong activity log

---

## 2. API ENDPOINTS

### 2.1 Admin Dashboard Stats

**Endpoint**: `GET /api/v1/admin/stats`

**Headers**: `Authorization: Bearer <token>`

**Authorization**: Admin only

**Success Response** (200):
```json
{
  "overview": {
    "total_users": 1250,
    "new_users_today": 15,
    "total_courses": 45,
    "published_courses": 32,
    "total_enrollments": 3500,
    "enrollments_today": 25
  },
  "charts": {
    "user_growth": [
      {"date": "2026-02-25", "count": 1200},
      {"date": "2026-02-26", "count": 1220},
      {"date": "2026-02-27", "count": 1235},
      {"date": "2026-02-28", "count": 1245},
      {"date": "2026-03-01", "count": 1250}
    ],
    "enrollment_growth": [
      {"date": "2026-02-25", "count": 3400},
      {"date": "2026-02-26", "count": 3420},
      {"date": "2026-02-27", "count": 3450},
      {"date": "2026-02-28", "count": 3475},
      {"date": "2026-03-01", "count": 3500}
    ]
  },
  "top_courses": [
    {
      "id": 1,
      "title": "Python Basics",
      "enrolled_count": 450,
      "completion_rate": 65.5
    }
  ],
  "recent_activities": [
    {
      "type": "user_registered",
      "user": "john@example.com",
      "timestamp": "2026-03-01T10:00:00Z"
    }
  ]
}
```

---

### 2.2 List Users

**Endpoint**: `GET /api/v1/admin/users`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
| Param | Type | Description |
|-------|------|-------------|
| search | string | Search by email/name |
| role | string | Filter by role |
| page | int | Page number |
| limit | int | Items per page |

**Success Response** (200):
```json
{
  "users": [
    {
      "id": 1,
      "email": "user@example.com",
      "name": "John Doe",
      "role": "user",
      "avatar": "https://...",
      "courses_created": 2,
      "courses_enrolled": 5,
      "created_at": "2026-01-15T10:00:00Z",
      "last_active": "2026-03-01T09:00:00Z"
    }
  ],
  "meta": {
    "total": 1250,
    "page": 1,
    "limit": 20
  }
}
```

---

### 2.3 Get User Detail (Admin)

**Endpoint**: `GET /api/v1/admin/users/:id`

**Headers**: `Authorization: Bearer <token>`

**Success Response** (200):
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user",
    "avatar": "https://...",
    "created_at": "2026-01-15T10:00:00Z",
    "last_active": "2026-03-01T09:00:00Z",
    "stats": {
      "courses_created": 2,
      "courses_enrolled": 5,
      "lessons_completed": 45,
      "quizzes_taken": 15,
      "flashcards_reviewed": 200
    },
    "enrollments": [...],
    "created_courses": [...]
  }
}
```

---

### 2.4 Update User Role

**Endpoint**: `PUT /api/v1/admin/users/:id/role`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "role": "admin"
}
```

**Success Response** (200):
```json
{
  "message": "User role updated",
  "user": { ... }
}
```

---

### 2.5 List Categories (Admin)

**Endpoint**: `GET /api/v1/admin/categories`

**Headers**: `Authorization: Bearer <token>`

**Success Response** (200):
```json
{
  "categories": [
    {
      "id": 1,
      "name": "Programming",
      "slug": "programming",
      "description": "Programming courses",
      "courses_count": 15,
      "created_at": "2026-01-01T00:00:00Z"
    }
  ]
}
```

---

### 2.6 Create Category

**Endpoint**: `POST /api/v1/admin/categories`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "name": "Data Science",
  "description": "Data science and machine learning courses"
}
```

**Success Response** (201):
```json
{
  "message": "Category created",
  "category": {
    "id": 5,
    "name": "Data Science",
    "slug": "data-science",
    "description": "Data science and machine learning courses",
    "created_at": "2026-03-01T10:00:00Z"
  }
}
```

---

### 2.7 Update Category

**Endpoint**: `PUT /api/v1/admin/categories/:id`

**Headers**: `Authorization: Bearer <token>`

**Request Body**: Same as Create

---

### 2.8 Delete Category

**Endpoint**: `DELETE /api/v1/admin/categories/:id`

**Headers**: `Authorization: Bearer <token>`

**Preconditions**: Category must have no courses

**Error Response** (400):
```json
{
  "error": "Cannot delete category with existing courses",
  "courses_count": 5
}
```

---

### 2.9 List All Courses (Admin)

**Endpoint**: `GET /api/v1/admin/courses`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
| Param | Type | Description |
|-------|------|-------------|
| status | string | all/published/draft/pending |
| search | string | Search by title |
| category_id | int | Filter by category |

**Success Response** (200):
```json
{
  "courses": [
    {
      "id": 1,
      "title": "Python Basics",
      "status": "published",
      "creator": {
        "id": 5,
        "name": "John Doe",
        "email": "john@example.com"
      },
      "category": {
        "id": 1,
        "name": "Programming"
      },
      "enrolled_count": 150,
      "lessons_count": 20,
      "created_at": "2026-02-01T10:00:00Z",
      "published_at": "2026-02-05T10:00:00Z"
    }
  ]
}
```

---

### 2.10 Publish/Unpublish Course

**Endpoint**: `POST /api/v1/admin/courses/:id/publish`

**Endpoint**: `POST /api/v1/admin/courses/:id/unpublish`

**Headers**: `Authorization: Bearer <token>`

**Success Response** (200):
```json
{
  "message": "Course published",
  "course": { ... }
}
```

---

## 3. IMPLEMENTATION

### Admin Middleware

```python
# app/middleware/admin_required.py
from fastapi import Depends, HTTPException
from app.dependencies import get_current_user

async def admin_required(current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
```

### Service

```python
# app/services/admin_service.py
from datetime import datetime, timedelta
from sqlalchemy import func
from app.repositories.user_repository import UserRepository
from app.repositories.course_repository import CourseRepository
from app.repositories.enrollment_repository import EnrollmentRepository

class AdminService:
    def __init__(
        self,
        user_repo: UserRepository,
        course_repo: CourseRepository,
        enrollment_repo: EnrollmentRepository
    ):
        self.user_repo = user_repo
        self.course_repo = course_repo
        self.enrollment_repo = enrollment_repo

    async def get_dashboard_stats(self) -> dict:
        # Get totals
        total_users = await self.user_repo.count()
        total_courses = await self.course_repo.count()
        published_courses = await self.course_repo.count_published()
        total_enrollments = await self.enrollment_repo.count()

        # Get today's stats
        today = datetime.utcnow().date()
        new_users_today = await self.user_repo.count_created_today(today)
        enrollments_today = await self.enrollment_repo.count_created_today(today)

        # Get growth data (last 7 days)
        user_growth = await self.user_repo.get_growth_data(days=7)
        enrollment_growth = await self.enrollment_repo.get_growth_data(days=7)

        # Get top courses
        top_courses = await self.course_repo.get_top_enrolled(limit=5)

        # Get recent activities
        recent_activities = await self.activity_repo.get_recent(limit=10)

        return {
            "overview": {
                "total_users": total_users,
                "new_users_today": new_users_today,
                "total_courses": total_courses,
                "published_courses": published_courses,
                "total_enrollments": total_enrollments,
                "enrollments_today": enrollments_today
            },
            "charts": {
                "user_growth": user_growth,
                "enrollment_growth": enrollment_growth
            },
            "top_courses": top_courses,
            "recent_activities": recent_activities
        }

    async def update_user_role(self, user_id: int, role: str) -> dict:
        if role not in ["user", "admin"]:
            raise ValidationError("Invalid role")

        user = await self.user_repo.update(user_id, {"role": role})

        # Log action
        await self.activity_repo.create({
            "action": "user_role_updated",
            "target_user_id": user_id,
            "new_role": role
        })

        return user
```

---

## 4. DATABASE SCHEMA

```sql
-- categories table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_categories_slug ON categories(slug);
```

---

## 5. TESTS

```python
# tests/integration/test_admin_api.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
class TestAdminAPI:
    async def test_admin_stats_requires_admin(self, client: AsyncClient, user_auth_header):
        response = await client.get("/api/v1/admin/stats", headers=user_auth_header)
        assert response.status_code == 403

    async def test_admin_stats(self, client: AsyncClient, admin_auth_header):
        response = await client.get("/api/v1/admin/stats", headers=admin_auth_header)
        assert response.status_code == 200
        data = response.json()
        assert "overview" in data
        assert "total_users" in data["overview"]

    async def test_list_users(self, client: AsyncClient, admin_auth_header):
        response = await client.get("/api/v1/admin/users", headers=admin_auth_header)
        assert response.status_code == 200
        data = response.json()
        assert "users" in data

    async def test_update_user_role(self, client: AsyncClient, admin_auth_header, user):
        response = await client.put(
            f"/api/v1/admin/users/{user.id}/role",
            headers=admin_auth_header,
            json={"role": "admin"}
        )
        assert response.status_code == 200

    async def test_create_category(self, client: AsyncClient, admin_auth_header):
        response = await client.post(
            "/api/v1/admin/categories",
            headers=admin_auth_header,
            json={"name": "New Category", "description": "Description"}
        )
        assert response.status_code == 201
```

---

*Version: 1.0 - Updated: 2026-03-01*
