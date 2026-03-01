# BE AI TUTOR - Code Structure

> Chi tiết cấu trúc code Backend FastAPI
>
> **Version**: 3.0 - 75 APIs, 21 Tables

---

## 📁 Project Structure

```
BE-AI-TUTOR/
│
├── src/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   │
│   ├── controllers/               # HTTP handlers (15 controllers)
│   │   ├── __init__.py
│   │   ├── auth_controller.py     # 8 endpoints
│   │   ├── user_controller.py     # 4 endpoints
│   │   ├── category_controller.py # 4 endpoints
│   │   ├── course_controller.py   # 6 endpoints
│   │   ├── lesson_controller.py   # 5 endpoints
│   │   ├── quiz_controller.py     # 7 endpoints
│   │   ├── exercise_controller.py # 8 endpoints
│   │   ├── flashcard_controller.py # 7 endpoints
│   │   ├── note_controller.py     # 4 endpoints
│   │   ├── bookmark_controller.py # 3 endpoints
│   │   ├── chat_ai_controller.py  # 6 endpoints
│   │   ├── ai_service_controller.py # 5 endpoints
│   │   ├── learning_progress_controller.py # 3 endpoints
│   │   ├── document_controller.py # 4 endpoints
│   │   └── admin_controller.py    # 1 endpoint
│   │
│   ├── services/                  # Business logic layer (15 services)
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── category_service.py
│   │   ├── course_service.py
│   │   ├── lesson_service.py
│   │   ├── quiz_service.py
│   │   ├── exercise_service.py
│   │   ├── flashcard_service.py
│   │   ├── note_service.py
│   │   ├── bookmark_service.py
│   │   ├── chat_ai_service.py
│   │   ├── ai_service.py          # AI integration (Claude/OpenAI)
│   │   ├── learning_progress_service.py
│   │   ├── document_service.py
│   │   └── admin_service.py
│   │
│   ├── repositories/              # Data access layer
│   │   ├── __init__.py
│   │   ├── base_repository.py
│   │   ├── user_repository.py
│   │   ├── category_repository.py
│   │   ├── course_repository.py
│   │   ├── lesson_repository.py
│   │   ├── quiz_repository.py
│   │   ├── exercise_repository.py
│   │   ├── flashcard_repository.py
│   │   ├── note_repository.py
│   │   ├── bookmark_repository.py
│   │   ├── conversation_repository.py
│   │   ├── message_repository.py
│   │   └── learning_progress_repository.py
│   │
│   ├── models/                    # SQLAlchemy ORM models (21 models)
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── course.py
│   │   ├── lesson.py
│   │   ├── enrollment.py
│   │   ├── quiz.py
│   │   ├── question.py
│   │   ├── answer.py
│   │   ├── quiz_attempt.py
│   │   ├── exercise.py
│   │   ├── exercise_submission.py
│   │   ├── flashcard.py
│   │   ├── flashcard_review.py
│   │   ├── note.py
│   │   ├── bookmark.py
│   │   ├── conversation.py
│   │   ├── message.py
│   │   ├── document.py
│   │   ├── user_progress.py
│   │   ├── ai_quiz_generation.py
│   │   └── ai_summary.py
│   │
│   ├── schemas/                   # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── common.py              # Pagination, etc.
│   │   ├── user.py
│   │   ├── auth.py
│   │   ├── category.py
│   │   ├── course.py
│   │   ├── lesson.py
│   │   ├── quiz.py
│   │   ├── exercise.py
│   │   ├── flashcard.py
│   │   ├── note.py
│   │   ├── bookmark.py
│   │   ├── chat.py
│   │   ├── ai_service.py
│   │   ├── learning_progress.py
│   │   └── document.py
│   │
│   └── core/
│       ├── __init__.py
│       ├── config.py              # Settings
│       ├── database.py            # Async DB setup
│       ├── security.py            # JWT, password hashing
│       ├── exceptions.py          # Custom exceptions
│       ├── dependencies.py        # FastAPI dependencies
│       └── cache.py               # Redis setup
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_courses.py
│   ├── test_lessons.py
│   ├── test_quizzes.py
│   ├── test_exercises.py
│   ├── test_flashcards.py
│   ├── test_chat.py
│   └── test_ai_services.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── notebooks/analyzes-be/         # Spec files
├── .claude/
├── .agent/
│
├── requirements.txt
├── pyproject.toml
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── .gitignore
└── README.md
```

