# BE AI TUTOR - Database Design

> Database schema chi tiết cho hệ thống AI Tutor

---

## 📊 ER Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DATABASE SCHEMA                                      │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│    users    │       │   courses   │       │   lessons   │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id (PK)     │       │ id (PK)     │       │ id (PK)     │
│ email       │◀──┐   │ title       │◀──┐   │ course_id   │──▶ courses.id
│ password    │   │   │ description │   │   │ title       │
│ name        │   │   │ teacher_id  │───┘   │ content     │
│ role        │   │   │ thumbnail   │       │ order       │
│ avatar      │   │   │ is_published│       │ video_url   │
│ created_at  │   │   │ created_at  │       │ duration    │
└─────────────┘   │   └─────────────┘       └─────────────┘
                  │
                  │   ┌─────────────┐       ┌─────────────┐
                  │   │ enrollments │       │  quizzes    │
                  │   ├─────────────┤       ├─────────────┤
                  └──▶│ id (PK)     │       │ id (PK)     │
                      │ user_id     │──┐    │ lesson_id   │──▶ lessons.id
                      │ course_id   │──┼──▶ │ title       │
                      │ enrolled_at │  │    │ time_limit  │
                      │ completed   │  │    │ created_at  │
                      └─────────────┘  │    └─────────────┘
                                       │
                                       │    ┌─────────────┐
                                       │    │  questions  │
                                       │    ├─────────────┤
                                       │    │ id (PK)     │
                                       │    │ quiz_id     │──▶ quizzes.id
                                       │    │ content     │
                                       │    │ type        │
                                       │    │ points      │
                                       │    │ order       │
                                       │    └─────────────┘
                                       │           │
                                       │           ▼
                                       │    ┌─────────────┐
                                       │    │  answers    │
                                       │    ├─────────────┤
                                       │    │ id (PK)     │
                                       │    │ question_id │──▶ questions.id
                                       │    │ content     │
                                       │    │ is_correct  │
                                       │    └─────────────┘
                                       │
                                       ▼
┌─────────────┐       ┌─────────────┐ ┌─────────────┐
│conversations│       │  messages   │ │ user_progress│
├─────────────┤       ├─────────────┤ ├─────────────┤
│ id (PK)     │◀──────│ id (PK)     │ │ id (PK)     │
│ user_id     │──┐    │ conversation│ │ user_id     │──▶ users.id
│ course_id   │──┼──▶ │ role        │ │ lesson_id   │──▶ lessons.id
│ title       │  │    │ content     │ │ completed   │
│ created_at  │  │    │ created_at  │ │ score       │
└─────────────┘  │    └─────────────┘ │ completed_at│
                 │                    └─────────────┘
                 │
                 ▼
┌─────────────┐
│  documents  │
├─────────────┤
│ id (PK)     │
│ course_id   │──▶ courses.id
│ name        │
│ file_path   │
│ file_type   │
│ file_size   │
│ created_at  │
└─────────────┘
```

---

## 📋 Table Definitions

### 1. users

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'student',
    avatar VARCHAR(500),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
```

| Column | Type | Mô tả |
|--------|------|-------|
| id | SERIAL | Primary key |
| email | VARCHAR(255) | Email (unique) |
| password | VARCHAR(255) | Password đã hash (bcrypt) |
| name | VARCHAR(100) | Tên hiển thị |
| role | VARCHAR(20) | Role: student, teacher, admin |
| avatar | VARCHAR(500) | URL avatar |
| is_active | BOOLEAN | Trạng thái active |
| created_at | TIMESTAMP | Thời gian tạo |
| updated_at | TIMESTAMP | Thời gian cập nhật |

### 2. courses

```sql
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    teacher_id INTEGER REFERENCES users(id),
    thumbnail VARCHAR(500),
    category VARCHAR(100),
    level VARCHAR(50) DEFAULT 'beginner',
    duration_hours INTEGER DEFAULT 0,
    is_published BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_courses_teacher ON courses(teacher_id);
CREATE INDEX idx_courses_category ON courses(category);
CREATE INDEX idx_courses_published ON courses(is_published);
```

| Column | Type | Mô tả |
|--------|------|-------|
| id | SERIAL | Primary key |
| title | VARCHAR(255) | Tên khóa học |
| description | TEXT | Mô tả chi tiết |
| teacher_id | INTEGER | FK → users.id |
| thumbnail | VARCHAR(500) | URL hình ảnh |
| category | VARCHAR(100) | Danh mục |
| level | VARCHAR(50) | Level: beginner, intermediate, advanced |
| duration_hours | INTEGER | Tổng thời gian (giờ) |
| is_published | BOOLEAN | Đã publish chưa |

### 3. lessons

```sql
CREATE TABLE lessons (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    video_url VARCHAR(500),
    "order" INTEGER NOT NULL,
    duration_minutes INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_lessons_course ON lessons(course_id);
CREATE INDEX idx_lessons_order ON lessons(course_id, "order");
```

