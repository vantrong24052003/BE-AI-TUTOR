# BE AI TUTOR - Master Overview

> Tài liệu tổng quan cho toàn bộ dự án BE AI TUTOR - Nền tảng học tập thông minh với AI

---

## 📋 Mục Lục Tài Liệu

| File | Mô tả |
|------|-------|
| [00-MASTER-OVERVIEW.md](./00-MASTER-OVERVIEW.md) | Tổng quan dự án (file này) |
| [01-BUSINESS-MODEL.md](./01-BUSINESS-MODEL.md) | Business Model & User Personas |
| [02-DATABASE-DESIGN.md](./02-DATABASE-DESIGN.md) | Database Schema + JSON Structures |
| [03-CODE-STRUCTURE.md](./03-CODE-STRUCTURE.md) | Code Structure & Patterns |
| [04-API-DESIGN.md](./04-API-DESIGN.md) | REST API Endpoints |
| [05-AUTH-DESIGN.md](./05-AUTH-DESIGN.md) | Authentication |
| [06-AI-CHAT-FLOW.md](./06-AI-CHAT-FLOW.md) | Luồng tích hợp AI Chat |
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

### Single Role: User

| Role | Quyền hạn |
|------|-----------|
| **user** | Tất cả quyền: CRUD courses, lessons, quizzes, chat AI, xem progress |

**Lưu ý**: Hệ thống chỉ có 1 role duy nhất là `user`. Mọi user đều có quyền như nhau.

### User Actions

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER PERMISSIONS                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Authentication:                                                │
│  ├── Đăng ký tài khoản                                          │
│  ├── Đăng nhập                                                  │
│  └── Cập nhật profile                                           │
│                                                                 │
│  Courses:                                                       │
│  ├── Xem danh sách khóa học                                     │
│  ├── Tạo khóa học mới                                           │
│  ├── Cập nhật khóa học của mình                                 │
│  └── Xóa khóa học của mình                                      │
│                                                                 │
│  Lessons:                                                       │
│  ├── Xem bài học                                                │
│  ├── Tạo bài học                                                │
│  ├── Cập nhật bài học                                           │
│  └── Xóa bài học                                                │
│                                                                 │
│  Quizzes:                                                       │
│  ├── Tạo quiz                                                   │
│  ├── Làm quiz                                                   │
│  └── Xem kết quả                                                │
│                                                                 │
│  AI Chat:                                                       │
│  ├── Tạo conversation                                           │
│  ├── Chat với AI                                                │
│  └── Xem lịch sử chat                                           │
│                                                                 │
│  Progress:                                                      │
│  ├── Xem tiến độ học tập                                        │
│  └── Đánh dấu hoàn thành                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Core Flows

### Learning Flow
```
Đăng ký → Xem danh sách khóa học → Học bài →
Làm quiz → Chat với AI → Xem tiến độ
```

### Creating Flow
```
Tạo khóa học → Thêm bài học → Tạo quiz →
Cập nhật nội dung → Xem progress
```

### AI Chat Flow
```
Chọn khóa → Mở chat → Gửi câu hỏi → AI phản hồi (context: khóa học) →
Lưu lịch sử
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
*Version: 1.1 - Single role, no payment*
