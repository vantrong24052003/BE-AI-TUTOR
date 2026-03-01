# BE AI TUTOR - Database Design

> Database schema chi tiết cho hệ thống AI Tutor
>
> **Phiên bản**: 3.0
> **Cập nhật**: Thêm Flashcards, Exercises, Notes, Bookmarks, AI Services

---

## 📊 ER Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DATABASE SCHEMA v3.0                                 │
│                    Two Roles: ADMIN + USER                                   │
│                    21 Tables Total                                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│    users    │       │  categories │       │   courses   │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id (PK)     │       │ id (PK)     │       │ id (PK)     │
│ email       │       │ name        │◀──────│ category_id │
│ password    │       │ slug        │       │ title       │
│ name        │       │ description │       │ description │
│ avatar      │       │ icon        │       │ creator_id  │──┐
│ role        │       │ color       │       │ thumbnail   │  │
│ is_active   │       │ order       │       │ level       │  │
│ created_at  │       │ is_active   │       │ is_published│  │
│ updated_at  │       │ created_at  │       │ created_at  │  │
└─────────────┘       │ updated_at  │       │ updated_at  │  │
      │               └─────────────┘       └─────────────┘  │
      │                     │                    │            │
      │                     │                    │            │
      ▼                     ▼                    ▼            │
┌─────────────┐       ┌─────────────┐                          │
│  lessons    │       │ enrollments │                          │
├─────────────┤       ├─────────────┤                          │
│ id (PK)     │       │ id (PK)     │                          │
│ course_id   │──────▶│ user_id     │──────────────────────────┘
│ title       │       │ course_id   │
│ content     │       │ enrolled_at │
│ video_url   │       │ completed   │
│ order       │       │ completed_at│
│ duration    │       │ updated_at  │
│ created_at  │       └─────────────┘
│ updated_at  │
└─────────────┘
      │
      ├──────────────────────┬──────────────────────┬──────────────────────┐
      │                      │                      │                      │
      ▼                      ▼                      ▼                      ▼
┌─────────────┐       ┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   quizzes   │       │  exercises  │       │  flashcards │       │   notes     │
├─────────────┤       ├─────────────┤       ├─────────────┤       ├─────────────┤
│ id (PK)     │       │ id (PK)     │       │ id (PK)     │       │ id (PK)     │
│ lesson_id   │──────▶│ lesson_id   │──────▶│ lesson_id   │──────▶│ user_id     │
│ creator_id  │       │ title       │       │ front       │       │ lesson_id   │
│ title       │       │ description │       │ back        │       │ content     │
│ time_limit  │       │ type        │       │ hint        │       │ timestamp   │
│ passing     │       │ max_score   │       │ order       │       │ created_at  │
│ max_attempts│       │ order       │       │ created_at  │       │ updated_at  │
│ created_at  │       │ created_at  │       │ updated_at  │       └─────────────┘
│ updated_at  │       │ updated_at  │       └─────────────┘
└─────────────┘       └─────────────┘              │
      │                    │                      │
      │                    │                      ▼
      │                    │              ┌─────────────┐
      │                    │              │flashcard_   │
      │                    │              │ reviews     │
      │                    │              ├─────────────┤
      │                    │              │ id (PK)     │
      │                    │              │ user_id     │
      │                    │              │ flashcard_id│
      │                    │              │ quality     │
      │                    │              │ ease_factor │
      │                    │              │ interval    │
      │                    │              │ next_review │
      │                    │              │ reviewed_at │
      │                    │              └─────────────┘
      ▼                    ▼
┌─────────────┐       ┌─────────────┐
│  questions  │       │  exercise_  │
├─────────────┤       │ submissions │
│ id (PK)     │       ├─────────────┤
│ quiz_id     │       │ id (PK)     │
│ content     │       │ user_id     │
│ type        │       │ exercise_id │
│ points      │       │ answer      │
│ order       │       │ file_url    │
│ created_at  │       │ score       │
│ updated_at  │       │ feedback    │
└─────────────┘       │ ai_feedback │
      │               │ status      │
      ▼               │ submitted_at│
