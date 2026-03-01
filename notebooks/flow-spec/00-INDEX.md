# BE AI TUTOR - Flow Specifications Index

> Tổng hợp chi tiết specification cho từng tính năng của hệ thống AI Tutor
> **Phiên bản**: 5.1 (Tương thích 100% tài liệu Đặc tả hệ thống Gia sư AI)

---

## ⚠️ QUAN TRỌNG - Cách Sử Dụng

### Code Trong Spec Chỉ Là Tham Khảo

```
╔══════════════════════════════════════════════════════════════╗
║  🚨 CODE TRONG CÁC FILE SPEC CHỈ LÀ THAM KHẢO                ║
║                                                              ║
║  Mục đích cuối cùng: Sử dụng OpenSpec để generate spec chi tiết║
║  Lệnh: /opsx-ff + tên file → Generate implementation spec   ║
║                                                              ║
║  Các file spec này mô tả:                                    ║
║  - Business logic và data flow                               ║
║  - API endpoints và request/response format                  ║
║  - Database schema                                           ║
║  - Implementation patterns (tham khảo)                       ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🎯 TỔNG QUAN PROJECT

### Mô tả
**AI Tutor** là ứng dụng hỗ trợ học tập thông minh sử dụng AI. Người dùng có thể:
- Upload tài liệu (PDF, DOCX)
- AI tự động tạo Flashcard, Quiz, Tóm tắt từ tài liệu
- Chat với AI để hỏi đáp về nội dung tài liệu
- Ôn tập Flashcard với thuật toán Spaced Repetition (SM-2)

### Core Features
```
┌─────────────────────────────────────────────────────────────────┐
│                     AI TUTOR WORKFLOW                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. UPLOAD TÀI LIỆU                                             │
│     ┌──────────┐    ┌──────────┐    ┌──────────┐               │
│     │  PDF/    │───▶│  Extract │───▶│  Store   │               │
│     │  DOCX    │    │  Text    │    │  in RAG  │               │
│     └──────────┘    └──────────┘    └────┬─────┘               │
│                                          │                      │
│  2. AI GENERATION                         ▼                      │
│     ┌──────────────────────────────────────────────────┐       │
│     │  ┌─────────┐  ┌─────────┐  ┌─────────────────┐  │       │
│     │  │ Summary │  │ Flashcards │ │     Quiz       │  │       │
│     │  └─────────┘  └─────────┘  └─────────────────┘  │       │
│     └──────────────────────────────────────────────────┘       │
│                          │                                      │
│  3. STUDY                 ▼                                      │
│     ┌──────────┐    ┌──────────┐    ┌──────────┐               │
│     │  Review  │    │   Chat   │    │   Take   │               │
│     │ Flashcard│    │ with AI  │    │   Quiz   │               │
│     └──────────┘    └──────────┘    └──────────┘               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 TECH STACK

### Backend

| Công nghệ | Version | Mục đích | Cài đặt |
|-----------|---------|----------|---------|
| **Python** | 3.12 | Ngôn ngữ chính | `pyenv install 3.12` |
| **FastAPI** | Latest | Web framework | `pip install fastapi[all]` |
| **SQLAlchemy** | 2.x | ORM | `pip install sqlalchemy[asyncio]` |
| **Alembic** | Latest | Database migration | `pip install alembic` |
| **Pydantic** | 2.x | Data validation | `pip install pydantic` |
| **PostgreSQL** | 16 | Relational Database | Docker/Cài đặt trực tiếp |
| **Redis** | Latest | Cache & Message Queue | Docker/Cài đặt trực tiếp |

### AI & RAG

| Công nghệ | Mục đích | Cài đặt |
|-----------|----------|---------|
| **Claude API** (Anthropic) | Primary LLM | `pip install anthropic` |
| **LangChain** | AI Framework | `pip install langchain langchain-community` |
| **ChromaDB** | Vector Database (RAG) | `pip install chromadb` |
| **sentence-transformers** | Embedding model | `pip install sentence-transformers` |

### Additional Libraries

