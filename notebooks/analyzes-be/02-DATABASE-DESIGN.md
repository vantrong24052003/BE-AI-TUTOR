# BE AI TUTOR - Database Design

> Database schema chi tiết cho hệ thống AI Tutor - Document-RAG Based
>
> **Phiên bản**: 5.1 (Tương thích 100% tài liệu Đặc tả hệ thống Gia sư AI)
> **Cập nhật**: Đã đồng bộ UUID v4, 20 Tables, và kiến trúc Document-RAG.

---

## 📊 ER Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DATABASE SCHEMA v5.0                                 │
│                    Learning & Assessment Focused Architecture                 │
│                    20 Tables Total                                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              USERS & DOCUMENTS                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────────┐                    ┌─────────────────┐                    │
│   │    users    │                    │    documents    │                    │
│   ├─────────────┤                    ├─────────────────┤                    │
│   │ id (PK)     │◀───────────────────│ user_id (FK)    │                    │
│   │ email       │                    │ id (PK)         │                    │
│   │ google_id   │                    │ title           │                    │
│   │ name        │                    │ filename        │                    │
│   │ avatar      │                    │ file_path       │                    │
│   │ role        │                    │ file_type       │                    │
│   │ last_login  │                    │ file_size       │                    │
│   │ created_at  │                    │ status          │                    │
│   │ updated_at  │                    │ page_count      │                    │
│   └─────────────┘                    │ error_message   │                    │
│         │                            │ created_at      │                    │
│         │                            │ updated_at      │                    │
│         │                                    └─────────────────┘                    │
│         │                                    │                              │
│         │                                    │                              │
│         │            ┌───────────────────────┼───────────────────────┐      │
│         │            │                       │                       │      │
│         │            ▼                       ▼                       ▼      │
│         │   ┌─────────────────┐     ┌─────────────────┐     ┌─────────────┐ │
│         │   │ document_chunks │     │    flashcards   │     │   quizzes   │ │
│         │   ├─────────────────┤     ├─────────────────┤     ├─────────────┤ │
│         │   │ id (PK)         │     │ id (PK)         │     │ id (PK)     │ │
│         │   │ document_id(FK) │     │ document_id(FK) │     │document_id  │ │
│         │   │ chunk_index     │     │ front           │     │ title       │ │
│         │   │ content         │     │ back            │     │ description │ │
│         │   │ page_number     │     │ hint            │     │time_limit   │ │
│         │   │ embedding_id    │     │ order           │     │passing_score│ │
│         │   │ created_at      │     │ is_ai_generated │     │max_attempts │ │
│         │   └─────────────────┘     │ created_at      │     │is_ai_gen    │ │
│         │                           └─────────────────┘     │ created_at  │ │
│         │                                   │               └─────────────┘ │
│         │                                   │                       │        │
│         │                                   ▼                       ▼        │
│         │                           ┌─────────────────┐     ┌─────────────┐ │
│         │                           │flashcard_reviews│     │quiz_questions│
│         │                           ├─────────────────┤     ├─────────────┤ │
│         │                           │ id (PK)         │     │ id (PK)     │ │
│         │                           │ user_id (FK)    │     │ quiz_id(FK) │ │
│         │                           │ flashcard_id(FK)│     │ content     │ │
│         │                           │ quality         │     │ explanation │ │
│         │                           │ ease_factor     │     │ order       │ │
│         │                           │ interval        │     │ points      │ │
│         │                           │ repetitions     │     └─────────────┘ │
│         │                           │ next_review_at  │             │        │
│         │                           │ last_review_at  │             ▼        │
│         │                           │ total_reviews   │     ┌─────────────┐ │
│         │                           └─────────────────┘     │quiz_attempts│ │
│         │                                                   ├─────────────┤ │
│         │                                                   │ id (PK)     │ │
│         │                                                   │ quiz_id(FK) │ │
│         │                                                   │ user_id(FK) │ │
│         │                                                   │ score       │ │
│         │                                                   │ passed      │ │
│         │                                                   │ answers     │ │
│         │                                                   │ started_at  │ │
│         │                                                   │ completed_at│ │
│         │                                                   └─────────────┘ │
│         │                                                                   │
│         ├───────────────────────────────────────────────────────────────────┤
│         │                        LEARNING PATHS & PROGRESS                   │
│         │                                                                   │
│         │   ┌─────────────────┐                                             │
│         │   │ learning_paths  │                                             │
│         │   ├─────────────────┤                                             │
│         │   │ id (PK)         │◀────────────────────────────────────────────┐
│         │   │ document_id(FK) │                                             │
│         │   │ user_id (FK)    │                                             │
│         │   │ title           │                                             │
│         │   │ description     │                                             │
│         │   │ created_at      │                                             │
│         │   │ updated_at      │                                             │
│         │   └─────────────────┘                                             │
│         │         │                                                         │
│         │         ▼                                                         │
│         │   ┌─────────────────┐                                             │
│         │   │  path_stages    │                                             │
│         │   ├─────────────────┤                                             │
│         │   │ id (PK)         │                                             │
│         │   │ path_id (FK)    │                                             │
│         │   │ title           │                                             │
│         │   │ order           │                                             │
│         │   │ created_at      │                                             │
│         │   └─────────────────┘                                             │
│         │         │                                                         │
│         │         ▼                                                         │
│         │   ┌─────────────────┐                                             │
│         │   │  path_lessons   │                                             │
│         │   ├─────────────────┤                                             │
│         │   │ id (PK)         │                                             │
│         │   │ stage_id (FK)   │                                             │
│         │   │ title           │                                             │
│         │   │ content_summary │                                             │
│         │   │ order           │                                             │
│         │   │ created_at      │                                             │
│         │   └─────────────────┘                                             │
│         │         │                                                         │
│         │         ▼                                                         │
│         │   ┌─────────────────┐                                             │
│         │   │ lesson_progress │                                             │
│         │   ├─────────────────┤                                             │
│         │   │ id (PK)         │                                             │
│         │   │ user_id (FK)    │                                             │
│         │   │ lesson_id (FK)  │                                             │
│         │   │ status          │                                             │
│         │   │ completed_at    │                                             │
│         │   └─────────────────┘                                             │
│         │                                                                   │
│         ├───────────────────────────────────────────────────────────────────┤
│         │                        CHAT & AI SERVICES                          │
│         │                                                                   │
│         │   ┌─────────────────┐     ┌─────────────────┐                     │
│         │   │  chat_sessions  │     │  chat_messages  │                     │
│         │   ├─────────────────┤     ├─────────────────┤                     │
│         │   │ id (PK)         │◀────│ session_id (FK) │                     │
│         │   │ user_id (FK)    │     │ id (PK)         │                     │
│         │   │ document_id(FK) │     │ role            │                     │
│         │   │ title           │     │ content         │                     │
│         │   │ created_at      │     │ tokens_used     │                     │
│         │   │ updated_at      │     │ created_at      │                     │
│         │   └─────────────────┘     └─────────────────┘                     │
│         │                                                                   │
│         │   ┌─────────────────┐     ┌───────────────────┐                   │
│         │   │ ai_generations  │     │ homework_solutions│                   │
│         │   ├─────────────────┤     ├───────────────────┤                   │
│         │   │ id (PK)         │     │ id (PK)           │                   │
│         │   │ user_id (FK)    │     │ user_id (FK)      │                   │
│         │   │ document_id(FK) │     │ problem_text      │                   │
│         │   │ type (Path/Sol) │     │ solution_steps    │                   │
│         │   │ tokens_used     │     │ final_answer      │                   │
│         │   │ result          │     │ subject           │                   │
│         │   │ created_at      │     │ tokens_used       │                   │
│         │   └─────────────────┘     │ created_at        │                   │
│         │                             └───────────────────┘                   │
│         │                                                                   │
│         ├───────────────────────────────────────────────────────────────────┤
│         │                        NOTES & BOOKMARKS & TEST MATRICES           │
│         │                                                                   │
│         │   ┌─────────────────┐     ┌─────────────────┐                     │
│         │   │     notes       │     │    bookmarks    │                     │
│         │   ├─────────────────┤     ├─────────────────┤                     │
│         │   │ id (PK)         │     │ id (PK)         │                     │
│         │   │ user_id (FK)    │     │ user_id (FK)    │                     │
│         │   │ document_id(FK) │     │ document_id(FK) │                     │
│         │   │ content         │     │ note            │                     │
│         │   │ page_number     │     │ created_at      │                     │
│         │   │ created_at      │     └─────────────────┘                     │
│         │   │ updated_at      │                                             │
│         │   └─────────────────┘                                             │
│         │                                                                   │
│         │   ┌─────────────────┐                                             │
│         │   │  test_matrices  │                                             │
│         │   ├─────────────────┤                                             │
│         │   │ id (PK)         │                                             │
│         │   │ document_id(FK) │                                             │
│         │   │ user_id (FK)    │                                             │
│         │   │ title           │                                             │
│         │   │ total_questions │                                             │
│         │   │ created_at      │                                             │
│         │   └─────────────────┘                                             │
│         │         │                                                         │
│         │         ▼                                                         │
│         │   ┌───────────────────┐                                           │
│         │   │  matrix_criteria  │                                           │
│         │   ├───────────────────┤                                           │
│         │   │ id (PK)           │                                           │
│         │   │ matrix_id (FK)    │                                           │
│         │   │ topic             │                                           │
│         │   │ difficulty        │                                           │
│         │   │ question_count    │                                           │
│         │   │ points_per_question │                                         │
│         │   └───────────────────┘                                           │
└─────────┴───────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         RAG SYSTEM (Hybrid)                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   PostgreSQL (document_chunks)          ChromaDB (Vector Store)              │
│   ┌─────────────────────────┐          ┌─────────────────────────┐          │
│   │ - chunk metadata         │          │ - embeddings            │          │
│   │ - content text           │◀────────▶│ - similarity search     │          │
│   │ - embedding_id reference │          │ - collection per doc    │          │
│   └─────────────────────────┘          └─────────────────────────┘          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Table Definitions