---

## 📋 Controllers Summary (75 Endpoints)

| # | Controller | Endpoints | Mô tả |
|---|------------|-----------|-------|
| 1 | auth_controller.py | 8 | Register, Login, Logout, Refresh, Me, Change Password, Forgot/Reset |
| 2 | category_controller.py | 4 | CRUD categories (Admin) |
| 3 | user_controller.py | 4 | CRUD users |
| 4 | course_controller.py | 6 | CRUD + Enroll |
| 5 | lesson_controller.py | 5 | CRUD lessons |
| 6 | quiz_controller.py | 7 | CRUD + Submit + Attempts |
| 7 | exercise_controller.py | 8 | CRUD + Submit + Submissions |
| 8 | flashcard_controller.py | 7 | CRUD + Review + Progress |
| 9 | note_controller.py | 4 | CRUD notes |
| 10 | bookmark_controller.py | 3 | List + Create + Delete |
| 11 | chat_ai_controller.py | 6 | Conversations + Messages |
| 12 | ai_service_controller.py | 5 | Generate Quiz, Summarize, Solve, Grade, Generate Flashcards |
| 13 | learning_progress_controller.py | 3 | Overview + Course Progress + Complete |
| 14 | document_controller.py | 4 | CRUD documents |
| 15 | admin_controller.py | 1 | Statistics |

---

## 🎯 Controller Pattern Example

### Course Controller

```python
# src/controllers/course_controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from src.schemas.course import (
    CourseCreate,
    CourseUpdate,
    CourseResponse,
    CourseListResponse
)
from src.services.course_service import CourseService
from src.core.dependencies import get_current_user, require_role
from src.models.user import User

router = APIRouter(prefix="/api/courses", tags=["Courses"])


# ============ INDEX - List all courses ============
@router.get("", response_model=CourseListResponse)
async def index(
    page: int = 1,
    size: int = 10,
    category_id: int | None = None,
    level: str | None = None,
    search: str | None = None,
    service: CourseService = Depends()
):
    """Lấy danh sách khóa học với phân trang"""
    return await service.get_all(
        page=page,
        size=size,
        category_id=category_id,
        level=level,
        search=search
    )


# ============ SHOW - Get course by ID ============
@router.get("/{course_id}", response_model=CourseResponse)
async def show(
    course_id: int,
    current_user: Annotated[User | None, Depends(get_current_user_optional)] = None,
    service: CourseService = Depends()
):
    """Lấy chi tiết khóa học"""
    return await service.get_by_id(course_id, user=current_user)


# ============ CREATE - Create new course ============
@router.post("", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create(
    data: CourseCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: CourseService = Depends()
):
    """Tạo khóa học mới (any authenticated user)"""
    return await service.create(data, creator_id=current_user.id)


# ============ UPDATE - Update course ============
@router.put("/{course_id}", response_model=CourseResponse)
async def update(
    course_id: int,
    data: CourseUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: CourseService = Depends()
):
    """Cập nhật khóa học (Owner/Admin)"""
    return await service.update(course_id, data, user=current_user)


# ============ DELETE - Delete course ============
@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(
    course_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    service: CourseService = Depends()
):
    """Xóa khóa học (Owner/Admin)"""
    await service.delete(course_id, user=current_user)


# ============ ENROLL - Enroll in course ============
@router.post("/{course_id}/enroll", status_code=status.HTTP_200_OK)
async def enroll(
    course_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    service: CourseService = Depends()
):
    """Đăng ký khóa học"""
    await service.enroll(course_id, user_id=current_user.id)
    return {"message": "Enrolled successfully"}
```

---

## 🏭 Service Pattern Example

