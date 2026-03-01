# QUIZ Feature Specification

> Chi tiết specification cho tính năng Quiz System

---

## 1. TỔNG QUAN

### Mô tả
Hệ thống quiz với multiple choice questions, tracking kết quả và AI generation.

### Business Rules
- Quiz thuộc về một Lesson
- Mỗi Question có 2-5 Answers
- Chỉ có 1 Answer đúng cho mỗi Question
- User có thể retry quiz không giới hạn
- Lưu best score cho mỗi user
- AI có thể generate quiz từ nội dung lesson

---

## 2. DATA MODEL

### Quiz Fields

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Primary key |
| lesson_id | integer | FK → lessons |
| title | string | Tiêu đề quiz |
| description | text | Mô tả |
| time_limit_minutes | integer | Giới hạn thời gian (nullable) |
| passing_score | decimal | Điểm qua môn (default: 60) |
| max_attempts | integer | Số lần làm tối đa (0 = unlimited) |
| shuffle_questions | boolean | Random thứ tự câu hỏi |
| created_at | timestamp | Thời gian tạo |

### Question Fields

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Primary key |
| quiz_id | integer | FK → quizzes |
| content | text | Nội dung câu hỏi |
| explanation | text | Giải thích đáp án |
| order | integer | Thứ tự |
| points | decimal | Điểm (default: 1) |

### Answer Fields

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Primary key |
| question_id | integer | FK → questions |
| content | text | Nội dung đáp án |
| is_correct | boolean | Có phải đáp án đúng |

### Quiz Attempt Fields

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Primary key |
| quiz_id | integer | FK → quizzes |
| user_id | integer | FK → users |
| score | decimal | Điểm đạt được |
| passed | boolean | Có qua môn không |
| started_at | timestamp | Thời gian bắt đầu |
| completed_at | timestamp | Thời gian hoàn thành |
| time_spent_seconds | integer | Thời gian làm bài |

---

## 3. API ENDPOINTS

### 3.1 Get Quiz by Lesson

**Endpoint**: `GET /api/v1/lessons/:lesson_id/quiz`

**Headers**: `Authorization: Bearer <token>`

**Success Response** (200):
```json
{
  "id": 1,
  "lesson_id": 1,
  "title": "Quiz: Giới thiệu Python",
  "description": "Kiểm tra kiến thức cơ bản",
  "time_limit_minutes": 15,
  "passing_score": 60,
  "max_attempts": 0,
  "shuffle_questions": true,
  "questions_count": 10,
  "total_points": 10,
  "attempts_count": 2,
  "best_score": 80,
  "best_attempt_id": 5
}
```

---

### 3.2 Start Quiz Attempt

**Endpoint**: `POST /api/v1/quizzes/:quiz_id/start`

**Headers**: `Authorization: Bearer <token>`

**Preconditions**:
- Phải enroll vào course
- Nếu max_attempts > 0: chưa vượt quá số lần

**Success Response** (200):
```json
{
  "attempt": {
    "id": 1,
    "quiz_id": 1,
    "started_at": "2026-03-01T10:00:00Z",
    "expires_at": "2026-03-01T10:15:00Z"
  },
  "questions": [
    {
      "id": 1,
      "content": "Python là gì?",
      "points": 1,
      "answers": [
        {"id": 1, "content": "Ngôn ngữ lập trình"},
        {"id": 2, "content": "Loài rắn"},
        {"id": 3, "content": "Một loại đồ ăn"},
        {"id": 4, "content": "Một loại xe"}
      ]
    }
  ]
}
```

**Note**: Nếu `shuffle_questions = true`, thứ tự questions và answers sẽ random.

---

### 3.3 Submit Answer

**Endpoint**: `POST /api/v1/attempts/:attempt_id/answer`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "question_id": 1,
  "answer_id": 1
}
```

**Success Response** (200):
```json
{
  "message": "Answer saved",
  "is_correct": true,
  "explanation": "Python là ngôn ngữ lập trình bậc cao..."
}
```

**Note**: Giải thích chỉ trả về sau khi submit quiz.

---

### 3.4 Submit Quiz

**Endpoint**: `POST /api/v1/attempts/:attempt_id/submit`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "answers": [
    {"question_id": 1, "answer_id": 1},
    {"question_id": 2, "answer_id": 5}
  ]
}
```

**Success Response** (200):
```json
{
  "attempt": {
    "id": 1,
    "score": 80,
    "passed": true,
    "time_spent_seconds": 450,
    "completed_at": "2026-03-01T10:07:30Z"
  },
  "results": {
    "correct_count": 8,
    "total_count": 10,
    "points_earned": 8,
    "total_points": 10
  },
  "questions": [
    {
      "id": 1,
      "content": "Python là gì?",
      "user_answer_id": 1,
      "correct_answer_id": 1,
      "is_correct": true,
      "explanation": "Python là ngôn ngữ lập trình..."
    }
  ]
}
```

