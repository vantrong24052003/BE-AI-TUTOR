# EXERCISES Feature Specification

> Chi tiết specification cho tính năng Exercise Submission với AI Grading

---

## 1. TỔNG QUAN

### Mô tả
Hệ thống bài tập với nộp bài, chấm điểm thủ công và AI grading.

### Business Rules
- Exercise thuộc về một Lesson
- Có 4 loại bài tập: text, code, file, multiple choice
- User có số lần nộp tối đa (max_attempts)
- AI có thể chấm tự động cho text và code
- Best score được lưu lại

---

## 2. DATA MODEL

### Exercise Fields

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Primary key |
| lesson_id | integer | FK → lessons |
| title | string | Tiêu đề bài tập |
| description | text | Mô tả yêu cầu |
| type | enum | text/code/file/multiple |
| max_score | decimal | Điểm tối đa |
| max_attempts | integer | Số lần nộp tối đa (0 = unlimited) |
| order | integer | Thứ tự |
| rubric | json | Tiêu chí chấm điểm |
| created_at | timestamp | Thời gian tạo |

### Submission Fields

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Primary key |
| exercise_id | integer | FK → exercises |
| user_id | integer | FK → users |
| answer | text | Câu trả lời (text/code) |
| file_url | string | URL file nộp (nếu type=file) |
| score | decimal | Điểm đạt được |
| feedback | text | Feedback từ instructor |
| ai_feedback | json | Feedback từ AI |
| status | enum | pending/grading/graded/needs_review |
| attempt_number | integer | Lần nộp thứ mấy |
| submitted_at | timestamp | Thời gian nộp |
| graded_at | timestamp | Thời gian chấm |

---

## 3. API ENDPOINTS

### 3.1 Get Exercises by Lesson

**Endpoint**: `GET /api/v1/lessons/:lesson_id/exercises`

**Headers**: `Authorization: Bearer <token>`

**Success Response** (200):
```json
{
  "exercises": [
    {
      "id": 1,
      "lesson_id": 1,
      "title": "Viết hàm tính tổng",
      "description": "Viết hàm Python tính tổng 2 số",
      "type": "code",
      "max_score": 10,
      "max_attempts": 3,
      "order": 1,
      "has_submitted": true,
      "best_score": 8.5,
      "attempts_used": 2,
      "status": "graded"
    }
  ]
}
```

---

### 3.2 Get Exercise Detail

**Endpoint**: `GET /api/v1/exercises/:id`

**Headers**: `Authorization: Bearer <token>`

**Success Response** (200):
```json
{
  "id": 1,
  "lesson_id": 1,
  "title": "Viết hàm tính tổng",
  "description": "Viết hàm Python tính tổng 2 số\n\nYêu cầu:\n- Hàm nhận 2 tham số\n- Trả về tổng 2 số\n- Xử lý edge cases",
  "type": "code",
  "max_score": 10,
  "max_attempts": 3,
  "rubric": {
    "criteria": [
      {"name": "Correctness", "weight": 0.5, "description": "Code runs correctly"},
      {"name": "Edge cases", "weight": 0.3, "description": "Handles edge cases"},
      {"name": "Code style", "weight": 0.2, "description": "Clean and readable"}
    ]
  },
  "submissions": [
    {
      "id": 1,
      "attempt_number": 1,
      "score": 6,
      "status": "graded",
      "submitted_at": "2026-03-01T09:00:00Z"
    },
    {
      "id": 2,
      "attempt_number": 2,
      "score": 8.5,
      "status": "graded",
      "submitted_at": "2026-03-01T10:00:00Z"
    }
  ]
}
```

---

### 3.3 Submit Exercise

**Endpoint**: `POST /api/v1/exercises/:id/submit`

**Headers**: `Authorization: Bearer <token>`

**Request Body (text/code)**:
```json
{
  "answer": "def add(a, b):\n    return a + b"
}
```

**Request Body (file)**:
```
Content-Type: multipart/form-data
file: <binary>
```

**Preconditions**:
- Phải enroll vào course
- Nếu max_attempts > 0: chưa vượt quá số lần

**Success Response** (201):
```json
{
  "message": "Submission received",
  "submission": {
    "id": 3,
    "exercise_id": 1,
    "attempt_number": 3,
    "status": "grading",
    "submitted_at": "2026-03-01T11:00:00Z"
  },
  "ai_grading_in_progress": true
}
```

---

### 3.4 Get Submission Detail

**Endpoint**: `GET /api/v1/submissions/:id`

**Headers**: `Authorization: Bearer <token>`