```python
# src/services/course_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status

from src.repositories.course_repository import CourseRepository
from src.repositories.enrollment_repository import EnrollmentRepository
from src.schemas.course import CourseCreate, CourseUpdate
from src.core.database import get_db
from src.models.user import User

class CourseService:
    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        course_repo: CourseRepository = Depends(),
        enrollment_repo: EnrollmentRepository = Depends()
    ):
        self.db = db
        self.course_repo = course_repo
        self.enrollment_repo = enrollment_repo

    async def get_all(
        self,
        page: int,
        size: int,
        category_id: int | None = None,
        level: str | None = None,
        search: str | None = None
    ) -> dict:
        """Lấy danh sách khóa học"""
        courses, total = await self.course_repo.find_all(
            page=page,
            size=size,
            category_id=category_id,
            level=level,
            search=search,
            is_published=True
        )
        return {
            "items": courses,
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size
        }

    async def get_by_id(self, course_id: int, user: User | None = None):
        """Lấy khóa học theo ID"""
        course = await self.course_repo.find_by_id(course_id)
        if not course:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Course not found")

        # Add enrollment info if user is logged in
        if user:
            enrollment = await self.enrollment_repo.find_by_user_and_course(
                user.id, course_id
            )
            course.is_enrolled = enrollment is not None
            if enrollment:
                course.progress = await self.course_repo.get_progress(course_id, user.id)

        return course

    async def create(self, data: CourseCreate, creator_id: int):
        """Tạo khóa học mới"""
        return await self.course_repo.create({
            **data.model_dump(),
            "creator_id": creator_id
        })

    async def update(self, course_id: int, data: CourseUpdate, user: User):
        """Cập nhật khóa học"""
        course = await self.course_repo.find_by_id(course_id)
        if not course:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Course not found")

        # Check permission (owner or admin)
        if course.creator_id != user.id and user.role != "admin":
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Not authorized")

        return await self.course_repo.update(course_id, data.model_dump(exclude_unset=True))

    async def delete(self, course_id: int, user: User):
        """Xóa khóa học"""
        course = await self.course_repo.find_by_id(course_id)
        if not course:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Course not found")

        # Check permission
        if course.creator_id != user.id and user.role != "admin":
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Not authorized")

        await self.course_repo.delete(course_id)

    async def enroll(self, course_id: int, user_id: int):
        """Đăng ký khóa học"""
        course = await self.course_repo.find_by_id(course_id)
        if not course:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Course not found")

        existing = await self.enrollment_repo.find_by_user_and_course(user_id, course_id)
        if existing:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Already enrolled")

        await self.enrollment_repo.create({
            "user_id": user_id,
            "course_id": course_id
        })
```

---

## 🗄️ Repository Pattern Example

```python
# src/repositories/course_repository.py
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.course import Course
from src.models.lesson import Lesson
from src.models.enrollment import Enrollment

class CourseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_all(
        self,
        page: int,
        size: int,
        category_id: int | None = None,
        level: str | None = None,
        search: str | None = None,
        is_published: bool | None = None,
        creator_id: int | None = None
    ) -> tuple[list[Course], int]:
        """Tìm tất cả khóa học với filter"""
        query = select(Course).options(
            selectinload(Course.creator),
            selectinload(Course.category)
        )

        # Filters
        if category_id:
            query = query.where(Course.category_id == category_id)
        if level:
            query = query.where(Course.level == level)
        if search:
            query = query.where(Course.title.ilike(f"%{search}%"))
        if is_published is not None:
            query = query.where(Course.is_published == is_published)
        if creator_id:
            query = query.where(Course.creator_id == creator_id)

        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.db.scalar(count_query)

        # Paginate
        query = query.offset((page - 1) * size).limit(size)
        query = query.order_by(Course.created_at.desc())
        result = await self.db.execute(query)

        return result.scalars().all(), total

    async def find_by_id(self, course_id: int) -> Course | None:
        """Tìm khóa học theo ID"""
        query = select(Course).where(Course.id == course_id).options(
            selectinload(Course.creator),
            selectinload(Course.category),
            selectinload(Course.lessons)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, data: dict) -> Course:
        """Tạo khóa học mới"""
        course = Course(**data)
        self.db.add(course)
        await self.db.commit()
        await self.db.refresh(course)
        return course

    async def update(self, course_id: int, data: dict) -> Course:
        """Cập nhật khóa học"""
        course = await self.find_by_id(course_id)
        for key, value in data.items():
            if value is not None:
                setattr(course, key, value)
        await self.db.commit()
        await self.db.refresh(course)
        return course

    async def delete(self, course_id: int):
        """Xóa khóa học"""
        course = await self.find_by_id(course_id)
        await self.db.delete(course)
        await self.db.commit()

    async def get_progress(self, course_id: int, user_id: int) -> int:
        """Tính tiến độ khóa học"""
        # Count total lessons
        total_query = select(func.count()).select_from(Lesson).where(
            Lesson.course_id == course_id
        )
        total = await self.db.scalar(total_query) or 0

        if total == 0:
            return 0

        # Count completed lessons
        from src.models.user_progress import UserProgress
        completed_query = select(func.count()).select_from(UserProgress).where(
            UserProgress.user_id == user_id,
            UserProgress.lesson_id.in_(
                select(Lesson.id).where(Lesson.course_id == course_id)
            ),
            UserProgress.completed == True
        )
        completed = await self.db.scalar(completed_query) or 0

        return int((completed / total) * 100)
```