┌─────────────┐       │ graded_at   │
│  answers    │       │ updated_at  │
├─────────────┤       └─────────────┘
│ id (PK)     │
│ question_id │       ┌─────────────┐       ┌─────────────┐
│ content     │       │conversations│       │  messages   │
│ is_correct  │       ├─────────────┤       ├─────────────┤
│ order       │       │ id (PK)     │◀──────│ id (PK)     │
│ created_at  │       │ user_id     │       │ conversation│
└─────────────┘       │ course_id   │       │ role        │
                      │ context_type│       │ content     │
┌─────────────┐       │ context_id  │       │ tokens_used │
│quiz_attempts│       │ title       │       │ created_at  │
├─────────────┤       │ created_at  │       └─────────────┘
│ id (PK)     │       │ updated_at  │
│ user_id     │       └─────────────┘
│ quiz_id     │
│ score       │       ┌─────────────┐       ┌─────────────┐
│ total_points│       │  documents  │       │  bookmarks  │
│ passed      │       ├─────────────┤       ├─────────────┤
│ answers     │       │ id (PK)     │       │ id (PK)     │
│ started_at  │       │ course_id   │       │ user_id     │
│ completed_at│       │ creator_id  │       │ lesson_id   │
│ updated_at  │       │ name        │       │ note        │
└─────────────┘       │ file_path   │       │ created_at  │
                      │ file_type   │       └─────────────┘
┌─────────────┐       │ file_size   │
│user_progress│       │ created_at  │
├─────────────┤       │ updated_at  │
│ id (PK)     │       └─────────────┘
│ user_id     │
│ lesson_id   │       ┌─────────────┐       ┌─────────────┐
│ completed   │       │ai_quiz_     │       │ ai_summaries│
│ score       │       │ generations │       ├─────────────┤
│ time_spent  │       ├─────────────┤       │ id (PK)     │
│ completed_at│       │ id (PK)     │       │ user_id     │
│ updated_at  │       │ user_id     │       │ lesson_id   │
└─────────────┘       │ lesson_id   │       │ summary     │
                      │ quiz_id     │       │ key_points  │
                      │ prompt      │       │ keywords    │
                      │ settings    │       │ created_at  │
                      │ created_at  │       └─────────────┘
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
    avatar VARCHAR(500),
    role VARCHAR(20) DEFAULT 'user' CHECK (role IN ('admin', 'user')),
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
| avatar | VARCHAR(500) | URL avatar |
| role | VARCHAR(20) | `admin` hoặc `user` |
| is_active | BOOLEAN | Trạng thái active |

---

### 2. categories

```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    icon VARCHAR(50),
    color VARCHAR(20),
    "order" INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_categories_slug ON categories(slug);
CREATE INDEX idx_categories_active ON categories(is_active);
```

---

### 3. courses

```sql
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    creator_id INTEGER REFERENCES users(id),
    category_id INTEGER REFERENCES categories(id),
    thumbnail VARCHAR(500),
    level VARCHAR(50) DEFAULT 'beginner',
    duration_hours INTEGER DEFAULT 0,
    is_published BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_courses_creator ON courses(creator_id);
CREATE INDEX idx_courses_category ON courses(category_id);
CREATE INDEX idx_courses_published ON courses(is_published);
```

| Level | Mô tả |
|-------|-------|
| beginner | Dành cho người mới bắt đầu |
| intermediate | Dành cho người có nền tảng |
| advanced | Dành cho người có kinh nghiệm |

---

### 4. lessons

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

---

### 5. enrollments

```sql
CREATE TABLE enrollments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    course_id INTEGER REFERENCES courses(id),
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed BOOLEAN DEFAULT false,
    completed_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, course_id)
);

CREATE INDEX idx_enrollments_user ON enrollments(user_id);
CREATE INDEX idx_enrollments_course ON enrollments(course_id);
```