**Success Response** (200):
```json
{
  "id": 3,
  "exercise_id": 1,
  "user_id": 5,
  "answer": "def add(a, b):\n    return a + b",
  "score": 8.5,
  "feedback": "Good work! Consider adding type hints.",
  "ai_feedback": {
    "score": 8.5,
    "overall_comment": "Well-structured solution with correct logic.",
    "criteria_scores": [
      {"name": "Correctness", "score": 5, "max_score": 5, "comment": "Perfect"},
      {"name": "Edge cases", "score": 2, "max_score": 3, "comment": "Missing negative number handling"},
      {"name": "Code style", "score": 1.5, "max_score": 2, "comment": "Add type hints for better readability"}
    ],
    "strengths": [
      "Clean function definition",
      "Correct return statement"
    ],
    "improvements": [
      "Add type hints: def add(a: int, b: int) -> int",
      "Consider handling None values"
    ],
    "suggested_solution": "def add(a: int | float, b: int | float) -> int | float:\n    return a + b"
  },
  "status": "graded",
  "attempt_number": 3,
  "submitted_at": "2026-03-01T11:00:00Z",
  "graded_at": "2026-03-01T11:00:30Z"
}
```

---

### 3.5 Re-submit Exercise

**Endpoint**: `POST /api/v1/submissions/:id/resubmit`

**Headers**: `Authorization: Bearer <token>`

**Note**: Tạo submission mới từ submission cũ, tăng attempt_number.

---

### 3.6 AI Grade Submission

**Endpoint**: `POST /api/v1/ai/grade-submission`

**Headers**: `Authorization: Bearer <token>`

**Authorization**: Admin only (hoặc trigger tự động)

**Request Body**:
```json
{
  "submission_id": 3
}
```

**Success Response** (200):
```json
{
  "message": "Grading completed",
  "submission": {
    "id": 3,
    "score": 8.5,
    "status": "graded"
  },
  "tokens_used": 850
}
```

---

## 4. AI GRADING PROMPT

### Prompt Template

```
You are an expert programming instructor. Grade the following exercise submission.

EXERCISE:
Title: {title}
Description: {description}
Type: {type}

RUBRIC:
{rubric_json}

STUDENT ANSWER:
{answer}

Grade the submission based on the rubric. Provide:
1. A score out of {max_score}
2. Score breakdown for each criterion
3. Overall comment
4. Strengths (2-3 points)
5. Areas for improvement (2-3 points)
6. Suggested solution (if applicable)

Respond in JSON format:
{
  "score": <number>,
  "overall_comment": "<string>",
  "criteria_scores": [
    {"name": "<criterion>", "score": <number>, "max_score": <number>, "comment": "<string>"}
  ],
  "strengths": ["<string>", ...],
  "improvements": ["<string>", ...],
  "suggested_solution": "<string>"
}
```

---

## 5. IMPLEMENTATION

### Service

```python
# app/services/exercise_service.py
from datetime import datetime
from app.repositories.exercise_repository import ExerciseRepository
from app.repositories.submission_repository import SubmissionRepository
from app.services.ai_service import AIService
from app.exceptions import NotFoundError, ValidationError, AuthorizationError

class ExerciseService:
    def __init__(
        self,
        exercise_repo: ExerciseRepository,
        submission_repo: SubmissionRepository,
        ai_service: AIService
    ):
        self.exercise_repo = exercise_repo
        self.submission_repo = submission_repo
        self.ai_service = ai_service

    async def submit_exercise(self, exercise_id: int, user_id: int,
                             answer: str = None, file_url: str = None) -> dict:
        exercise = await self.exercise_repo.get_by_id(exercise_id)
        if not exercise:
            raise NotFoundError("Exercise not found")

        # Check attempts
        if exercise["max_attempts"] > 0:
            attempts = await self.submission_repo.count_by_exercise_and_user(
                exercise_id, user_id
            )
            if attempts >= exercise["max_attempts"]:
                raise ValidationError("Maximum attempts reached")

        # Get attempt number
        attempt_number = await self.submission_repo.get_next_attempt_number(
            exercise_id, user_id
        )

        # Create submission
        submission = await self.submission_repo.create({
            "exercise_id": exercise_id,
            "user_id": user_id,
            "answer": answer,
            "file_url": file_url,
            "attempt_number": attempt_number,
            "status": "grading",
            "submitted_at": datetime.utcnow()
        })

        # Trigger AI grading for text/code types
        if exercise["type"] in ["text", "code"]:
            await self._trigger_ai_grading(submission["id"], exercise, answer)

        return submission

    async def _trigger_ai_grading(self, submission_id: int, exercise: dict, answer: str):
        """Trigger AI grading asynchronously."""
        try:
            ai_result = await self.ai_service.grade_exercise(
                exercise_title=exercise["title"],
                exercise_description=exercise["description"],
                exercise_type=exercise["type"],
                rubric=exercise.get("rubric"),
                max_score=exercise["max_score"],
                answer=answer
            )

            # Update submission with AI feedback
            await self.submission_repo.update(submission_id, {
                "score": ai_result["score"],
                "ai_feedback": ai_result,
                "status": "graded",
                "graded_at": datetime.utcnow()
            })
        except Exception as e:
            # Mark for manual review if AI fails
            await self.submission_repo.update(submission_id, {
                "status": "needs_review"
            })
            raise

    async def get_submission_detail(self, submission_id: int, user_id: int) -> dict:
        submission = await self.submission_repo.get_by_id(submission_id)
        if not submission:
            raise NotFoundError("Submission not found")

        # Check authorization
        if submission["user_id"] != user_id:
            user = await self.user_repo.get_by_id(user_id)
            if user["role"] != "admin":
                raise AuthorizationError("Not authorized to view this submission")

        return submission
```