| Column | Type | Mô tả |
|--------|------|-------|
| id | SERIAL | Primary key |
| course_id | INTEGER | FK → courses.id |
| title | VARCHAR(255) | Tiêu đề bài học |
| content | TEXT | Nội dung bài học |
| video_url | VARCHAR(500) | URL video |
| order | INTEGER | Thứ tự trong khóa |
| duration_minutes | INTEGER | Thời lượng (phút) |

### 4. enrollments

```sql
CREATE TABLE enrollments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    course_id INTEGER REFERENCES courses(id),
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed BOOLEAN DEFAULT false,
    completed_at TIMESTAMP,
    UNIQUE(user_id, course_id)
);

CREATE INDEX idx_enrollments_user ON enrollments(user_id);
CREATE INDEX idx_enrollments_course ON enrollments(course_id);
```

### 5. quizzes

```sql
CREATE TABLE quizzes (
    id SERIAL PRIMARY KEY,
    lesson_id INTEGER REFERENCES lessons(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    time_limit INTEGER DEFAULT 30,
    passing_score INTEGER DEFAULT 60,
    max_attempts INTEGER DEFAULT 3,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_quizzes_lesson ON quizzes(lesson_id);
```

### 6. questions

```sql
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER REFERENCES quizzes(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    type VARCHAR(50) DEFAULT 'single_choice',
    points INTEGER DEFAULT 1,
    "order" INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_questions_quiz ON questions(quiz_id);
```

| Type | Mô tả |
|------|-------|
| single_choice | Chọn 1 đáp án |
| multiple_choice | Chọn nhiều đáp án |
| true_false | Đúng/Sai |
| fill_blank | Điền vào chỗ trống |

### 7. answers

```sql
CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    question_id INTEGER REFERENCES questions(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT false,
    "order" INTEGER NOT NULL
);

CREATE INDEX idx_answers_question ON answers(question_id);
```

### 8. user_progress

```sql
CREATE TABLE user_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    lesson_id INTEGER REFERENCES lessons(id),
    completed BOOLEAN DEFAULT false,
    score INTEGER,
    time_spent INTEGER DEFAULT 0,
    completed_at TIMESTAMP,
    UNIQUE(user_id, lesson_id)
);

CREATE INDEX idx_progress_user ON user_progress(user_id);
CREATE INDEX idx_progress_lesson ON user_progress(lesson_id);
```

### 9. quiz_attempts

```sql
CREATE TABLE quiz_attempts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    quiz_id INTEGER REFERENCES quizzes(id),
    score INTEGER,
    total_points INTEGER,
    passed BOOLEAN DEFAULT false,
    answers JSONB,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE INDEX idx_attempts_user ON quiz_attempts(user_id);
CREATE INDEX idx_attempts_quiz ON quiz_attempts(quiz_id);
```

### 10. conversations

```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    course_id INTEGER REFERENCES courses(id),
    title VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_conversations_user ON conversations(user_id);
CREATE INDEX idx_conversations_course ON conversations(course_id);
```

### 11. messages

```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    tokens_used INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_messages_conversation ON messages(conversation_id);
```

| Role | Mô tả |
|------|-------|
| user | Tin nhắn từ user |
| assistant | Tin nhắn từ AI |
| system | System message |

### 12. documents

```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(50),
    file_size INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_documents_course ON documents(course_id);
```

---

## 📋 JSON Structure Definitions

### quiz_attempts.answers (JSONB)

```json
{
  "answers": [
    {
      "question_id": 1,
      "answer_ids": [1, 2],
      "text_answer": null
    },
    {
      "question_id": 2,
      "answer_ids": [3],
      "text_answer": null
    },
    {
      "question_id": 5,
      "answer_ids": [],
      "text_answer": "Python là ngôn ngữ lập trình"
    }
  ]
}
```

| Field | Type | Mô tả |
|-------|------|-------|
| question_id | integer | ID của câu hỏi |
| answer_ids | array[int] | Danh sách ID đáp án đã chọn |
| text_answer | string\|null | Câu trả lời text (cho fill_blank) |

### Course Full JSON Response

```json
{
  "id": 1,
  "title": "Python cơ bản từ A-Z",
  "description": "Khóa học Python dành cho người mới bắt đầu",
  "teacher_id": 2,
  "thumbnail": "https://example.com/images/python.jpg",
  "category": "programming",
  "level": "beginner",
  "duration_hours": 20,
  "is_published": true,
  "created_at": "2026-02-27T10:00:00Z",
  "updated_at": "2026-02-27T15:00:00Z",
  "teacher": {
    "id": 2,
    "name": "GV. Nguyễn Văn B",
    "email": "teacher@example.com",
    "avatar": "https://example.com/avatars/teacher.jpg"
  },
  "lessons_count": 10,
  "enrolled_count": 150
}
```

### Lesson Full JSON Response

