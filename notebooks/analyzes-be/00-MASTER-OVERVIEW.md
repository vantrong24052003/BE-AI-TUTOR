# BE AI TUTOR - Master Overview

> Tài liệu tổng quan cho toàn bộ dự án BE AI TUTOR - Nền tảng học tập thông minh với AI

---

## 📋 Mục Lục Tài Liệu

| File | Mô tả |
|------|-------|
| [00-MASTER-OVERVIEW.md](./00-MASTER-OVERVIEW.md) | Tổng quan dự án (file này) |
| [01-BUSINESS-MODEL.md](./01-BUSINESS-MODEL.md) | Business Model & User Personas |
| [02-DATABASE-DESIGN.md](./02-DATABASE-DESIGN.md) | Database Schema - 21 Tables |
| [03-CODE-STRUCTURE.md](./03-CODE-STRUCTURE.md) | Code Structure & Patterns |
| [04-API-DESIGN.md](./04-API-DESIGN.md) | REST API - 75 Endpoints |
| [05-AUTH-DESIGN.md](./05-AUTH-DESIGN.md) | Authentication |
| [06-AI-SERVICES-FLOW.md](./06-AI-SERVICES-FLOW.md) | Luồng tích hợp AI Services |
| [07-SECURITY.md](./07-SECURITY.md) | Security & Access Control |

---

## 🎯 Tóm Tắt Dự Án

### Concept
**BE AI TUTOR** là nền tảng học tập trực tuyến tích hợp AI, hỗ trợ người dùng học tập thông qua khóa học, bài giảng, bài kiểm tra và trò chuyện với AI tutor.

### Điểm Khác Biệt
- **AI Tutor**: Trò chuyện với AI để được hỗ trợ học tập 24/7
- **Context-Aware AI**: AI hiểu ngữ cảnh khóa học đang học
- **Quiz System**: Hệ thống bài kiểm tra tự động với chấm điểm
- **Progress Tracking**: Theo dõi tiến độ học tập chi tiết
- **Miễn phí 100%**: Không có phí, không thanh toán

---

## 🏗️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 16+ (async với asyncpg)
- **ORM**: SQLAlchemy 2.0+ (async)
- **Cache**: Redis 7+
- **Auth**: JWT (python-jose)
- **AI**: Claude API / OpenAI

### Architecture
- **Pattern**: MVC (Controller → Service → Repository)
- **Async**: Toàn bộ I/O operations async
- **Validation**: Pydantic v2

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SYSTEM ARCHITECTURE                                 │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
    │   CLIENT    │         │   FASTAPI   │         │  POSTGRESQL │
    │   (Web/App) │◀───────▶│   API       │◀───────▶│  DATABASE   │
    │             │  REST   │   (Async)   │         │             │
    └─────────────┘         └──────┬──────┘         └─────────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
                    ▼              ▼              ▼
            ┌───────────┐  ┌───────────┐  ┌───────────┐
            │   REDIS   │  │CLAUDE API │  │  FILE     │
            │   CACHE   │  │  (AI)     │  │  STORAGE  │
            └───────────┘  └───────────┘  └───────────┘
```

---

## 👥 User Model

### Two Roles: Admin + User

Hệ thống có **2 roles**: `admin` và `user` (mặc định).

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER PERMISSIONS                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ✅ USER (mặc định):                                            │
│  ├── Xem và tạo khóa học                                        │
│  ├── Xem và tạo bài học (trong course do mình tạo)              │
│  ├── Xem và tạo quiz (trong course do mình tạo)                 │
│  ├── Làm quiz và xem kết quả (nếu enrolled)                     │
│  ├── Chat với AI                                                │
│  ├── Xem tiến độ học tập của mình                               │
│  └── Upload tài liệu                                            │
│                                                                 │
│  ✅ ADMIN (toàn quyền):                                         │
│  ├── Tất cả quyền của User                                      │
│  ├── Quản lý tất cả users (CRUD)                                │
│  ├── Quản lý tất cả courses                                     │
│  ├── Quản lý categories                                         │
│  └── Xem tất cả progress                                        │
│                                                                 │
│  ✅ Ownership-based access:                                     │
│  └── User chỉ sửa/xóa resource do mình tạo                      │
│  └── Admin có thể sửa/xóa tất cả                                │
│  ❌ KHÔNG CÓ THANH TOÁN / PHÍ                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Core Flows

### Learning Flow
```
Đăng ký → Xem danh sách khóa học → Đăng ký khóa → Học bài →
Làm bài tập → Nộp bài → AI feedback → Làm Quiz → Review Flashcard →
Chat với AI → Xem tiến độ
```

### Creating Flow
```
Tạo khóa học → Thêm bài học → Tạo flashcard → Tạo bài tập →
Tạo quiz → Upload tài liệu → Xem progress học viên
```

### AI Services Flow
```
Chọn khóa → Mở chat → Gửi câu hỏi → AI phản hồi (context: khóa học) →
Lưu lịch sử

Hoặc:
Xem bài học → AI tóm tắt → AI tạo quiz → AI tạo flashcard →
Học flashcard (SRS)
```

### Spaced Repetition Flow (Flashcard)
```
Xem flashcard cần review → Review (đánh giá 0-5) → SM-2 algorithm →
Tính next_review_at → Hiển thị card tiếp theo
```

### Exercise Submission Flow
```
Làm bài tập → Nộp bài → AI chấm điểm → Feedback →
Có thể nộp lại (nếu allowed)
```

---

## 📅 Development Phases

| Phase | Nội dung | Priority |
|-------|----------|----------|
| **Phase 1** | Database Models & Migrations | High |
| **Phase 2** | Auth API (Register, Login, JWT) | High |
| **Phase 3** | Course & Lesson APIs | High |
| **Phase 4** | Quiz System APIs | High |
| **Phase 5** | AI Chat Integration | High |
| **Phase 6** | Progress Tracking | Medium |
| **Phase 7** | Document Management | Medium |

---

## ✅ Decisions Made

| Decision | Choice | Reason |
|----------|--------|--------|
| User Role | Single role (user) | Đơn giản hóa, mọi user có quyền như nhau |
| Pricing | Miễn phí 100% | Không có payment, không thu phí |
| Database | PostgreSQL | Relational data, ACID, full-text search |
| Auth | JWT | Stateless, scalable, mobile-friendly |
| AI Provider | Claude API / OpenAI | Best-in-class LLM capabilities |
| Architecture | MVC | Clear separation of concerns |
| Async | Yes | High concurrency, better performance |

---

## 🚀 Getting Started

1. Đọc qua tất cả spec files trong folder này
2. Setup environment: `cp .env.example .env`
3. Run: `docker-compose up -d`
4. Migrate: `alembic upgrade head`
5. Start: `uvicorn src.main:app --reload`

---

*Tài liệu được tạo ngày: 2026-02-27*
*Cập nhật: 2026-03-01*
*Version: 3.0 - 21 Tables, 75 APIs, Flashcards, Exercises, Notes, Bookmarks, AI Services*