---

### 6. quizzes

```sql
CREATE TABLE quizzes (
    id SERIAL PRIMARY KEY,
    lesson_id INTEGER REFERENCES lessons(id) ON DELETE CASCADE,
    creator_id INTEGER REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    time_limit INTEGER DEFAULT 30,
    passing_score INTEGER DEFAULT 60,
    max_attempts INTEGER DEFAULT 3,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_quizzes_lesson ON quizzes(lesson_id);
CREATE INDEX idx_quizzes_creator ON quizzes(creator_id);
```

| Column | Type | Mô tả |
|--------|------|-------|
| time_limit | INTEGER | Thời gian làm (phút), 0 = unlimited |
| passing_score | INTEGER | Điểm đạt (%) mặc định 60 |
| max_attempts | INTEGER | Số lần làm tối đa, 0 = unlimited |

---

### 7. questions

```sql
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER REFERENCES quizzes(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    type VARCHAR(50) DEFAULT 'single_choice',
    points INTEGER DEFAULT 1,
    "order" INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_questions_quiz ON questions(quiz_id);
```

| Type | Mô tả |
|------|-------|
| single_choice | Chọn 1 đáp án đúng |
| multiple_choice | Chọn nhiều đáp án đúng |
| true_false | Đúng/Sai |
| fill_blank | Điền vào chỗ trống |

---

### 8. answers

```sql
CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    question_id INTEGER REFERENCES questions(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT false,
    "order" INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(question_id, "order")
);

CREATE INDEX idx_answers_question ON answers(question_id);
```

---

### 9. quiz_attempts

```sql
CREATE TABLE quiz_attempts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    quiz_id INTEGER REFERENCES quizzes(id),
    score INTEGER,
    total_points INTEGER,
    passed BOOLEAN DEFAULT false,
    answers JSONB NOT NULL DEFAULT '[]',
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_attempts_user ON quiz_attempts(user_id);
CREATE INDEX idx_attempts_quiz ON quiz_attempts(quiz_id);
```

#### 📝 JSON Structure: answers

```json
[
  {
    "question_id": 1,
    "answer_ids": [1, 2]
  },
  {
    "question_id": 2,
    "answer_ids": [5]
  }
]
```

| Field | Type | Mô tả |
|-------|------|-------|
| question_id | integer | ID của câu hỏi |
| answer_ids | array[integer] | Các ID của đáp án đã chọn |

---

### 10. exercises

```sql
CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    lesson_id INTEGER REFERENCES lessons(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    type VARCHAR(50) DEFAULT 'text',
    max_score INTEGER DEFAULT 100,
    max_attempts INTEGER DEFAULT 3,
    "order" INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_exercises_lesson ON exercises(lesson_id);
CREATE INDEX idx_exercises_order ON exercises(lesson_id, "order");
```

| Type | Mô tả |
|------|-------|
| text | Trả lời bằng văn bản |
| code | Viết code (có thể test tự động) |
| file | Upload file |
| multiple | Nhiều câu hỏi nhỏ (JSON) |

---

### 11. exercise_submissions

```sql
CREATE TABLE exercise_submissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    exercise_id INTEGER REFERENCES exercises(id) ON DELETE CASCADE,
    answer TEXT,
    file_url VARCHAR(500),
    score INTEGER,
    feedback TEXT,
    ai_feedback JSONB,
    status VARCHAR(20) DEFAULT 'pending',
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    graded_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_submissions_user ON exercise_submissions(user_id);
CREATE INDEX idx_submissions_exercise ON exercise_submissions(exercise_id);
CREATE INDEX idx_submissions_status ON exercise_submissions(status);
```

| Status | Mô tả |
|--------|-------|
| pending | Chờ chấm |
| grading | Đang chấm bởi AI |
| graded | Đã chấm xong |
| needs_review | Cần giáo viên review |