### AI Service Integration

```python
# app/services/ai_service.py
import json
from anthropic import Anthropic
from app.core.config import settings

class AIService:
    def __init__(self):
        self.client = Anthropic(api_key=settings.AI_API_KEY)

    async def grade_exercise(
        self,
        exercise_title: str,
        exercise_description: str,
        exercise_type: str,
        rubric: dict,
        max_score: float,
        answer: str
    ) -> dict:
        prompt = f"""You are an expert programming instructor. Grade the following exercise submission.

EXERCISE:
Title: {exercise_title}
Description: {exercise_description}
Type: {exercise_type}

RUBRIC:
{json.dumps(rubric, indent=2) if rubric else 'No specific rubric provided'}

MAX SCORE: {max_score}

STUDENT ANSWER:
{answer}

Grade the submission. Provide:
1. A score out of {max_score}
2. Score breakdown for each criterion (if rubric provided)
3. Overall comment
4. Strengths (2-3 points)
5. Areas for improvement (2-3 points)
6. Suggested solution (if applicable)

Respond in JSON format only."""

        response = self.client.messages.create(
            model="claude-sonnet-4-6-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        result_text = response.content[0].text
        result = json.loads(result_text)

        return result
```

---

## 6. DATABASE SCHEMA

```sql
-- exercises table
CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    lesson_id INTEGER NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    type VARCHAR(20) NOT NULL CHECK (type IN ('text', 'code', 'file', 'multiple')),
    max_score DECIMAL(5,2) DEFAULT 10,
    max_attempts INTEGER DEFAULT 0,
    "order" INTEGER NOT NULL DEFAULT 0,
    rubric JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- exercise_submissions table
CREATE TABLE exercise_submissions (
    id SERIAL PRIMARY KEY,
    exercise_id INTEGER NOT NULL REFERENCES exercises(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    answer TEXT,
    file_url VARCHAR(500),
    score DECIMAL(5,2),
    feedback TEXT,
    ai_feedback JSONB,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'grading', 'graded', 'needs_review')),
    attempt_number INTEGER NOT NULL,
    submitted_at TIMESTAMP NOT NULL DEFAULT NOW(),
    graded_at TIMESTAMP
);

-- Indexes
CREATE INDEX idx_exercises_lesson ON exercises(lesson_id);
CREATE INDEX idx_submissions_exercise_user ON exercise_submissions(exercise_id, user_id);
CREATE INDEX idx_submissions_user ON exercise_submissions(user_id);
```

---

## 7. TESTS

```python
# tests/integration/test_exercises_api.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
class TestExercisesAPI:
    async def test_submit_text_exercise(self, client: AsyncClient, auth_header, exercise_text):
        response = await client.post(
            f"/api/v1/exercises/{exercise_text.id}/submit",
            headers=auth_header,
            json={"answer": "This is my answer"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["submission"]["status"] == "grading"

    async def test_submit_code_exercise(self, client: AsyncClient, auth_header, exercise_code):
        code = "def add(a, b):\n    return a + b"
        response = await client.post(
            f"/api/v1/exercises/{exercise_code.id}/submit",
            headers=auth_header,
            json={"answer": code}
        )
        assert response.status_code == 201

    async def test_max_attempts_limit(self, client: AsyncClient, auth_header, exercise_with_limit):
        for i in range(exercise_with_limit.max_attempts):
            response = await client.post(
                f"/api/v1/exercises/{exercise_with_limit.id}/submit",
                headers=auth_header,
                json={"answer": f"Answer {i}"}
            )
            assert response.status_code == 201

        # Try one more
        response = await client.post(
            f"/api/v1/exercises/{exercise_with_limit.id}/submit",
            headers=auth_header,
            json={"answer": "One more try"}
        )
        assert response.status_code == 400

    async def test_get_submission_with_ai_feedback(
        self, client: AsyncClient, auth_header, graded_submission
    ):
        response = await client.get(
            f"/api/v1/submissions/{graded_submission.id}",
            headers=auth_header
        )
        assert response.status_code == 200
        data = response.json()
        assert "ai_feedback" in data
        assert data["status"] == "graded"
```

---

*Version: 1.0 - Updated: 2026-03-01*
