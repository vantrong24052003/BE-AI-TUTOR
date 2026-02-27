# BE AI TUTOR - Code Structure

> Chi tiết cấu trúc code Backend FastAPI

---

## 📁 Project Structure

```
BE-AI-TUTOR/
│
├── src/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   │
│   ├── controllers/               # HTTP handlers (5 methods RESTful)
│   │   ├── __init__.py
│   │   ├── auth_controller.py     # Auth (special - login/register)
│   │   ├── user_controller.py     # User CRUD
│   │   ├── course_controller.py   # Course CRUD
│   │   ├── lesson_controller.py   # Lesson CRUD
│   │   ├── quiz_controller.py     # Quiz CRUD
│   │   ├── chat_controller.py     # Chat (special - messages)
│   │   ├── progress_controller.py # Progress (special - tracking)
│   │   └── document_controller.py # Document CRUD
│   │
│   ├── services/                  # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── course_service.py
│   │   ├── lesson_service.py
│   │   ├── quiz_service.py
│   │   ├── chat_service.py
│   │   ├── progress_service.py
│   │   └── document_service.py
│   │
│   ├── repositories/              # Data access layer
│   │   ├── __init__.py
│   │   ├── base_repository.py
│   │   ├── user_repository.py
│   │   ├── course_repository.py
│   │   ├── lesson_repository.py
│   │   ├── quiz_repository.py
│   │   ├── chat_repository.py
│   │   └── progress_repository.py
│   │
│   ├── models/                    # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── course.py
│   │   ├── lesson.py
│   │   ├── quiz.py
│   │   ├── chat.py
│   │   └── progress.py
│   │
│   ├── schemas/                   # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── course.py
│   │   ├── lesson.py
│   │   ├── quiz.py
│   │   ├── chat.py
│   │   ├── progress.py
│   │   └── common.py
│   │
│   └── core/
│       ├── __init__.py
│       ├── config.py
│       ├── database.py
│       ├── security.py
│       ├── exceptions.py
│       └── dependencies.py
│
├── tests/
├── alembic/
├── notebooks/
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

## 📝 RESTful Controller Pattern

### Mỗi Controller chỉ có 5 methods chuẩn

```python
# src/controllers/[name]_controller.py
from fastapi import APIRouter

router = APIRouter(prefix="/api/[resource]", tags=["[Resource]"])

@router.get("")           # INDEX  - List all
@router.get("/{id}")      # SHOW   - Get one
@router.post("")          # CREATE - Create new
@router.put("/{id}")      # UPDATE - Update full
@router.delete("/{id}")   # DELETE - Delete
```

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
    category: str | None = None,
    search: str | None = None,
    service: CourseService = Depends()
):
    """
    Lấy danh sách khóa học với phân trang

    Query params:
    - page: Số trang (default: 1)
    - size: Số item/trang (default: 10)
    - category: Lọc theo danh mục
    - search: Tìm kiếm theo tên
    """
    return await service.get_all(
        page=page,
        size=size,
        category=category,
        search=search
    )


# ============ SHOW - Get course by ID ============
@router.get("/{course_id}", response_model=CourseResponse)
async def show(
    course_id: int,
    service: CourseService = Depends()
):
    """
    Lấy chi tiết khóa học theo ID

    Path params:
    - course_id: ID của khóa học
    """
    course = await service.get_by_id(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return course


# ============ CREATE - Create new course ============
@router.post("", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create(
    data: CourseCreate,
    current_user: Annotated[User, Depends(require_role(["teacher", "admin"]))],
    service: CourseService = Depends()
):
    """
    Tạo khóa học mới (Teacher+)

    Body:
    - title: Tên khóa học (required)
    - description: Mô tả
    - category: Danh mục
    - level: Cấp độ (beginner/intermediate/advanced)
    - thumbnail: URL hình ảnh
    """
    return await service.create(data, teacher_id=current_user.id)


# ============ UPDATE - Update course ============
@router.put("/{course_id}", response_model=CourseResponse)
async def update(
    course_id: int,
    data: CourseUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: CourseService = Depends()
):
    """
    Cập nhật khóa học (Owner/Admin)

    Path params:
    - course_id: ID của khóa học

    Body: Các trường cần cập nhật
    """
    return await service.update(course_id, data, user=current_user)


# ============ DELETE - Delete course ============
@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(
    course_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    service: CourseService = Depends()
):
    """
    Xóa khóa học (Owner/Admin)

    Path params:
    - course_id: ID của khóa học
    """
    await service.delete(course_id, user=current_user)
```

