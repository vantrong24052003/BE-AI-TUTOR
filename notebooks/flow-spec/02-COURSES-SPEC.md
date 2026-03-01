# COURSES Feature Specification

> Chi tiết specification cho tính năng Course Management

---

## 1. TỔNG QUAN

### Mô tả
Hệ thống quản lý khóa học với các chức năng CRUD, enrollment, và tracking tiến độ.

### Business Rules
- Mọi user đều có thể tạo khóa học
- Khóa học mặc định là `draft` (chưa publish)
- Admin có thể publish/unpublish khóa học
- User có thể enroll vào khóa học đã published
- Một user chỉ có thể enroll 1 lần vào mỗi khóa học
- Creator của khóa học không thể enroll vào khóa của chính mình

---

## 2. DATA MODEL

### Course Fields

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Primary key |
| title | string | Tiêu đề khóa học (max 200 chars) |
| description | text | Mô tả chi tiết |
| thumbnail | string | URL hình ảnh |
| creator_id | integer | FK → users |
| category_id | integer | FK → categories |
| level | enum | beginner/intermediate/advanced |
| duration_hours | decimal | Tổng thời lượng (giờ) |
| is_published | boolean | Trạng thái publish |
| published_at | timestamp | Thời gian publish |
| created_at | timestamp | Thời gian tạo |
| updated_at | timestamp | Thời gian cập nhật |

### Enrollment Fields

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Primary key |
| user_id | integer | FK → users |
| course_id | integer | FK → courses |
| enrolled_at | timestamp | Thời gian đăng ký |
| completed_at | timestamp | Thời gian hoàn thành (nullable) |
| progress | decimal | Tiến độ 0-100 |

---

## 3. API ENDPOINTS

### 3.1 List Courses

**Endpoint**: `GET /api/v1/courses`

**Query Parameters**:
| Param | Type | Description |
|-------|------|-------------|
| page | int | Page number (default: 1) |
| limit | int | Items per page (default: 10, max: 50) |
| search | string | Search in title, description |
| category_id | int | Filter by category |
| level | string | Filter by level |
| creator_id | int | Filter by creator |

**Success Response** (200):
```json
{
  "courses": [
    {
      "id": 1,
      "title": "Python cơ bản",
      "description": "Khóa học Python cho người mới bắt đầu",
      "thumbnail": "https://example.com/thumb.jpg",
      "creator": {
        "id": 2,
        "name": "Nguyễn Văn A",
        "avatar": "https://..."
      },
      "category": {
        "id": 1,
        "name": "Lập trình",
        "slug": "programming"
      },
      "level": "beginner",
      "duration_hours": 20.5,
      "is_published": true,
      "is_enrolled": false,
      "progress": null,
      "lessons_count": 15,
      "enrolled_count": 150,
      "published_at": "2026-03-01T10:00:00Z"
    }
  ],
  "meta": {
    "total": 100,
    "page": 1,
    "limit": 10,
    "total_pages": 10
  }
}
```

---

### 3.2 Get Course Detail

**Endpoint**: `GET /api/v1/courses/:id`

**Success Response** (200):
```json
{
  "id": 1,
  "title": "Python cơ bản",
  "description": "Khóa học Python cho người mới bắt đầu...",
  "thumbnail": "https://example.com/thumb.jpg",
  "creator": {
    "id": 2,
    "name": "Nguyễn Văn A",
    "avatar": "https://..."
  },
  "category": {
    "id": 1,
    "name": "Lập trình",
    "slug": "programming"
  },
  "level": "beginner",
  "duration_hours": 20.5,
  "is_published": true,
  "is_enrolled": true,
  "progress": 35.5,
  "lessons_count": 15,
  "enrolled_count": 150,
  "lessons": [
    {
      "id": 1,
      "title": "Giới thiệu Python",
      "order": 1,
      "duration_minutes": 30,
      "is_completed": true
    },
    {
      "id": 2,
      "title": "Cài đặt môi trường",
      "order": 2,
      "duration_minutes": 45,
      "is_completed": true
    }
  ],
  "published_at": "2026-03-01T10:00:00Z",
  "created_at": "2026-02-15T10:00:00Z"
}
```