```json
{
  "id": 1,
  "course_id": 1,
  "title": "Bài 1: Biến và kiểu dữ liệu",
  "content": "Nội dung bài học...",
  "video_url": "https://youtube.com/watch?v=xxx",
  "order": 1,
  "duration_minutes": 30,
  "created_at": "2026-02-27T10:00:00Z",
  "has_quiz": true,
  "is_completed": false,
  "quiz_id": 1
}
```

### Quiz with Questions JSON Response

```json
{
  "id": 1,
  "lesson_id": 1,
  "title": "Quiz: Biến và kiểu dữ liệu",
  "description": "Kiểm tra kiến thức bài 1",
  "time_limit": 30,
  "passing_score": 60,
  "max_attempts": 3,
  "questions": [
    {
      "id": 1,
      "content": "Python là gì?",
      "type": "single_choice",
      "points": 2,
      "order": 1,
      "answers": [
        {"id": 1, "content": "Ngôn ngữ lập trình", "order": 1},
        {"id": 2, "content": "Hệ điều hành", "order": 2},
        {"id": 3, "content": "Phần mềm", "order": 3},
        {"id": 4, "content": "Thương hiệu", "order": 4}
      ]
    },
    {
      "id": 2,
      "content": "Chọn các kiểu dữ liệu trong Python:",
      "type": "multiple_choice",
      "points": 3,
      "order": 2,
      "answers": [
        {"id": 5, "content": "int", "order": 1},
        {"id": 6, "content": "string", "order": 2},
        {"id": 7, "content": "array", "order": 3},
        {"id": 8, "content": "list", "order": 4}
      ]
    }
  ]
}
```

### Quiz Submit Request JSON

```json
{
  "answers": [
    {
      "question_id": 1,
      "answer_ids": [1]
    },
    {
      "question_id": 2,
      "answer_ids": [5, 6, 8]
    }
  ]
}
```

### Quiz Result JSON Response

```json
{
  "attempt_id": 1,
  "score": 80,
  "total_points": 10,
  "earned_points": 8,
  "passed": true,
  "completed_at": "2026-02-27T11:00:00Z",
  "details": [
    {
      "question_id": 1,
      "question_content": "Python là gì?",
      "correct": true,
      "selected_answer_ids": [1],
      "correct_answer_ids": [1],
      "points_earned": 2
    },
    {
      "question_id": 2,
      "question_content": "Chọn các kiểu dữ liệu trong Python:",
      "correct": false,
      "selected_answer_ids": [5, 6, 7],
      "correct_answer_ids": [5, 6, 8],
      "points_earned": 0
    }
  ]
}
```

### Chat Message JSON Response

```json
{
  "id": 1,
  "conversation_id": 1,
  "role": "user",
  "content": "Biến trong Python là gì?",
  "tokens_used": 15,
  "created_at": "2026-02-27T10:00:00Z"
}
```

### AI Response JSON

```json
{
  "id": 2,
  "conversation_id": 1,
  "role": "assistant",
  "content": "Biến trong Python là một tên định danh được sử dụng để lưu trữ giá trị. Ví dụ:\n\n```python\nname = \"Python\"\nage = 30\n```\n\nBiến có thể thay đổi giá trị và có nhiều kiểu dữ liệu khác nhau.",
  "tokens_used": 150,
  "created_at": "2026-02-27T10:00:05Z"
}
```

### Progress JSON Response

```json
{
  "total_courses": 5,
  "completed_courses": 2,
  "total_lessons": 50,
  "completed_lessons": 25,
  "total_time_spent_minutes": 1200,
  "average_score": 85.5,
  "courses": [
    {
      "course_id": 1,
      "course_title": "Python cơ bản",
      "total_lessons": 10,
      "completed_lessons": 5,
      "progress_percentage": 50,
      "last_accessed": "2026-02-27T10:00:00Z"
    }
  ]
}
```

### Pagination JSON Response

```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "size": 10,
  "pages": 10
}
```

---

## 📊 Indexes Summary

| Table | Index | Columns |
|-------|-------|---------|
| users | idx_users_email | email |
| users | idx_users_role | role |
| courses | idx_courses_teacher | teacher_id |
| courses | idx_courses_category | category |
| lessons | idx_lessons_course | course_id |
| lessons | idx_lessons_order | course_id, order |
| messages | idx_messages_conversation | conversation_id |

---

## 🔐 Data Constraints

### Business Rules
- User không thể tự đổi role (chỉ admin)
- Lesson order phải unique trong course
- Quiz attempt không vượt quá max_attempts
- Score từ 0-100
- Password phải hash với bcrypt

### Referential Integrity
- CASCADE DELETE: lessons khi xóa course
- CASCADE DELETE: questions khi xóa quiz
- CASCADE DELETE: messages khi xóa conversation
- RESTRICT: không xóa user nếu có courses

---

*Tài liệu này định nghĩa cấu trúc database cho toàn bộ hệ thống.*