#### 📝 JSON Structure: ai_feedback

```json
{
  "score": 85,
  "overall_comment": "Bài làm tốt, code chạy đúng...",
  "strengths": [
    "Logic chặt chẽ",
    "Code dễ đọc"
  ],
  "improvements": [
    "Có thể tối ưu vòng lặp",
    "Nên thêm comment"
  ],
  "code_analysis": {
    "complexity": "O(n)",
    "style_score": 8,
    "correctness": true
  },
  "suggestions": [
    "Thử dùng list comprehension",
    "Thêm error handling"
  ]
}
```

| Field | Type | Mô tả |
|-------|------|-------|
| score | integer | Điểm AI chấm (0-100) |
| overall_comment | string | Nhận xét chung |
| strengths | array[string] | Điểm mạnh |
| improvements | array[string] | Điểm cần cải thiện |
| code_analysis | object | Phân tích code (nếu là code) |
| suggestions | array[string] | Gợi ý cải thiện |

---

### 12. flashcards

```sql
CREATE TABLE flashcards (
    id SERIAL PRIMARY KEY,
    lesson_id INTEGER REFERENCES lessons(id) ON DELETE CASCADE,
    front TEXT NOT NULL,
    back TEXT NOT NULL,
    hint TEXT,
    "order" INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_flashcards_lesson ON flashcards(lesson_id);
CREATE INDEX idx_flashcards_order ON flashcards(lesson_id, "order");
```

| Column | Type | Mô tả |
|--------|------|-------|
| front | TEXT | Mặt trước (câu hỏi/thuật ngữ) |
| back | TEXT | Mặt sau (câu trả lời/định nghĩa) |
| hint | TEXT | Gợi ý (optional) |

---

### 13. flashcard_reviews

> **Spaced Repetition System (SRS)** sử dụng thuật toán **SM-2**

```sql
CREATE TABLE flashcard_reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    flashcard_id INTEGER REFERENCES flashcards(id) ON DELETE CASCADE,
    quality INTEGER NOT NULL CHECK (quality >= 0 AND quality <= 5),
    ease_factor DECIMAL(3,2) DEFAULT 2.50,
    interval INTEGER DEFAULT 0,
    repetitions INTEGER DEFAULT 0,
    next_review_at TIMESTAMP,
    last_reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, flashcard_id)
);

CREATE INDEX idx_flashcard_reviews_user ON flashcard_reviews(user_id);
CREATE INDEX idx_flashcard_reviews_next ON flashcard_reviews(user_id, next_review_at);
```

| Column | Type | Mô tả |
|--------|------|-------|
| quality | INTEGER | Đánh giá chất lượng nhớ (0-5) |
| ease_factor | DECIMAL | Hệ số dễ nhớ (mặc định 2.5) |
| interval | INTEGER | Số ngày đến lần review tiếp |
| repetitions | INTEGER | Số lần review liên tiếp đúng |
| next_review_at | TIMESTAMP | Thời gian review tiếp theo |

#### Quality Rating (SM-2 Algorithm)

| Quality | Mô tả | Action |
|---------|-------|--------|
| 0 | Complete blackout | Reset repetitions, interval = 1 |
| 1 | Incorrect, but recognized | Reset repetitions, interval = 1 |
| 2 | Incorrect, easy to recall | Reset repetitions, interval = 1 |
| 3 | Correct with difficulty | Continue, increase interval |
| 4 | Correct after hesitation | Continue, increase interval |
| 5 | Perfect response | Continue, increase interval |

---

### 14. notes

```sql
CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    lesson_id INTEGER REFERENCES lessons(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    timestamp_seconds INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_notes_user ON notes(user_id);
CREATE INDEX idx_notes_lesson ON notes(lesson_id);
```

| Column | Type | Mô tả |
|--------|------|-------|
| content | TEXT | Nội dung ghi chú |
| timestamp_seconds | INTEGER | Thời điểm trong video (nếu có) |