**Error Responses**:
- `404` - Course not found

---

### 3.3 Create Course

**Endpoint**: `POST /api/v1/courses`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "title": "Python cơ bản",
  "description": "Khóa học Python cho người mới bắt đầu",
  "thumbnail": "https://example.com/thumb.jpg",
  "category_id": 1,
  "level": "beginner",
  "duration_hours": 20.5
}
```

**Validation Rules**:
| Field | Rule |
|-------|------|
| title | Required, 5-200 chars |
| description | Required, min 50 chars |
| thumbnail | Optional, valid URL |
| category_id | Required, must exist |
| level | Required, one of: beginner/intermediate/advanced |
| duration_hours | Optional, positive number |

**Success Response** (201):
```json
{
  "message": "Course created successfully",
  "course": {
    "id": 1,
    "title": "Python cơ bản",
    "description": "Khóa học Python cho người mới bắt đầu",
    "thumbnail": "https://example.com/thumb.jpg",
    "creator_id": 2,
    "category_id": 1,
    "level": "beginner",
    "duration_hours": 20.5,
    "is_published": false,
    "created_at": "2026-03-01T10:00:00Z"
  }
}
```

---

### 3.4 Update Course

**Endpoint**: `PUT /api/v1/courses/:id`

**Headers**: `Authorization: Bearer <token>`

**Request Body**: Same as Create (all fields optional)

**Authorization**: Only creator or admin can update

**Success Response** (200):
```json
{
  "message": "Course updated successfully",
  "course": { ... }
}
```

**Error Responses**:
- `403` - Not authorized
- `404` - Course not found

---

### 3.5 Delete Course

**Endpoint**: `DELETE /api/v1/courses/:id`

**Headers**: `Authorization: Bearer <token>`

**Authorization**: Only creator or admin can delete

**Success Response** (200):
```json
{
  "message": "Course deleted successfully"
}
```

**Error Responses**:
- `403` - Not authorized
- `404` - Course not found
- `400` - Course has enrollments (cannot delete)

---

### 3.6 Enroll Course

**Endpoint**: `POST /api/v1/courses/:id/enroll`

**Headers**: `Authorization: Bearer <token>`

**Preconditions**:
- Course must be published
- User must not be the creator
- User must not already enrolled

**Success Response** (200):
```json
{
  "message": "Enrolled successfully",
  "enrollment": {
    "id": 1,
    "course_id": 1,
    "user_id": 5,
    "enrolled_at": "2026-03-01T10:00:00Z",
    "progress": 0
  }
}
```

**Error Responses**:
- `400` - Already enrolled
- `400` - Cannot enroll in own course
- `404` - Course not found
- `403` - Course not published

---

### 3.7 Get Course Progress

**Endpoint**: `GET /api/v1/courses/:id/progress`

**Headers**: `Authorization: Bearer <token>`

**Success Response** (200):
```json
{
  "course_id": 1,
  "progress": 35.5,
  "completed_lessons": 5,
  "total_lessons": 15,
  "lessons": [
    {
      "id": 1,
      "title": "Giới thiệu Python",
      "is_completed": true,
      "completed_at": "2026-03-01T10:30:00Z"
    },
    {
      "id": 2,
      "title": "Cài đặt môi trường",
      "is_completed": false,
      "completed_at": null
    }
  ]
}
```

**Error Responses**:
- `404` - Course not found or not enrolled

---

### 3.8 Get My Courses (Enrolled)

**Endpoint**: `GET /api/v1/courses/my-courses`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
| Param | Type | Description |
|-------|------|-------------|
| status | string | all/in_progress/completed |

**Success Response** (200):
```json
{
  "courses": [
    {
      "id": 1,
      "title": "Python cơ bản",
      "thumbnail": "https://...",
      "progress": 35.5,
      "enrolled_at": "2026-03-01T10:00:00Z",
      "lessons_completed": 5,
      "lessons_total": 15
    }
  ],
  "meta": {
    "total": 5,
    "in_progress": 3,
    "completed": 2
  }
}
```

---

### 3.9 Publish Course (Admin)

**Endpoint**: `POST /api/v1/courses/:id/publish`

**Headers**: `Authorization: Bearer <token>`

**Authorization**: Admin only

**Preconditions**:
- Course must have at least 1 lesson

**Success Response** (200):
```json
{
  "message": "Course published successfully",
  "course": {
    "id": 1,
    "is_published": true,
    "published_at": "2026-03-01T10:00:00Z"
  }
}
```

---

## 4. IMPLEMENTATION

### Controller

```python
# app/controllers/courses_controller.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.services.course_service import CourseService
from app.schemas.courses import (
    CourseCreate, CourseUpdate, CourseResponse, CourseListResponse,
    EnrollmentResponse, ProgressResponse
)
from app.dependencies import get_current_user, get_optional_user

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("", response_model=CourseListResponse)
async def list_courses(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    search: str | None = None,
    category_id: int | None = None,
    level: str | None = None,
    current_user = Depends(get_optional_user),
    service: CourseService = Depends()
):
    return await service.list_courses(
        page=page,
        limit=limit,
        search=search,
        category_id=category_id,
        level=level,
        user_id=current_user.id if current_user else None
    )