---

## 📦 Schema Pattern Example

```python
# src/schemas/course.py
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

# ============ Nested Schemas ============
class CreatorBrief(BaseModel):
    """Thông tin ngắn gọn của creator"""
    id: int
    name: str
    avatar: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CategoryBrief(BaseModel):
    """Thông tin ngắn gọn của category"""
    id: int
    name: str
    slug: str

    model_config = ConfigDict(from_attributes=True)


# ============ Base Schema ============
class CourseBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category_id: Optional[int] = None
    level: str = Field("beginner", pattern="^(beginner|intermediate|advanced)$")
    thumbnail: Optional[str] = Field(None, max_length=500)
    duration_hours: int = Field(0, ge=0)


# ============ Create Schema ============
class CourseCreate(CourseBase):
    """Schema để tạo khóa học mới"""
    pass


# ============ Update Schema ============
class CourseUpdate(BaseModel):
    """Schema để cập nhật khóa học"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category_id: Optional[int] = None
    level: Optional[str] = Field(None, pattern="^(beginner|intermediate|advanced)$")
    thumbnail: Optional[str] = Field(None, max_length=500)
    duration_hours: Optional[int] = Field(None, ge=0)
    is_published: Optional[bool] = None


# ============ Response Schema ============
class CourseResponse(CourseBase):
    """Schema response cho 1 khóa học"""
    id: int
    creator: CreatorBrief
    category: Optional[CategoryBrief] = None
    is_published: bool
    lessons_count: int = 0
    enrolled_count: int = 0
    is_enrolled: bool = False
    progress: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ============ List Response Schema ============
class CourseListResponse(BaseModel):
    """Schema response cho danh sách khóa học"""
    items: list[CourseResponse]
    total: int
    page: int
    size: int
    pages: int
```

---

## 🤖 AI Service Pattern