### 1. users

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    google_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    avatar VARCHAR(500),
    role VARCHAR(20) DEFAULT 'user' CHECK (role IN ('admin', 'user')),
    last_login TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_google_id ON users(google_id);
CREATE INDEX idx_users_role ON users(role);
```

| Column | Type | Mo ta |
|--------|------|-------|
| id | SERIAL | Primary key |
| email | VARCHAR(255) | Email (unique) |
| google_id | VARCHAR(255) | Google ID (unique) |
| name | VARCHAR(100) | Ten hien thi |
| avatar | VARCHAR(500) | URL avatar |
| role | VARCHAR(20) | `admin` hoac `user` |
| last_login | TIMESTAMP | Lan dang nhap cuoi |

---

### 2. documents

```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(10) NOT NULL CHECK (file_type IN ('pdf', 'docx')),
    file_size INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'ready', 'failed')),
    page_count INTEGER,
    error_message TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_documents_user ON documents(user_id);
CREATE INDEX idx_documents_status ON documents(status);
CREATE INDEX idx_documents_created ON documents(created_at DESC);
```

| Column | Type | Mo ta |
|--------|------|-------|
| id | SERIAL | Primary key |
| user_id | INTEGER | FK -> users (owner) |
| title | VARCHAR(255) | Tieu de tai lieu |
| filename | VARCHAR(255) | Ten file goc |
| file_path | VARCHAR(500) | Duong dan file tren server |
| file_type | VARCHAR(10) | pdf/docx |
| file_size | INTEGER | Kich thuoc (bytes) |
| status | VARCHAR(20) | pending/processing/ready/failed |
| page_count | INTEGER | So trang |
| error_message | TEXT | Loi neu processing that bai |

#### Document Processing Flow

```
┌─────────┐     ┌─────────┐     ┌───────────┐     ┌──────────┐
│  UPLOAD │────▶│ PENDING │────▶│ PROCESSING│────▶│  READY   │
│ (moi)   │     │ (cho)   │     │ (xu ly)   │     │ (san sang)│
└─────────┘     └─────────┘     └───────────┘     └──────────┘
                                      │
                                      ▼
                                ┌──────────┐
                                │  FAILED  │
                                └──────────┘