@router.get("/my-courses", response_model=CourseListResponse)
async def get_my_courses(
    status: str = Query("all", regex="^(all|in_progress|completed)$"),
    current_user = Depends(get_current_user),
    service: CourseService = Depends()
):
    return await service.get_user_courses(current_user.id, status)

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: int,
    current_user = Depends(get_optional_user),
    service: CourseService = Depends()
):
    return await service.get_course_detail(
        course_id,
        user_id=current_user.id if current_user else None
    )

@router.post("", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    request: CourseCreate,
    current_user = Depends(get_current_user),
    service: CourseService = Depends()
):
    return await service.create_course(current_user.id, request)

@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: int,
    request: CourseUpdate,
    current_user = Depends(get_current_user),
    service: CourseService = Depends()
):
    return await service.update_course(course_id, current_user.id, request)

@router.delete("/{course_id}")
async def delete_course(
    course_id: int,
    current_user = Depends(get_current_user),
    service: CourseService = Depends()
):
    return await service.delete_course(course_id, current_user.id)

@router.post("/{course_id}/enroll", response_model=EnrollmentResponse)
async def enroll_course(
    course_id: int,
    current_user = Depends(get_current_user),
    service: CourseService = Depends()
):
    return await service.enroll_course(course_id, current_user.id)

@router.get("/{course_id}/progress", response_model=ProgressResponse)
async def get_course_progress(
    course_id: int,
    current_user = Depends(get_current_user),
    service: CourseService = Depends()
):
    return await service.get_course_progress(course_id, current_user.id)

@router.post("/{course_id}/publish", response_model=CourseResponse)
async def publish_course(
    course_id: int,
    current_user = Depends(get_current_user),
    service: CourseService = Depends()
):
    return await service.publish_course(course_id, current_user.id)
```

### Service

```python
# app/services/course_service.py
from app.repositories.course_repository import CourseRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.lesson_repository import LessonRepository
from app.exceptions import NotFoundError, AuthorizationError, ValidationError

