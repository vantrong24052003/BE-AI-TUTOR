# BE AI TUTOR - Master Overview

> Tài liệu tổng quan cho toàn bộ dự án BE AI TUTOR - Nền tảng học tập thông minh với AI

---

## 📋 Mục Lục Tài Liệu

| File | Mô tả |
|------|-------|
| [00-MASTER-OVERVIEW.md](./00-MASTER-OVERVIEW.md) | Tổng quan dự án (file này) |
| [01-BUSINESS-MODEL.md](./01-BUSINESS-MODEL.md) | Business Model & User Personas |
| [02-DATABASE-DESIGN.md](./02-DATABASE-DESIGN.md) | Database Schema chi tiết |
| [03-API-DESIGN.md](./03-API-DESIGN.md) | REST API Endpoints |
| [04-AUTH-DESIGN.md](./04-AUTH-DESIGN.md) | Authentication & Authorization |
| [05-AI-CHAT-FLOW.md](./05-AI-CHAT-FLOW.md) | Luồng tích hợp AI Chat |
| [06-SECURITY.md](./06-SECURITY.md) | Security & Access Control |
| [07-CODE-STRUCTURE.md](./07-CODE-STRUCTURE.md) | Code Structure Design |

---

## 🎯 Tóm Tắt Dự Án

### Concept
**BE AI TUTOR** là nền tảng học tập trực tuyến tích hợp AI, hỗ trợ học viên học tập thông qua khóa học, bài giảng, bài kiểm tra và trò chuyện với AI tutor.

### Điểm Khác Biệt
- **AI Tutor**: Trò chuyện với AI để được hỗ trợ học tập 24/7
- **Context-Aware AI**: AI hiểu ngữ cảnh khóa học đang học
- **Quiz System**: Hệ thống bài kiểm tra tự động với chấm điểm
- **Progress Tracking**: Theo dõi tiến độ học tập chi tiết

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

## 👥 User Personas

| Persona | Vai trò | Actions |
|---------|---------|---------|
| **Student** | Học viên | Xem khóa học, làm bài tập, chat AI, xem tiến độ |
| **Teacher** | Giáo viên | Tạo khóa học, bài học, quiz, xem tiến độ học viên |
| **Admin** | Quản trị viên | Quản lý users, courses, toàn bộ hệ thống |

---

## 🔄 Core Flows

### 1. Student Flow
```
Đăng ký → Xem danh sách khóa học → Đăng ký khóa → Học bài →
Làm quiz → Chat với AI → Xem tiến độ
```

### 2. Teacher Flow
```
Tạo khóa học → Thêm bài học → Tạo quiz → Xem tiến độ học viên →
Cập nhật nội dung
```

### 3. AI Chat Flow
```
Student chọn khóa → Mở chat → Gửi câu hỏi → AI phản hồi (context: khóa học) →
Lưu lịch sử
```

---

## 📅 Development Phases

| Phase | Nội dung | Priority |
|-------|----------|----------|
| **Phase 1** | Database Models & Migrations | High |
| **Phase 2** | Auth API (Register, Login, JWT) | High |
| **Phase 3** | User Management APIs | High |
| **Phase 4** | Course & Lesson APIs | High |
| **Phase 5** | Quiz System APIs | High |
| **Phase 6** | AI Chat Integration | High |
| **Phase 7** | Progress Tracking | Medium |
| **Phase 8** | Document Management | Medium |
| **Phase 9** | Admin Dashboard APIs | Medium |

---

## ✅ Decisions Made

| Decision | Choice | Reason |
|----------|--------|--------|
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
*Version: 1.0*