---

### 3.5 Get Attempt Result

**Endpoint**: `GET /api/v1/attempts/:attempt_id`

**Headers**: `Authorization: Bearer <token>`

**Success Response**: Same as Submit Quiz response

---

### 3.6 Get Attempt History

**Endpoint**: `GET /api/v1/quizzes/:quiz_id/attempts`

**Headers**: `Authorization: Bearer <token>`

**Success Response** (200):
```json
{
  "attempts": [
    {
      "id": 1,
      "score": 60,
      "passed": true,
      "completed_at": "2026-03-01T09:00:00Z",
      "time_spent_seconds": 600
    },
    {
      "id": 2,
      "score": 80,
      "passed": true,
      "completed_at": "2026-03-01T10:00:00Z",
      "time_spent_seconds": 450
    }
  ],
  "meta": {
    "total_attempts": 2,
    "best_score": 80,
    "average_score": 70
  }
}
```

---

## 4. AI QUIZ GENERATION

### 4.1 Generate Quiz

**Endpoint**: `POST /api/v1/ai/generate-quiz`

**Headers**: `Authorization: Bearer <token>`

**Authorization**: Course creator only

**Request Body**:
```json
{
  "lesson_id": 1,
  "num_questions": 5,
  "difficulty": "medium"
}
```

**Success Response** (200):
```json
{
  "generation_id": 1,
  "quiz": {
    "title": "AI Generated Quiz: Giới thiệu Python",
    "questions": [
      {
        "content": "Câu hỏi được AI tạo...",
        "answers": [
          {"content": "Đáp án A", "is_correct": true},
          {"content": "Đáp án B", "is_correct": false},
          {"content": "Đáp án C", "is_correct": false},
          {"content": "Đáp án D", "is_correct": false}
        ],
        "explanation": "Giải thích..."
      }
    ]
  },
  "tokens_used": 1500
}
```

---

## 5. IMPLEMENTATION

### Service

```python
# app/services/quiz_service.py
import random
from datetime import datetime, timedelta
from app.repositories.quiz_repository import QuizRepository
from app.repositories.question_repository import QuestionRepository
from app.repositories.attempt_repository import AttemptRepository
from app.exceptions import NotFoundError, ValidationError, AuthorizationError

class QuizService:
    def __init__(
        self,
        quiz_repo: QuizRepository,
        question_repo: QuestionRepository,
        attempt_repo: AttemptRepository
    ):
        self.quiz_repo = quiz_repo
        self.question_repo = question_repo
        self.attempt_repo = attempt_repo

    async def start_attempt(self, quiz_id: int, user_id: int) -> dict:
        quiz = await self.quiz_repo.get_by_id(quiz_id)
        if not quiz:
            raise NotFoundError("Quiz not found")

        # Check max attempts
        if quiz["max_attempts"] > 0:
            attempts = await self.attempt_repo.count_by_quiz_and_user(quiz_id, user_id)
            if attempts >= quiz["max_attempts"]:
                raise ValidationError("Maximum attempts reached")

        # Create attempt
        attempt = await self.attempt_repo.create({
            "quiz_id": quiz_id,
            "user_id": user_id,
            "started_at": datetime.utcnow()
        })

        # Get questions with answers
        questions = await self.question_repo.get_by_quiz(quiz_id)

        # Shuffle if enabled
        if quiz["shuffle_questions"]:
            random.shuffle(questions)
            for q in questions:
                random.shuffle(q["answers"])

        # Remove correct answers from response
        for q in questions:
            for a in q["answers"]:
                del a["is_correct"]

        # Calculate expiry
        expires_at = None
        if quiz["time_limit_minutes"]:
            expires_at = datetime.utcnow() + timedelta(minutes=quiz["time_limit_minutes"])

        return {
            "attempt": {
                **attempt,
                "expires_at": expires_at
            },
            "questions": questions
        }

    async def submit_quiz(self, attempt_id: int, user_id: int, answers: list) -> dict:
        attempt = await self.attempt_repo.get_by_id(attempt_id)
        if not attempt or attempt["user_id"] != user_id:
            raise NotFoundError("Attempt not found")

        if attempt["completed_at"]:
            raise ValidationError("Attempt already submitted")

        quiz = await self.quiz_repo.get_by_id(attempt["quiz_id"])

        # Check time limit
        if quiz["time_limit_minutes"]:
            deadline = attempt["started_at"] + timedelta(minutes=quiz["time_limit_minutes"])
            if datetime.utcnow() > deadline:
                raise ValidationError("Time limit exceeded")

        # Get correct answers
        questions = await self.question_repo.get_by_quiz(attempt["quiz_id"])
        correct_map = {}
        for q in questions:
            for a in q["answers"]:
                if a["is_correct"]:
                    correct_map[q["id"]] = a["id"]

        # Calculate score
        correct_count = 0
        points_earned = 0
        total_points = sum(q["points"] for q in questions)

        answer_map = {a["question_id"]: a["answer_id"] for a in answers}

        results = []
        for q in questions:
            user_answer_id = answer_map.get(q["id"])
            correct_answer_id = correct_map[q["id"]]
            is_correct = user_answer_id == correct_answer_id

            if is_correct:
                correct_count += 1
                points_earned += q["points"]

            results.append({
                "question_id": q["id"],
                "user_answer_id": user_answer_id,
                "correct_answer_id": correct_answer_id,
                "is_correct": is_correct
            })

        score = round((points_earned / total_points) * 100, 2) if total_points > 0 else 0
        passed = score >= quiz["passing_score"]
        time_spent = int((datetime.utcnow() - attempt["started_at"]).total_seconds())

        # Update attempt
        updated = await self.attempt_repo.update(attempt_id, {
            "score": score,
            "passed": passed,
            "completed_at": datetime.utcnow(),
            "time_spent_seconds": time_spent
        })

        # Save answers
        await self.attempt_repo.save_answers(attempt_id, answers)

        return {
            "attempt": updated,
            "results": {
                "correct_count": correct_count,
                "total_count": len(questions),
                "points_earned": points_earned,
                "total_points": total_points
            }
        }
```