```

---

### 3. document_chunks

> **RAG System** - Luu tru chunks de truy van thong tin

```sql
CREATE TABLE document_chunks (
    id SERIAL PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    page_number INTEGER,
    embedding_id VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(document_id, chunk_index)
);

CREATE INDEX idx_chunks_document ON document_chunks(document_id);
CREATE INDEX idx_chunks_embedding ON document_chunks(embedding_id);
```

| Column | Type | Mo ta |
|--------|------|-------|
| id | SERIAL | Primary key |
| document_id | INTEGER | FK -> documents |
| chunk_index | INTEGER | Thu tu chunk (0, 1, 2, ...) |
| content | TEXT | Noi dung chunk |
| page_number | INTEGER | So trang (neu applicable) |
| embedding_id | VARCHAR(100) | ID trong vector store (ChromaDB) |

#### RAG Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      RAG PROCESSING FLOW                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. UPLOAD DOCUMENT                                              │
│     └──▶ Extract text from PDF/DOCX                              │
│                                                                  │
│  2. CHUNKING                                                     │
│     └──▶ Split text into chunks (1000 chars, 200 overlap)        │
│                                                                  │
│  3. EMBEDDING                                                    │
│     └──▶ Generate embeddings (OpenAI/Claude)                     │
│     └──▶ Store in ChromaDB                                       │
│                                                                  │
│  4. QUERY ( khi user hoi)                                        │
│     └──▶ Embed query                                             │
│     └──▶ Similarity search in ChromaDB                           │
│     └──▶ Return top-k relevant chunks                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

### 4. flashcards

```sql
CREATE TABLE flashcards (
    id SERIAL PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    front TEXT NOT NULL,
    back TEXT NOT NULL,
    hint TEXT,
    "order" INTEGER NOT NULL DEFAULT 0,
    is_ai_generated BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_flashcards_document ON flashcards(document_id);
CREATE INDEX idx_flashcards_order ON flashcards(document_id, "order");
```

| Column | Type | Mo ta |
|--------|------|-------|
| id | SERIAL | Primary key |
| document_id | INTEGER | FK -> documents |
| front | TEXT | Mat truoc (cau hoi) |
| back | TEXT | Mat sau (dap an) |
| hint | TEXT | Goi y (nullable) |
| order | INTEGER | Thu tu |
| is_ai_generated | BOOLEAN | Duoc tao boi AI |

---

### 5. flashcard_reviews

> **Spaced Repetition System (SRS)** su dung thuat toan **SM-2**

```sql
CREATE TABLE flashcard_reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    flashcard_id INTEGER NOT NULL REFERENCES flashcards(id) ON DELETE CASCADE,
    quality INTEGER CHECK (quality >= 0 AND quality <= 5),
    ease_factor DECIMAL(4,2) DEFAULT 2.50,
    interval INTEGER DEFAULT 0,
    repetitions INTEGER DEFAULT 0,
    next_review_at TIMESTAMP,
    last_review_at TIMESTAMP,
    total_reviews INTEGER DEFAULT 0,
    UNIQUE(user_id, flashcard_id)
);

