# QUIZ Feature Specification

> Chi tiết specification cho tính năng Quiz System - Document-RAG Based

---

## 1. TỔNG QUAN

### Mô tả
Hệ thống quiz được tạo tự động bởi AI hoặc thủ công từ Documents. Sử dụng JSONB để lưu trữ bộ câu hỏi nhằm tối ưu hiệu suất và linh hoạt cấu trúc.

### Business Rules
- Quiz thuộc về một Document (tài liệu).
- Sử dụng UUID v4 cho tất cả IDs.
- Mỗi Question lưu trữ bộ answers trong cùng bản ghi (JSONB).
- User có thể làm lại quiz không giới hạn.
- Lưu lịch sử làm bài (Attempts) và Best Score.

---

## 2. DATA MODEL (UUID & JSONB)

### 2.1 Quiz Table
| Field | Type | Description |
|-------|------|-------------|
| id | string (UUID) | Primary key |
| document_id | string (UUID) | FK → documents |
| title | string | Tiêu đề quiz |
| description | text | Mô tả |
| passing_score | decimal | Điểm đạt (default: 60) |
| is_ai_generated | boolean | Cờ đánh dấu |
| questions | JSONB | Danh sách câu hỏi (xem bên dưới) |
| created_at | timestamp | |

### Question Structure (Lưu trong JSONB column `questions`)
```json
[
  {
    "id": "uuid-q1",
    "content": "Python hỗ trợ những paradigm nào?",
    "explanation": "Giải thích...",
    "points": 1.0,
    "is_multiple_selection": true, 
    "answers": [
      {"id": "a1", "content": "OOP", "is_correct": true},
      {"id": "a2", "content": "Functional", "is_correct": true},
      {"id": "a3", "content": "Assembly", "is_correct": false}
    ]
  }
]
```

### 2.2 Quiz Attempt Table
| Field | Type | Description |
|-------|------|-------------|
| id | string (UUID) | |
| quiz_id | string (UUID) | |
| user_id | string (UUID) | |
| score | decimal | |
| passed | boolean | |
| user_responses | JSONB | Lưu lựa chọn: `{"q-id": "a-id"}` hoặc `{"q-id": ["a-id1", "a-id2"]}` |
| started_at | timestamp | |
| completed_at | timestamp | |

---

## 3. API ENDPOINTS (v5.1)

### 3.1 Get Quiz Detail

**Endpoint**: `GET /api/v1/quizzes/:id`

**Success Response** (200):
```json
{
  "id": "uuid-quiz-1",
  "title": "Machine Learning Quiz",
  "questions": [
    {
      "id": "q-1",
      "content": "What is supervised learning?",
      "answers": [
        {"id": "ans-1", "content": "Learning with labeled data"},
        {"id": "ans-2", "content": "Learning without labels"}
      ]
    }
  ]
}
```
*Note: Correct answers are HIDDEN in this endpoint.*

---

### 3.2 Submit Quiz

**Endpoint**: `POST /api/v1/quizzes/:id/submit`

**Request Body**:
```json
{
  "responses": {
    "q-1": "ans-1", 
    "q-2": ["ans-1", "ans-3"] 
  }
}
```

**Success Response** (200):
```json
{
  "attempt": {
    "id": "uuid-attempt-1",
    "score": 100,
    "passed": true,
    "completed_at": "2026-03-01T10:00:00Z"
  },
  "feedback": [
    {
      "question_id": "q-1",
      "is_correct": true,
      "correct_answer_id": "ans-1",
      "explanation": "Supervised learning uses labeled training data."
    }
  ]
}
```

---

## 4. DATABASE SCHEMA (PostgreSQL)

```sql
-- Standardized v5.1 with UUID and JSONB
CREATE TABLE quizzes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    passing_score DECIMAL(5,2) DEFAULT 60,
    questions JSONB NOT NULL DEFAULT '[]',
    is_ai_generated BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE quiz_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    quiz_id UUID NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id),
    score DECIMAL(5,2),
    passed BOOLEAN,
    user_responses JSONB NOT NULL DEFAULT '{}',
    started_at TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_quizzes_doc ON quizzes(document_id);
CREATE INDEX idx_attempts_user_quiz ON quiz_attempts(user_id, quiz_id);
CREATE INDEX idx_quizzes_questions_gin ON quizzes USING GIN (questions);
```

---

*Version: 5.1 - Updated: 2026-03-01*
*Document-RAG Alignment: JSONB + UUID Standards*