```python
# src/services/ai_service.py
from anthropic import Anthropic
from openai import OpenAI
from typing import AsyncGenerator
import json

from src.core.config import settings
from src.core.cache import redis_client

class AIService:
    def __init__(self):
        self.claude = Anthropic(api_key=settings.AI_API_KEY)
        self.openai = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
        self.model = settings.AI_MODEL  # claude-3-sonnet or claude-3-haiku

    async def chat(
        self,
        message: str,
        conversation_history: list[dict],
        system_prompt: str,
        course_context: dict | None = None
    ) -> str:
        """Chat với AI"""
        # Build messages
        messages = conversation_history.copy()
        messages.append({"role": "user", "content": message})

        # Call Claude API
        response = self.claude.messages.create(
            model=self.model,
            max_tokens=2048,
            system=system_prompt,
            messages=messages
        )

        return response.content[0].text

    async def stream_chat(
        self,
        message: str,
        conversation_history: list[dict],
        system_prompt: str
    ) -> AsyncGenerator[str, None]:
        """Stream chat response"""
        messages = conversation_history.copy()
        messages.append({"role": "user", "content": message})

        with self.claude.messages.stream(
            model=self.model,
            max_tokens=2048,
            system=system_prompt,
            messages=messages
        ) as stream:
            for text in stream.text_stream:
                yield text

    async def generate_quiz(
        self,
        lesson_content: str,
        num_questions: int = 5,
        difficulty: str = "medium"
    ) -> dict:
        """AI tạo quiz từ nội dung bài học"""
        prompt = f"""
Nhiệm vụ: Tạo quiz từ nội dung bài học sau.

NỘI DUNG BÀI HỌC:
{lesson_content}

YÊU CẦU:
- Số câu hỏi: {num_questions}
- Độ khó: {difficulty}
- Loại câu hỏi: trắc nghiệm 1 đáp án
- Mỗi câu có 4 lựa chọn (A, B, C, D)

ĐỊNH DẠNG OUTPUT (JSON):
{{
  "questions": [
    {{
      "content": "Câu hỏi?",
      "answers": [
        {{"content": "Đáp án A", "is_correct": true}},
        {{"content": "Đáp án B", "is_correct": false}},
        {{"content": "Đáp án C", "is_correct": false}},
        {{"content": "Đáp án D", "is_correct": false}}
      ]
    }}
  ]
}}
"""
        response = self.claude.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse JSON response
        content = response.content[0].text
        # Extract JSON from response
        json_str = content[content.index("{"):content.rindex("}")+1]
        return json.loads(json_str)

    async def summarize(
        self,
        lesson_content: str,
        length: str = "medium"
    ) -> dict:
        """AI tóm tắt nội dung"""
        length_words = {"short": 100, "medium": 200, "long": 400}

        prompt = f"""
Nhiệm vụ: Tóm tắt nội dung bài học sau.

NỘI DUNG:
{lesson_content}

YÊU CẦU:
- Độ dài: {length_words.get(length, 200)} từ
- Trình bày các ý chính thành bullet points
- Giữ lại các từ khóa quan trọng

ĐỊNH DẠNG OUTPUT (JSON):
{{
  "summary": "Tóm tắt ngắn gọn...",
  "key_points": ["Điểm 1", "Điểm 2", "Điểm 3"],
  "keywords": ["keyword1", "keyword2"]
}}
"""
        response = self.claude.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.content[0].text
        json_str = content[content.index("{"):content.rindex("}")+1]
        return json.loads(json_str)

    async def grade_submission(
        self,
        exercise_description: str,
        submission_answer: str,
        grading_criteria: str,
        max_score: int = 100
    ) -> dict:
        """AI chấm điểm bài nộp"""
        prompt = f"""
Nhiệm vụ: Chấm điểm bài nộp của học viên.

BÀI TẬP:
{exercise_description}

TIÊU CHÍ CHẤM ĐIỂM:
{grading_criteria}

ĐIỂM TỐI ĐA: {max_score}

BÀI NỘP CỦA HỌC VIÊN:
{submission_answer}

ĐỊNH DẠNG OUTPUT (JSON):
{{
  "score": 85,
  "overall_comment": "Nhận xét chung...",
  "strengths": ["Điểm tốt 1", "Điểm tốt 2"],
  "improvements": ["Cần cải thiện 1", "Cần cải thiện 2"],
  "suggestions": ["Gợi ý 1"]
}}
"""
        response = self.claude.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.content[0].text
        json_str = content[content.index("{"):content.rindex("}")+1]
        return json.loads(json_str)
```

---

## 🚀 Commands

| Task | Command |
|------|---------|
| Run server | `uvicorn src.main:app --reload` |
| Run tests | `pytest` |
| Format code | `black .` |
| Lint code | `ruff check --fix .` |
| Type check | `mypy src` |
| Create migration | `alembic revision --autogenerate -m "msg"` |
| Apply migrations | `alembic upgrade head` |
| Docker up | `docker-compose up -d` |

---

*Tài liệu này định nghĩa cấu trúc code cho hệ thống.*
*Version: 3.0 - 75 APIs, 21 Tables, 15 Controllers, 15 Services*