---

## 🏭 Service Pattern Example

```python
# src/services/course_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status

from src.repositories.course_repository import CourseRepository
from src.schemas.course import CourseCreate, CourseUpdate
from src.core.database import get_db
from src.models.user import User

class CourseService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.repository = CourseRepository(db)

    async def get_all(
        self,
        page: int,
        size: int,
        category: str | None = None,
        search: str | None = None
    ) -> dict:
        """Lấy danh sách khóa học"""
        courses, total = await self.repository.find_all(
            page=page,
            size=size,
            category=category,
            search=search
        )
        return {
            "items": courses,
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size
        }

    async def get_by_id(self, course_id: int):
        """Lấy khóa học theo ID"""
        return await self.repository.find_by_id(course_id)

    async def create(self, data: CourseCreate, teacher_id: int):
        """Tạo khóa học mới"""
        return await self.repository.create({
            **data.model_dump(),
            "teacher_id": teacher_id
        })

    async def update(self, course_id: int, data: CourseUpdate, user: User):
        """Cập nhật khóa học"""
        course = await self.repository.find_by_id(course_id)
        if not course:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Course not found")

        # Check permission
        if course.teacher_id != user.id and user.role != "admin":
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Not authorized")

        return await self.repository.update(course_id, data.model_dump(exclude_unset=True))

    async def delete(self, course_id: int, user: User):
        """Xóa khóa học"""
        course = await self.repository.find_by_id(course_id)
        if not course:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Course not found")

        # Check permission
        if course.teacher_id != user.id and user.role != "admin":
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Not authorized")

        await self.repository.delete(course_id)
```

---

## 🗄️ Repository Pattern Example

```python
# src/repositories/course_repository.py
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.course import Course

class CourseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_all(
        self,
        page: int,
        size: int,
        category: str | None = None,
        search: str | None = None
    ) -> tuple[list[Course], int]:
        """Tìm tất cả khóa học với filter"""
        query = select(Course)

        # Filter by category
        if category:
            query = query.where(Course.category == category)

        # Search by title
        if search:
            query = query.where(Course.title.ilike(f"%{search}%"))

        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.db.scalar(count_query)

        # Paginate
        query = query.offset((page - 1) * size).limit(size)
        result = await self.db.execute(query)

        return result.scalars().all(), total

    async def find_by_id(self, course_id: int) -> Course | None:
        """Tìm khóa học theo ID"""
        query = select(Course).where(Course.id == course_id)
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
```

---

## 📦 Schema Pattern Example

```python
# src/schemas/course.py
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

# ============ Base Schema ============
class CourseBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Tên khóa học")
    description: Optional[str] = Field(None, description="Mô tả khóa học")
    category: Optional[str] = Field(None, max_length=100, description="Danh mục")
    level: str = Field("beginner", description="Cấp độ: beginner/intermediate/advanced")
    thumbnail: Optional[str] = Field(None, max_length=500, description="URL hình ảnh")

# ============ Create Schema ============
class CourseCreate(CourseBase):
    """Schema để tạo khóa học mới"""
    pass

# ============ Update Schema ============
class CourseUpdate(BaseModel):
    """Schema để cập nhật khóa học (tất cả optional)"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    level: Optional[str] = None
    thumbnail: Optional[str] = Field(None, max_length=500)
    is_published: Optional[bool] = None

# ============ Response Schema ============
class CourseResponse(CourseBase):
    """Schema response cho 1 khóa học"""
    id: int
    teacher_id: int
    is_published: bool
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

## 🗃️ Model Pattern Example

```python
# src/models/course.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.models.base import Base

class Course(Base):
    __tablename__ = "courses"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Columns
    title = Column(String(255), nullable=False)
    description = Column(Text)
    thumbnail = Column(String(500))
    category = Column(String(100))
    level = Column(String(50), default="beginner")
    duration_hours = Column(Integer, default=0)
    is_published = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    teacher = relationship("User", back_populates="courses")
    lessons = relationship(
        "Lesson",
        back_populates="course",
        cascade="all, delete-orphan",
        order_by="Lesson.order"
    )
    enrollments = relationship("Enrollment", back_populates="course")
    documents = relationship("Document", back_populates="course")

    def __repr__(self):
        return f"<Course {self.title}>"
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