class CourseService:
    def __init__(
        self,
        course_repo: CourseRepository,
        enrollment_repo: EnrollmentRepository,
        lesson_repo: LessonRepository
    ):
        self.course_repo = course_repo
        self.enrollment_repo = enrollment_repo
        self.lesson_repo = lesson_repo

    async def list_courses(self, page: int, limit: int, search: str | None,
                           category_id: int | None, level: str | None,
                           user_id: int | None) -> dict:
        # Get published courses only
        courses, total = await self.course_repo.find_published(
            page=page,
            limit=limit,
            search=search,
            category_id=category_id,
            level=level
        )

        # Add enrollment info if user is logged in
        if user_id:
            enrolled_ids = await self.enrollment_repo.get_enrolled_course_ids(user_id)
            for course in courses:
                course["is_enrolled"] = course["id"] in enrolled_ids
                if course["is_enrolled"]:
                    enrollment = await self.enrollment_repo.get_by_user_and_course(
                        user_id, course["id"]
                    )
                    course["progress"] = enrollment.progress

        return {
            "courses": courses,
            "meta": {
                "total": total,
                "page": page,
                "limit": limit,
                "total_pages": (total + limit - 1) // limit
            }
        }

    async def get_course_detail(self, course_id: int, user_id: int | None) -> dict:
        course = await self.course_repo.get_by_id(course_id)
        if not course:
            raise NotFoundError("Course not found")

        # Get lessons
        lessons = await self.lesson_repo.get_by_course(course_id)
        course["lessons"] = lessons

        # Add enrollment info
        if user_id:
            enrollment = await self.enrollment_repo.get_by_user_and_course(
                user_id, course_id
            )
            course["is_enrolled"] = enrollment is not None
            course["progress"] = enrollment.progress if enrollment else None

            # Add completion status for each lesson
            if enrollment:
                completed_ids = await self.lesson_repo.get_completed_lesson_ids(
                    user_id, course_id
                )
                for lesson in lessons:
                    lesson["is_completed"] = lesson["id"] in completed_ids

        return course

    async def create_course(self, user_id: int, data: CourseCreate) -> dict:
        course = await self.course_repo.create({
            **data.dict(),
            "creator_id": user_id,
            "is_published": False
        })
        return course

    async def update_course(self, course_id: int, user_id: int,
                           data: CourseUpdate) -> dict:
        course = await self.course_repo.get_by_id(course_id)
        if not course:
            raise NotFoundError("Course not found")

        # Check authorization (creator or admin)
        user = await self.user_repo.get_by_id(user_id)
        if course["creator_id"] != user_id and user["role"] != "admin":
            raise AuthorizationError("Not authorized to update this course")

        updated = await self.course_repo.update(course_id, data.dict(exclude_unset=True))
        return updated

    async def delete_course(self, course_id: int, user_id: int) -> dict:
        course = await self.course_repo.get_by_id(course_id)
        if not course:
            raise NotFoundError("Course not found")

        user = await self.user_repo.get_by_id(user_id)
        if course["creator_id"] != user_id and user["role"] != "admin":
            raise AuthorizationError("Not authorized to delete this course")

        # Check if course has enrollments
        enrollment_count = await self.enrollment_repo.count_by_course(course_id)
        if enrollment_count > 0:
            raise ValidationError("Cannot delete course with existing enrollments")

        await self.course_repo.delete(course_id)
        return {"message": "Course deleted successfully"}

    async def enroll_course(self, course_id: int, user_id: int) -> dict:
        course = await self.course_repo.get_by_id(course_id)
        if not course:
            raise NotFoundError("Course not found")

        if not course["is_published"]:
            raise ValidationError("Course is not published")

        if course["creator_id"] == user_id:
            raise ValidationError("Cannot enroll in your own course")

        # Check existing enrollment
        existing = await self.enrollment_repo.get_by_user_and_course(user_id, course_id)
        if existing:
            raise ValidationError("Already enrolled in this course")

        enrollment = await self.enrollment_repo.create({
            "user_id": user_id,
            "course_id": course_id,
            "progress": 0
        })

        return enrollment

    async def get_course_progress(self, course_id: int, user_id: int) -> dict:
        enrollment = await self.enrollment_repo.get_by_user_and_course(user_id, course_id)
        if not enrollment:
            raise NotFoundError("Not enrolled in this course")

        lessons = await self.lesson_repo.get_by_course(course_id)
        completed_ids = await self.lesson_repo.get_completed_lesson_ids(user_id, course_id)

        lessons_with_status = [
            {
                "id": lesson["id"],
                "title": lesson["title"],
                "is_completed": lesson["id"] in completed_ids
            }
            for lesson in lessons
        ]

        return {
            "course_id": course_id,
            "progress": enrollment["progress"],
            "completed_lessons": len(completed_ids),
            "total_lessons": len(lessons),
            "lessons": lessons_with_status
        }

    async def publish_course(self, course_id: int, user_id: int) -> dict:
        user = await self.user_repo.get_by_id(user_id)
        if user["role"] != "admin":
            raise AuthorizationError("Only admins can publish courses")

        course = await self.course_repo.get_by_id(course_id)
        if not course:
            raise NotFoundError("Course not found")

        # Check minimum requirements
        lesson_count = await self.lesson_repo.count_by_course(course_id)
        if lesson_count == 0:
            raise ValidationError("Course must have at least 1 lesson")

        updated = await self.course_repo.update(course_id, {
            "is_published": True,
            "published_at": datetime.utcnow()
        })

        return updated