CREATE INDEX idx_reviews_user_flashcard ON flashcard_reviews(user_id, flashcard_id);
CREATE INDEX idx_reviews_next_review ON flashcard_reviews(user_id, next_review_at)
    WHERE next_review_at IS NOT NULL;
```

| Column | Type | Mo ta |
|--------|------|-------|
| quality | INTEGER | Danh gia chat luong nho (0-5) |
| ease_factor | DECIMAL | He so de nho (mac dinh 2.5) |
| interval | INTEGER | So ngay den lan review tiep |
| repetitions | INTEGER | So lan review lien tiep dung |
| next_review_at | TIMESTAMP | Thoi gian review tiep theo |
| total_reviews | INTEGER | Tong so lan review |

#### SM-2 Algorithm Quality Rating

| Quality | Mo ta | Action |
|---------|-------|--------|
| 0 | Complete blackout | Reset repetitions, interval = 1 |
| 1 | Incorrect, but recognized | Reset repetitions, interval = 1 |
| 2 | Incorrect, easy to recall | Reset repetitions, interval = 1 |
| 3 | Correct with difficulty | Continue, increase interval |
| 4 | Correct after hesitation | Continue, increase interval |
| 5 | Perfect response | Continue, increase interval |

---

### 6. quizzes

```sql
CREATE TABLE quizzes (
    id SERIAL PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    time_limit_minutes INTEGER,
    passing_score DECIMAL(5,2) DEFAULT 60,
    max_attempts INTEGER DEFAULT 0,
    shuffle_questions BOOLEAN DEFAULT TRUE,
    is_ai_generated BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_quizzes_document ON quizzes(document_id);
```

| Column | Type | Mo ta |
|--------|------|-------|
| id | SERIAL | Primary key |
| document_id | INTEGER | FK -> documents |
| title | VARCHAR(200) | Tieu de quiz |
| description | TEXT | Mo ta |
| time_limit_minutes | INTEGER | Thoi gian lam (phut), NULL = unlimited |
| passing_score | DECIMAL | Diem qua mon (%) mac dinh 60 |
| max_attempts | INTEGER | So lan lam toi da, 0 = unlimited |
| shuffle_questions | BOOLEAN | Random thu tu cau hoi |
| is_ai_generated | BOOLEAN | Duoc tao boi AI |

---

### 7. quiz_questions

```sql
CREATE TABLE quiz_questions (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    explanation TEXT,
    "order" INTEGER NOT NULL,
    points DECIMAL(5,2) DEFAULT 1,
    answers JSONB NOT NULL DEFAULT '[]',
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_questions_quiz ON quiz_questions(quiz_id);
```

| Column | Type | Mo ta |
|--------|------|-------|
| id | SERIAL | Primary key |
| quiz_id | INTEGER | FK -> quizzes |
| content | TEXT | Noi dung cau hoi |
| explanation | TEXT | Giai thich dap an |
| order | INTEGER | Thu tu |
| points | DECIMAL | Diem (mac dinh 1) |
| answers | JSONB | Danh sách đáp án |

#### JSON Structure: answers
```json
[
  {
    "id": 1, 
    "content": "Dap an A", 
    "is_correct": false,
    "explanation": "Optional explanation for this specific choice"
  },
  {
    "id": 2, 
    "content": "Dap an B", 
    "is_correct": true
  }
]
```

---

### 8. quiz_attempts

```sql
CREATE TABLE quiz_attempts (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER NOT NULL REFERENCES quizzes(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    score DECIMAL(5,2),
    passed BOOLEAN DEFAULT FALSE,
    answers JSONB NOT NULL DEFAULT '[]',
    started_at TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP,
    time_spent_seconds INTEGER
);

CREATE INDEX idx_attempts_quiz_user ON quiz_attempts(quiz_id, user_id);
CREATE INDEX idx_attempts_user ON quiz_attempts(user_id);
```

| Column | Type | Mo ta |
|--------|------|-------|
| id | SERIAL | Primary key |
| quiz_id | INTEGER | FK -> quizzes |
| user_id | INTEGER | FK -> users |
| score | DECIMAL | Diem dat duoc (%) |
| passed | BOOLEAN | Co qua mon khon |
| answers | JSONB | Cau tra loi cua user |
| started_at | TIMESTAMP | Thoi gian bat dau |
| completed_at | TIMESTAMP | Thoi gian hoan thanh |
| time_spent_seconds | INTEGER | Thoi gian lam bai (giay) |

#### JSON Structure: answers
```json
[
  {
    "question_id": 1, 
    "answer_id": 2,
    "is_correct": true,
    "points_earned": 1.0
  },
  {
    "question_id": 2, 
    "answer_id": 5,
    "is_correct": false,
    "points_earned": 0.0
  }
]
```

---

### 9. chat_sessions

```sql
CREATE TABLE chat_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    document_id INTEGER REFERENCES documents(id) ON DELETE SET NULL,
    title VARCHAR(200) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_chat_sessions_user ON chat_sessions(user_id);
CREATE INDEX idx_chat_sessions_document ON chat_sessions(document_id);
CREATE INDEX idx_chat_sessions_updated ON chat_sessions(updated_at DESC);
```

| Column | Type | Mo ta |
|--------|------|-------|
| id | SERIAL | Primary key |
| user_id | INTEGER | FK -> users |
| document_id | INTEGER | FK -> documents (nullable) |
| title | VARCHAR(200) | Tieu de session |
| created_at | TIMESTAMP | Thoi gian tao |
| updated_at | TIMESTAMP | Thoi gian cap nhat cuoi |

---

### 10. chat_messages

```sql
CREATE TABLE chat_messages (
    id SERIAL PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    tokens_used INTEGER DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_chat_messages_session ON chat_messages(session_id);
CREATE INDEX idx_chat_messages_created ON chat_messages(session_id, created_at);
```

| Column | Type | Mo ta |
|--------|------|-------|
| id | SERIAL | Primary key |
| session_id | INTEGER | FK -> chat_sessions |
| role | VARCHAR(20) | user/assistant/system |
| content | TEXT | Noi dung tin nhan |
| tokens_used | INTEGER | So tokens su dung |
| created_at | TIMESTAMP | Thoi gian tao |

---

### 11. notes

```sql
CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    page_number INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_notes_user ON notes(user_id);
CREATE INDEX idx_notes_document ON notes(document_id);
CREATE INDEX idx_notes_content ON notes USING gin(to_tsvector('english', content));
```

| Column | Type | Mo ta |
|--------|------|-------|
| id | SERIAL | Primary key |
| user_id | INTEGER | FK -> users |
| document_id | INTEGER | FK -> documents |
| content | TEXT | Noi dung ghi chu |
| page_number | INTEGER | So trang trong tai lieu |

---

### 12. bookmarks

```sql
CREATE TABLE bookmarks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    note TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, document_id)
);

CREATE INDEX idx_bookmarks_user ON bookmarks(user_id);
CREATE INDEX idx_bookmarks_document ON bookmarks(document_id);
CREATE INDEX idx_bookmarks_created ON bookmarks(created_at DESC);
```

| Column | Type | Mo ta |
|--------|------|-------|
| id | SERIAL | Primary key |
| user_id | INTEGER | FK -> users |
| document_id | INTEGER | FK -> documents |
| note | TEXT | Ghi chu kem theo |

---

### 13. ai_generations

> **Unified table** cho tat ca AI generation history (quiz, summary, flashcard)

```sql
CREATE TABLE ai_generations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    document_id INTEGER REFERENCES documents(id) ON DELETE SET NULL,
    type VARCHAR(20) NOT NULL CHECK (type IN ('quiz', 'summary', 'flashcard', 'learning_path', 'test_matrix', 'homework_solution')),
    tokens_used INTEGER NOT NULL,
    result JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ai_generations_user ON ai_generations(user_id);
CREATE INDEX idx_ai_generations_document ON ai_generations(document_id);
CREATE INDEX idx_ai_generations_type ON ai_generations(type);
CREATE INDEX idx_ai_generations_created ON ai_generations(created_at DESC);
```

| Column | Type | Mo ta |
|--------|------|-------|
| id | SERIAL | Primary key |
| user_id | INTEGER | FK -> users |
| document_id | INTEGER | FK -> documents |
| type | VARCHAR(20) | quiz/summary/flashcard/learning_path/test_matrix/homework_solution |
| tokens_used | INTEGER | So tokens su dung |
| result | JSONB | Ket qua generation |

#### JSON Structure: result (by type)

**Quiz Result:**
```json
{
  "title": "AI Generated Quiz",
  "questions": [
    {
      "content": "Question text",
      "explanation": "Explanation",
      "answers": [
        {"id": 1, "content": "Dap an A", "is_correct": false, "explanation": "Optional explanation for this specific choice"},
        {"id": 2, "content": "Dap an B", "is_correct": true}
      ]
    }
  ]
}
```

**Summary Result:**
```json
{
  "summary": "Summary text...",
  "style": "bullet_points",
  "key_points": ["Point 1", "Point 2"]
}
```

**Flashcard Result:**
```json
{
  "flashcards": [
    {"front": "Question", "back": "Answer", "hint": "Hint"}
  ]
}
```

**Learning Path Result:**
```json
{
  "path_title": "AI Generated Learning Path",
  "stages": [
    {
      "stage_title": "Stage 1: Introduction",
      "lessons": [
        {"lesson_title": "Lesson 1.1", "summary": "Summary of lesson 1.1"},
        {"lesson_title": "Lesson 1.2", "summary": "Summary of lesson 1.2"}
      ]
    }
  ]
}
```

**Test Matrix Result:**
```json
{
  "matrix_title": "AI Generated Test Matrix",
  "total_questions": 10,
  "criteria": [
    {"topic": "Topic A", "difficulty": "easy", "question_count": 5},
    {"topic": "Topic B", "difficulty": "medium", "question_count": 5}
  ]
}
```

**Homework Solution Result:**
```json
{
  "problem_text": "Original problem text",
  "subject": "Mathematics",
  "difficulty": "Medium",
  "solution_steps": [
    {
      "step": 1, 
      "title": "Analyze the problem",
      "content": "Step 1 explanation...",
      "formula": "y = ax + b"
    },
    {
      "step": 2, 
      "title": "Calculate the result",
      "content": "Step 2 explanation..."
    }
  ],
  "final_answer": "Final Result",
  "explanation_video_url": null
}
```

---

### 14. learning_paths
> **Requirement 3.3** - Cấu trúc lộ trình học tập từ tài liệu

```sql
CREATE TABLE learning_paths (
    id SERIAL PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(document_id, user_id)
);

CREATE INDEX idx_learning_paths_document ON learning_paths(document_id);
CREATE INDEX idx_learning_paths_user ON learning_paths(user_id);
```

| Column | Type | Mo ta |
|--------|------|-------|
| id | SERIAL | Primary key |
| document_id | INTEGER | FK -> documents |
| user_id | INTEGER | FK -> users (owner) |
| title | VARCHAR(255) | Tieu de lo trinh |
| description | TEXT | Mo ta lo trinh |

---

### 15. path_stages
> Các giai đoạn trong một lộ trình

```sql
CREATE TABLE path_stages (
    id SERIAL PRIMARY KEY,
    path_id INTEGER NOT NULL REFERENCES learning_paths(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    "order" INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_path_stages_path ON path_stages(path_id);
CREATE UNIQUE INDEX idx_path_stages_path_order ON path_stages(path_id, "order");
```

| Column | Type | Mo ta |
|--------|------|-------|
| id | SERIAL | Primary key |
| path_id | INTEGER | FK -> learning_paths |
| title | VARCHAR(255) | Tieu de giai doan |
| order | INTEGER | Thu tu giai doan |

---

### 16. path_lessons
> Các bài học chi tiết trong từng giai đoạn

```sql
CREATE TABLE path_lessons (
    id SERIAL PRIMARY KEY,
    stage_id INTEGER NOT NULL REFERENCES path_stages(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content_summary TEXT, -- Tóm tắt ngắn gọn bài học
    "order" INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_path_lessons_stage ON path_lessons(stage_id);
CREATE UNIQUE INDEX idx_path_lessons_stage_order ON path_lessons(stage_id, "order");
```

| Column | Type | Mo ta |
|--------|------|-------|
| id | SERIAL | Primary key |
| stage_id | INTEGER | FK -> path_stages |
| title | VARCHAR(255) | Tieu de bai hoc |
| content_summary | TEXT | Tom tat noi dung bai hoc |
| order | INTEGER | Thu tu bai hoc |

---

### 17. lesson_progress
> **Requirement 3.9** - Theo dõi tiến độ học bài

```sql
CREATE TABLE lesson_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    lesson_id INTEGER NOT NULL REFERENCES path_lessons(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'completed')),
    completed_at TIMESTAMP,
    UNIQUE(user_id, lesson_id)
);

CREATE INDEX idx_lesson_progress_user ON lesson_progress(user_id);
CREATE INDEX idx_lesson_progress_lesson ON lesson_progress(lesson_id);
```

| Column | Type | Mo ta |
|--------|------|-------|
| id | SERIAL | Primary key |
| user_id | INTEGER | FK -> users |
| lesson_id | INTEGER | FK -> path_lessons |
| status | VARCHAR(20) | pending/completed |
| completed_at | TIMESTAMP | Thoi gian hoan thanh |

---

### 18. test_matrices
> **Requirement 3.7** - Sinh đề kiểm tra theo ma trận

```sql
CREATE TABLE test_matrices (
    id SERIAL PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    total_questions INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_test_matrices_document ON test_matrices(document_id);
CREATE INDEX idx_test_matrices_user ON test_matrices(user_id);
```

| Column | Type | Mo ta |
|--------|------|-------|
| id | SERIAL | Primary key |
| document_id | INTEGER | FK -> documents |
| user_id | INTEGER | FK -> users |
| title | VARCHAR(255) | Tieu de ma tran |
| total_questions | INTEGER | Tong so cau hoi |

---

### 19. matrix_criteria

```sql
CREATE TABLE matrix_criteria (
    id SERIAL PRIMARY KEY,
    matrix_id INTEGER NOT NULL REFERENCES test_matrices(id) ON DELETE CASCADE,
    topic VARCHAR(255), -- Chủ đề của nhóm câu hỏi
    difficulty VARCHAR(20) CHECK (difficulty IN ('easy', 'medium', 'hard')),
    question_count INTEGER NOT NULL, -- Số lượng câu cho tiêu chí này
    points_per_question DECIMAL(4,2) DEFAULT 1.0
);

CREATE INDEX idx_matrix_criteria_matrix ON matrix_criteria(matrix_id);
```

| Column | Type | Mo ta |
|--------|------|-------|
| id | SERIAL | Primary key |
| matrix_id | INTEGER | FK -> test_matrices |
| topic | VARCHAR(255) | Chu de cau hoi |
| difficulty | VARCHAR(20) | Do kho (easy/medium/hard) |
| question_count | INTEGER | So luong cau hoi |
| points_per_question | DECIMAL | Diem moi cau |

---

### 20. homework_solutions
> **Requirement 3.8** - Giải bài tập chi tiết (Chain-of-Thought)

```sql
CREATE TABLE homework_solutions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    problem_text TEXT NOT NULL, -- Đề bài user nhập
    solution_steps JSONB NOT NULL, -- Các bước giải chi tiết [ { "step": 1, "content": "..." }, ... ]
    final_answer TEXT,
    subject VARCHAR(50), -- Toán, Lý, Hóa...
    tokens_used INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_homework_solutions_user ON homework_solutions(user_id);
CREATE INDEX idx_homework_solutions_subject ON homework_solutions(subject);
```

| Column | Type | Mo ta |
|--------|------|-------|
| id | SERIAL | Primary key |
| user_id | INTEGER | FK -> users |
| problem_text | TEXT | De bai user nhap |
| solution_steps | JSONB | Cac buoc giai chi tiet |
| final_answer | TEXT | Dap an cuoi cung |
| subject | VARCHAR(50) | Mon hoc (Toan, Ly, Hoa...) |
| tokens_used | INTEGER | So tokens su dung |

---

## 📊 Tables Summary

| # | Table | Mo ta | JSON Fields |
|---|-------|-------|-------------|
| 1 | users | Nguoi dung (Google Auth) | - |
| 2 | documents | Tai lieu upload (PDF/DOCX) | - |
| 3 | document_chunks | Chunks cho RAG | - |
| 4 | flashcards | Flashcard tu tai lieu | - |
| 5 | flashcard_reviews | Review SRS (SM-2) | - |
| 6 | quizzes | Quiz tu tai lieu | - |
| 7 | quiz_questions | Cau hoi quiz | answers |
| 8 | quiz_attempts | Lan lam quiz | answers |
| 9 | chat_sessions | Phien chat AI | - |
| 10 | chat_messages | Tin nhan | - |
| 11 | notes | Ghi chu ca nhan | - |
| 12 | bookmarks | Bookmark | - |
| 13 | ai_generations | Lich su AI generation | result |
| 14 | learning_paths | Lo trinh hoc tap | - |
| 15 | path_stages | Giai doan lo trinh | - |
| 16 | path_lessons | Bai hoc lo trinh | - |
| 17 | lesson_progress | Tien do bai hoc | - |
| 18 | test_matrices | Ma tran de thi | - |
| 19 | matrix_criteria | Tieu chi ma tran | - |
| 20 | homework_solutions | Giai bai tập | solution_steps |

**Total: 20 Tables**

---

## 📊 Indexes Summary

| Table | Index | Purpose |
|-------|-------|---------|
| users | idx_users_email | Tim user theo email |
| users | idx_users_role | Filter theo role |
| documents | idx_documents_user | Tim documents theo user |
| documents | idx_documents_status | Filter theo status |
| document_chunks | idx_chunks_document | Tim chunks theo document |
| document_chunks | idx_chunks_embedding | Tim theo embedding ID |
| flashcards | idx_flashcards_document | Tim flashcards theo document |
| flashcard_reviews | idx_reviews_next_review | Tim cards can review |
| quizzes | idx_quizzes_document | Tim quiz theo document |
| quiz_questions | idx_questions_quiz | Tim questions theo quiz |
| quiz_attempts | idx_attempts_quiz_user | Tim attempts theo quiz va user |
| chat_sessions | idx_chat_sessions_user | Tim sessions theo user |
| chat_messages | idx_chat_messages_session | Tim messages theo session |
| notes | idx_notes_content | Full-text search notes |
| bookmarks | idx_bookmarks_user | Tim bookmarks theo user |
| ai_generations | idx_ai_generations_type | Filter theo type |

---

## 🔐 Access Control (2 Roles: Admin + User)

| Resource | Public | User | Admin |
|----------|--------|------|-------|
| **Documents** |
| List documents | - | Owner | All |
| Upload document | - | Yes | Yes |
| View document | - | Owner | All |
| Delete document | - | Owner | All |
| **Flashcards** |
| View flashcards | - | Owner | All |
| Create flashcard | - | Owner | Yes |
| Review flashcard | - | Owner | All |
| **Quizzes** |
| View quiz | - | Owner | All |
| Start quiz | - | Owner | All |
| **Chat** |
| Create session | - | Yes | Yes |
| Send message | - | Owner | All |
| **Notes & Bookmarks** |
| CRUD | - | Self | All |
| **AI Services** |
| Generate Quiz | - | Owner | Yes |
| Generate Flashcards | - | Owner | Yes |
| Summarize | - | Owner | Yes |
| **Admin Only** |
| Manage users | - | - | Yes |

---

## 🔄 Migration Guide (v4.0 -> v5.0)

### Tables REMOVED/REPLACED:
- `categories` - Khong can thiet trong Document-RAG model
- `courses` - Thay bang `documents`
- `lessons` - Thay bang `path_lessons` (Learning Path module)
- `enrollments` - Khong can thiet
- `exercise_submissions` - Thay bang `homework_solutions`
- `conversations` - Doi ten thanh `chat_sessions`
- `ai_quiz_generations` - Gop vao `ai_generations`
- `ai_summaries` - Gop vao `ai_generations`

### Key Changes:
1. **Flashcards**: `lesson_id` -> `document_id`
2. **Quizzes**: `lesson_id` -> `document_id`
3. **Notes**: `lesson_id` -> `document_id`
4. **Bookmarks**: `lesson_id` -> `document_id`
5. **Chat Sessions**: `course_id` -> `document_id`
6. **AI Generations**: Bang moi (unified) thay vi 2 bang rieng

---

## 🏗️ Architecture Benefits

### Document-RAG Based
- **Simplicity**: 20 tables focus on educational depth.
- **Flexibility**: User upload bat ky tai lieu nao
- **AI-Powered**: RAG system tra cuu thong tin thong minh
- **Scalability**: De mo rong voi nhieu loai tai lieu

### Key Features
1. **Document Management**: Upload PDF/DOCX, tu dong xu ly
2. **RAG System**: Chunking, embedding, similarity search
3. **Flashcards**: SM-2 algorithm, SRS learning
4. **Quizzes**: Multiple choice, AI generation
5. **AI Chat**: Context-aware, RAG-based responses
6. **Personal Notes**: Ghi chu theo tai lieu
7. **Bookmarks**: Luu tai lieu quan trong

---

*Tai lieu nay dinh nghia cau truc database cho he thong AI Tutor Document-RAG Based.*
*Version: 5.0 - 20 tables, Document-RAG architecture, unified AI generations*
*Updated: 2026-03-01*