---

### 15. bookmarks

```sql
CREATE TABLE bookmarks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    lesson_id INTEGER REFERENCES lessons(id) ON DELETE CASCADE,
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, lesson_id)
);

CREATE INDEX idx_bookmarks_user ON bookmarks(user_id);
CREATE INDEX idx_bookmarks_lesson ON bookmarks(lesson_id);
```

---

### 16. conversations

```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    course_id INTEGER REFERENCES courses(id),
    context_type VARCHAR(20) DEFAULT 'general',
    context_id INTEGER,
    title VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_conversations_user ON conversations(user_id);
CREATE INDEX idx_conversations_course ON conversations(course_id);
CREATE INDEX idx_conversations_context ON conversations(context_type, context_id);
```

| Context Type | Mô tả | context_id |
|--------------|-------|------------|
| general | Hỏi đáp chung | null |
| lesson | Hỏi về bài học cụ thể | lesson_id |
| exercise | Hỏi về bài tập | exercise_id |
| flashcard | Hỏi về flashcard | flashcard_id |

---

### 17. messages

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
| system | System message (context) |

---

### 18. documents

```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses(id) ON DELETE CASCADE,
    creator_id INTEGER REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(50),
    file_size INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_documents_course ON documents(course_id);
CREATE INDEX idx_documents_creator ON documents(creator_id);
```

| File Type | Extension |
|-----------|-----------|
| pdf | .pdf |
| docx | .docx |
| pptx | .pptx |
| image | .png, .jpg, .jpeg |
| code | .py, .js, .java |

---

### 19. user_progress

```sql
CREATE TABLE user_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    lesson_id INTEGER REFERENCES lessons(id),
    completed BOOLEAN DEFAULT false,
    score INTEGER,
    time_spent INTEGER DEFAULT 0,
    completed_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, lesson_id)
);

CREATE INDEX idx_progress_user ON user_progress(user_id);
CREATE INDEX idx_progress_lesson ON user_progress(lesson_id);
```

| Column | Type | Mô tả |
|--------|------|-------|
| completed | BOOLEAN | Đã hoàn thành bài học |
| score | INTEGER | Điểm quiz (nếu có) |
| time_spent | INTEGER | Thời gian học (giây) |

---

### 20. ai_quiz_generations

```sql
CREATE TABLE ai_quiz_generations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    lesson_id INTEGER REFERENCES lessons(id),
    quiz_id INTEGER REFERENCES quizzes(id),
    prompt TEXT,
    settings JSONB NOT NULL DEFAULT '{}',
    tokens_used INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ai_quiz_user ON ai_quiz_generations(user_id);
CREATE INDEX idx_ai_quiz_lesson ON ai_quiz_generations(lesson_id);
```

#### 📝 JSON Structure: settings

```json
{
  "num_questions": 5,
  "difficulty": "medium",
  "question_types": ["single_choice", "multiple_choice"],
  "language": "vi"
}
```

| Field | Type | Mô tả |
|-------|------|-------|
| num_questions | integer | Số câu hỏi muốn tạo |
| difficulty | string | Độ khó: easy/medium/hard |
| question_types | array | Các loại câu hỏi |
| language | string | Ngôn ngữ: vi/en |

---

### 21. ai_summaries

```sql
CREATE TABLE ai_summaries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    lesson_id INTEGER REFERENCES lessons(id),
    summary TEXT NOT NULL,
    key_points JSONB NOT NULL DEFAULT '[]',
    keywords JSONB NOT NULL DEFAULT '[]',
    tokens_used INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ai_summaries_user ON ai_summaries(user_id);
CREATE INDEX idx_ai_summaries_lesson ON ai_summaries(lesson_id);
```

#### 📝 JSON Structure: key_points

```json
[
  "Python là ngôn ngữ lập trình thông dịch",
  "Biến dùng để lưu trữ dữ liệu",
  "Có nhiều kiểu dữ liệu: int, float, string, bool"
]
```