```

---

## 5. DATABASE SCHEMA

```sql
-- courses table
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    thumbnail VARCHAR(500),
    creator_id INTEGER NOT NULL REFERENCES users(id),
    category_id INTEGER NOT NULL REFERENCES categories(id),
    level VARCHAR(20) NOT NULL CHECK (level IN ('beginner', 'intermediate', 'advanced')),
    duration_hours DECIMAL(5,2),
    is_published BOOLEAN DEFAULT FALSE,
    published_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- enrollments table
CREATE TABLE enrollments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    course_id INTEGER NOT NULL REFERENCES courses(id),
    enrolled_at TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP,
    progress DECIMAL(5,2) DEFAULT 0,
    UNIQUE(user_id, course_id)
);

-- Indexes
CREATE INDEX idx_courses_category ON courses(category_id);
CREATE INDEX idx_courses_creator ON courses(creator_id);
CREATE INDEX idx_courses_published ON courses(is_published);
CREATE INDEX idx_enrollments_user ON enrollments(user_id);
CREATE INDEX idx_enrollments_course ON enrollments(course_id);
```

---

## 6. TESTS

```python
# tests/integration/test_courses_api.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
class TestCoursesAPI:
    async def test_list_courses(self, client: AsyncClient, published_course):
        response = await client.get("/api/v1/courses")
        assert response.status_code == 200
        data = response.json()
        assert len(data["courses"]) > 0
        assert "meta" in data

    async def test_get_course_detail(self, client: AsyncClient, published_course):
        response = await client.get(f"/api/v1/courses/{published_course.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == published_course.id

    async def test_create_course(self, client: AsyncClient, auth_header, category):
        response = await client.post("/api/v1/courses", headers=auth_header, json={
            "title": "New Course",
            "description": "A" * 50,  # min 50 chars
            "category_id": category.id,
            "level": "beginner"
        })
        assert response.status_code == 201

    async def test_enroll_course(self, client: AsyncClient, auth_header, published_course):
        response = await client.post(
            f"/api/v1/courses/{published_course.id}/enroll",
            headers=auth_header
        )
        assert response.status_code == 200

    async def test_enroll_own_course_fails(self, client: AsyncClient, auth_header, own_course):
        response = await client.post(
            f"/api/v1/courses/{own_course.id}/enroll",
            headers=auth_header
        )
        assert response.status_code == 400

    async def test_double_enroll_fails(self, client: AsyncClient, auth_header, published_course):
        # First enrollment
        await client.post(f"/api/v1/courses/{published_course.id}/enroll", headers=auth_header)

        # Second enrollment
        response = await client.post(
            f"/api/v1/courses/{published_course.id}/enroll",
            headers=auth_header
        )
        assert response.status_code == 400
```

---

*Version: 1.0 - Updated: 2026-03-01*