```txt
# requirements.txt
fastapi[all]>=0.109.0
sqlalchemy[asyncio]>=2.0
alembic>=1.13
pydantic>=2.5
pydantic-settings>=2.1
asyncpg>=0.29
redis>=5.0
anthropic>=0.18
langchain>=0.1
langchain-community>=0.0.20
chromadb>=0.4
sentence-transformers>=2.2
python-jose[cryptography]>=3.3
passlib[bcrypt]>=1.7
python-multipart>=0.0.6
aiofiles>=23.2
httpx>=0.26
pypdf>=4.0
python-docx>=1.1
```

---

## 🔄 RAG SYSTEM (Retrieval-Augmented Generation)

### Kiến Trúc RAG

```
┌─────────────────────────────────────────────────────────────────┐
│                        RAG PIPELINE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. DOCUMENT INGESTION                                          │
│     ┌──────────┐    ┌──────────┐    ┌──────────┐               │
│     │  PDF/    │───▶│  Chunk   │───▶│ Embedding│               │
│     │  DOCX    │    │  Split   │    │  Model   │               │
│     └──────────┘    └──────────┘    └────┬─────┘               │
│                                          │                      │
│  2. STORAGE                              ▼                      │
│     ┌──────────────────────────────────────────┐               │
│     │           VECTOR DATABASE (ChromaDB)      │               │
│     │  - document_chunks                       │               │
│     │  - embeddings (768 dims)                 │               │
│     │  - metadata (document_id, page, etc.)    │               │
│     └──────────────────────────────────────────┘               │
│                          │                                      │
│  3. RETRIEVAL            ▼                                      │
│     ┌──────────┐    ┌──────────┐    ┌──────────┐               │
│     │  Query   │───▶│ Embed    │───▶│ Semantic │               │
│     │          │    │  Query   │    │  Search  │               │
│     └──────────┘    └──────────┘    └────┬─────┘               │
│                                          │                      │
│  4. GENERATION                           ▼                      │
│     ┌──────────────────────────────────────────┐               │
│     │              LLM (Claude)                 │               │
│     │  Context: Retrieved chunks + User query  │               │
│     └──────────────────────────────────────────┘               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### RAG Use Cases

1. **AI Chat** - Trả lời câu hỏi dựa trên nội dung tài liệu
2. **Tóm tắt tài liệu** - Sinh summary từ tài liệu
3. **Sinh Flashcards** - Tạo flashcard từ nội dung
4. **Tạo Quiz** - Tạo câu hỏi trắc nghiệm từ tài liệu

---

## 📨 MESSAGE QUEUE (Redis)

### Kiến Trúc Queue

```
┌─────────────────────────────────────────────────────────────────┐
│                    ASYNC TASK PROCESSING                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐     ┌──────────┐     ┌──────────────────┐        │
│  │  API     │────▶│  Redis   │────▶│  Worker Process  │        │
│  │  Request │     │  Queue   │     │  (Background)    │        │
│  └──────────┘     └──────────┘     └──────────────────┘        │
│       │                │                    │                   │
│       ▼                ▼                    ▼                   │
│  ┌──────────┐     ┌──────────┐     ┌──────────────────┐        │
│  │ Return   │     │ Queue    │     │ - PDF Processing │        │
│  │ Task ID  │     │ Status   │     │ - AI Generation  │        │
│  └──────────┘     └──────────┘     └──────────────────┘        │
│                                                                  │
│  QUEUES:                                                         │
│  ├── document_processing: Xử lý PDF/DOCX                       │
│  └── ai_generation: Tạo quiz, flashcard, summary               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 Danh Sách Specifications