#### 📝 JSON Structure: keywords

```json
["python", "biến", "kiểu dữ liệu", "int", "string"]
```

---

## 📊 Tables Summary

| # | Table | Mô tả | JSON Fields |
|---|-------|-------|-------------|
| 1 | users | Người dùng | - |
| 2 | categories | Danh mục khóa học | - |
| 3 | courses | Khóa học | - |
| 4 | lessons | Bài học | - |
| 5 | enrollments | Đăng ký khóa học | - |
| 6 | quizzes | Bài kiểm tra | - |
| 7 | questions | Câu hỏi quiz | - |
| 8 | answers | Đáp án quiz | - |
| 9 | quiz_attempts | Lần làm quiz | answers |
| 10 | exercises | Bài tập thực hành | - |
| 11 | exercise_submissions | Bài nộp | ai_feedback |
| 12 | flashcards | Thẻ ghi nhớ | - |
| 13 | flashcard_reviews | Review flashcard (SRS) | - |
| 14 | notes | Ghi chú cá nhân | - |
| 15 | bookmarks | Đánh dấu bài học | - |
| 16 | conversations | Hội thoại AI | - |
| 17 | messages | Tin nhắn | - |
| 18 | documents | Tài liệu | - |
| 19 | user_progress | Tiến độ học | - |
| 20 | ai_quiz_generations | Quiz AI tạo | settings |
| 21 | ai_summaries | Tóm tắt AI | key_points, keywords |

---

## 📊 Indexes Summary

| Table | Index | Purpose |
|-------|-------|---------|
| users | idx_users_email | Tìm user theo email |
| users | idx_users_role | Filter theo role |
| categories | idx_categories_slug | Tìm category theo slug |
| courses | idx_courses_creator | Tìm courses theo creator |
| courses | idx_courses_category | Filter theo category |
| lessons | idx_lessons_course | Tìm lessons theo course |
| quizzes | idx_quizzes_lesson | Tìm quiz theo lesson |
| exercises | idx_exercises_lesson | Tìm exercises theo lesson |
| exercise_submissions | idx_submissions_status | Filter theo status |
| flashcards | idx_flashcards_lesson | Tìm flashcards theo lesson |
| flashcard_reviews | idx_flashcard_reviews_next | Tìm cards cần review |
| conversations | idx_conversations_context | Filter theo context |

---

## 🔐 Access Control (2 Roles: Admin + User)

| Resource | Public | User | Admin |
|----------|--------|------|-------|
| **Courses** |
| List courses | ✅ | ✅ | ✅ |
| Create course | - | ✅ | ✅ |
| Update course | - | Owner | ✅ |
| Delete course | - | Owner | ✅ |
| **Lessons** |
| View lessons | ✅ | ✅ | ✅ |
| Create lesson | - | Owner | ✅ |
| **Quizzes** |
| View quiz | - | Enrolled | ✅ |
| Submit quiz | - | Enrolled | ✅ |
| **Exercises** |
| View exercises | - | Enrolled | ✅ |
| Submit exercise | - | Enrolled | ✅ |
| **Flashcards** |
| View flashcards | - | Enrolled | ✅ |
| Review flashcard | - | Enrolled | ✅ |
| **Notes & Bookmarks** |
| Create/View/Update | - | Self | ✅ |
| **AI Services** |
| Chat with AI | - | ✅ | ✅ |
| Generate Quiz | - | ✅ | ✅ |
| Summarize | - | ✅ | ✅ |
| Solve Exercise | - | ✅ | ✅ |
| **Admin Only** |
| Manage users | - | - | ✅ |
| Manage categories | - | - | ✅ |

---

*Tài liệu này định nghĩa cấu trúc database cho toàn bộ hệ thống.*
*Version: 3.0 - 21 tables, JSON structures defined, includes Flashcards, Exercises, Notes, Bookmarks, AI Services*