---

## 6. DATABASE SCHEMA

```sql
-- quizzes table
CREATE TABLE quizzes (
    id SERIAL PRIMARY KEY,
    lesson_id INTEGER NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    time_limit_minutes INTEGER,
    passing_score DECIMAL(5,2) DEFAULT 60,
    max_attempts INTEGER DEFAULT 0,
    shuffle_questions BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- questions table
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    explanation TEXT,
    "order" INTEGER NOT NULL,
    points DECIMAL(5,2) DEFAULT 1
);

-- answers table
CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT FALSE
);

-- quiz_attempts table
CREATE TABLE quiz_attempts (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER NOT NULL REFERENCES quizzes(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    score DECIMAL(5,2),
    passed BOOLEAN DEFAULT FALSE,
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    time_spent_seconds INTEGER
);

-- attempt_answers table (user's answers)
CREATE TABLE attempt_answers (
    id SERIAL PRIMARY KEY,
    attempt_id INTEGER NOT NULL REFERENCES quiz_attempts(id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL REFERENCES questions(id),
    answer_id INTEGER NOT NULL REFERENCES answers(id)
);

-- Indexes
CREATE INDEX idx_quizzes_lesson ON quizzes(lesson_id);
CREATE INDEX idx_questions_quiz ON questions(quiz_id);
CREATE INDEX idx_answers_question ON answers(question_id);
CREATE INDEX idx_attempts_quiz_user ON quiz_attempts(quiz_id, user_id);
```

---

## 7. TESTS

```python
# tests/integration/test_quiz_api.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
class TestQuizAPI:
    async def test_start_quiz(self, client: AsyncClient, auth_header, enrolled_quiz):
        response = await client.post(
            f"/api/v1/quizzes/{enrolled_quiz.id}/start",
            headers=auth_header
        )
        assert response.status_code == 200
        data = response.json()
        assert "attempt" in data
        assert "questions" in data

    async def test_submit_quiz(self, client: AsyncClient, auth_header, started_attempt):
        answers = [
            {"question_id": 1, "answer_id": 1},
            {"question_id": 2, "answer_id": 3}
        ]
        response = await client.post(
            f"/api/v1/attempts/{started_attempt.id}/submit",
            headers=auth_header,
            json={"answers": answers}
        )
        assert response.status_code == 200
        data = response.json()
        assert "score" in data["attempt"]
        assert "passed" in data["attempt"]

    async def test_max_attempts_limit(self, client: AsyncClient, auth_header, quiz_with_limit):
        # Exhaust attempts
        for _ in range(quiz_with_limit.max_attempts):
            response = await client.post(
                f"/api/v1/quizzes/{quiz_with_limit.id}/start",
                headers=auth_header
            )
            assert response.status_code == 200

        # Try again
        response = await client.post(
            f"/api/v1/quizzes/{quiz_with_limit.id}/start",
            headers=auth_header
        )
        assert response.status_code == 400
```

---

*Version: 1.0 - Updated: 2026-03-01*