| File | Tính năng | APIs | RAG | Queue |
|------|-----------|------|-----|-------|
| [01-AUTH-SPEC.md](./01-AUTH-SPEC.md) | Authentication | 4 | ❌ | ❌ |
| [02-DOCUMENTS-SPEC.md](./02-DOCUMENTS-SPEC.md) | Documents | 6 | ✅ | ✅ |
| [03-FLASHCARDS-SPEC.md](./03-FLASHCARDS-SPEC.md) | Flashcards | 7 | ✅ | ✅ |
| [04-QUIZ-SPEC.md](./04-QUIZ-SPEC.md) | Quiz | 6 | ✅ | ✅ |
| [05-AI-SERVICES-SPEC.md](./05-AI-SERVICES-SPEC.md) | AI Services | 5 | ✅ | ✅ |
| [06-CHAT-AI-SPEC.md](./06-CHAT-AI-SPEC.md) | AI Chat | 5 | ✅ | ❌ |
| [07-NOTES-SPEC.md](./07-NOTES-SPEC.md) | Notes | 5 | ❌ | ❌ |
| [08-BOOKMARKS-SPEC.md](./08-BOOKMARKS-SPEC.md) | Bookmarks | 4 | ❌ | ❌ |
| [09-ADMIN-SPEC.md](./09-ADMIN-SPEC.md) | Admin | 6 | ❌ | ❌ |
| [10-LEARNING-PATH-SPEC.md](./10-LEARNING-PATH-SPEC.md) | Learning Path | 8 | ✅ | ✅ |
| [11-HOMEWORK-SPEC.md](./11-HOMEWORK-SPEC.md) | Homework Solver | 3 | ✅ | ✅ |
| [04-API-DESIGN.md](../analyzes-be/04-API-DESIGN.md) | Test Matrix | 5 | ✅ | ✅ |

**Total: 62 APIs**

---

## 🔧 RAG Features

Các features sử dụng RAG:

1. **AI Chat** - Hỏi đáp dựa trên nội dung tài liệu
2. **Tóm tắt tài liệu** - Summarize documents
3. **Sinh Flashcards** - Generate flashcards from content
4. **Tạo Quiz** - Generate quiz questions

---

## 📨 Queue Features

Các features sử dụng Message Queue:

1. **Upload tài liệu** - Async PDF/DOCX processing
2. **AI Generation** - Quiz, Flashcard, Summary generation

---

## 📁 Cấu Trúc Folder

```
notebooks/
├── analyzes-be/           # Overview luồng hoạt động
│   ├── 00-MASTER-OVERVIEW.md
│   ├── 01-BUSINESS-MODEL.md
│   ├── 02-DATABASE-DESIGN.md
│   ├── 03-CODE-STRUCTURE.md
│   └── 04-API-DESIGN.md
│
└── flow-spec/             # Chi tiết spec từng feature
    ├── 00-INDEX.md        # File này - Tech stack, RAG, Queue
    ├── 01-AUTH-SPEC.md
    ├── 02-DOCUMENTS-SPEC.md
    ├── 03-FLASHCARDS-SPEC.md
    ├── 04-QUIZ-SPEC.md
    ├── 05-AI-SERVICES-SPEC.md
    ├── 06-CHAT-AI-SPEC.md
    ├── 07-NOTES-SPEC.md
    ├── 08-BOOKMARKS-SPEC.md
    ├── 09-ADMIN-SPEC.md
    ├── 10-LEARNING-PATH-SPEC.md
    └── 11-HOMEWORK-SPEC.md
```

---

## 🚀 Workflow Implementation

```
1. Đọc spec file để hiểu business logic
         ↓
2. Sử dụng /opsx-ff + tên file để generate spec chi tiết
         ↓
3. Implement theo spec đã generate
         ↓
4. Viết tests
         ↓
5. Review và update spec nếu cần
```

---

## 📊 Database Tables (Updated)

| Category | Tables |
|----------|--------|
| **Auth** | users |
| **Documents & RAG** | documents, document_chunks |
| **Learning Path** | learning_paths, path_stages, path_lessons, lesson_progress |
| **Flashcards** | flashcards, flashcard_reviews |
| **Assessment** | quizzes, quiz_questions, quiz_attempts, test_matrices, matrix_criteria |
| **Chat & Notes** | chat_sessions, chat_messages, notes, bookmarks |
| **Log AI** | ai_generations, homework_solutions |

**Tổng cộng: 20 Tables**

---

*Tài liệu được cập nhật: 2026-03-01*
*Version: 5.1 - Tài liệu Master Overview chuẩn xác theo yêu cầu khách hàng.*
*18 Screens, 20 Tables, 62 APIs*
*Tech Stack: Python 3.12, FastAPI, PostgreSQL 16, Redis, Claude API, LangChain, ChromaDB*
