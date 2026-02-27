# NRO Marketplace - Master Overview

> Tài liệu tổng quan cho toàn bộ dự án NRO Marketplace - Sàn giao dịch tài khoản game với cơ chế Escrow

---

## 📋 Mục Lục Tài Liệu

| File | Mô tả |
|------|-------|
| [00-MASTER-OVERVIEW.md](./00-MASTER-OVERVIEW.md) | Tổng quan dự án (file này) |
| [01-BUSINESS-MODEL.md](./01-BUSINESS-MODEL.md) | Business Model & User Personas |
| [02-DATABASE-DESIGN.md](./02-DATABASE-DESIGN.md) | Database Schema chi tiết |
| [03-API-DESIGN.md](./03-API-DESIGN.md) | REST API Endpoints |
| [04-ESCROW-FLOW.md](./04-ESCROW-FLOW.md) | Luồng ký quỹ & giao dịch |
| [05-AUTH-DESIGN.md](./05-AUTH-DESIGN.md) | Authentication (Google OAuth Only) |
| [06-UI-PAGES.md](./06-UI-PAGES.md) | Frontend Pages & Components |
| [07-ADMIN-FEATURES.md](./07-ADMIN-FEATURES.md) | Admin Dashboard Features (UI) |
| [08-SECURITY.md](./08-SECURITY.md) | Security & Access Control |
| [09-CODE-STRUCTURE.md](./09-CODE-STRUCTURE.md) | Code Structure Design (Backend + Frontend) |
| [10-ADMIN-FLOWS.md](./10-ADMIN-FLOWS.md) | Admin Operation Flows (chi tiết) |
| [11-LUCKY-WHEEL.md](./11-LUCKY-WHEEL.md) | Vòng Quay May Mắn (Lucky Wheel) |

---

## 🎯 Tóm Tắt Dự Án

### Concept
**NRO Marketplace** là sàn giao dịch tài khoản game trực tuyến, chuyên về các tựa game mobile phổ biến tại Việt Nam (Ngọc Rồng Online, Liên Quân Mobile).

### Điểm Khác Biệt
- **Escrow System**: Tiền được giữ bởi platform cho đến khi giao dịch hoàn tất
- **Google OAuth Only**: Không có form đăng ký/login truyền thống - chỉ 1 nút Google
- **Admin Moderation**: Mọi bài đăng phải được admin duyệt trước khi lên sàn
- **Dispute Resolution**: Hệ thống khiếu nại và xử lý tranh chấp

---

## 🏗️ Tech Stack

### Backend
- **Framework**: Ruby on Rails 8.0 (API mode)
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Auth**: OmniAuth Google OAuth2
- **Architecture**: HMVC with Operations, Forms, Validators

### Frontend
- **Framework**: React 18+ with Vite
- **Styling**: TailwindCSS / CSS Variables
- **State**: Zustand
- **Icons**: Lucide React

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SYSTEM ARCHITECTURE                                 │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
    │   REACT     │         │   RAILS     │         │  DATABASE   │
    │   FRONTEND  │◀───────▶│   API       │◀───────▶│  SQLite/PG  │
    │   (Vite)    │  REST   │   (JSON)    │         │             │
    └─────────────┘         └──────┬──────┘         └─────────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
                    ▼              ▼              ▼
            ┌───────────┐  ┌───────────┐  ┌───────────┐
            │  Google   │  │  Payment  │  │ Encryption│
            │   OAuth   │  │  Gateway  │  │  Service  │
            └───────────┘  └───────────┘  └───────────┘
```

---

## 👥 User Personas

| Persona | Vai trò | Actions |
|---------|---------|---------|
| **Buyer** | Người mua nick | Xem, tìm kiếm, mua, nạp tiền, khiếu nại |
| **Seller** | Người bán nick | Đăng nick, quản lý bài, rút tiền |
| **Admin** | Quản trị viên | Duyệt bài, xử lý dispute, quản lý users |

> **Lưu ý**: Một user có thể vừa là Buyer vừa là Seller. Role chỉ phân biệt `member` vs `admin`.

---

## 🔄 Core Flows

### 1. Seller Flow
```
Tạo Game Profile → Nhập Credentials → Tạo Post → Chờ Admin Duyệt →
Post Active → Chờ Buyer → Bán → Nhận Tiền
```

### 2. Buyer Flow
```
Tìm Nick → Xem Chi Tiết → Mua (Trừ Tiền) → Nhận Credentials →
Kiểm Tra → Complete / Dispute
```

### 3. Admin Flow
```
Xem Posts Pending → Verify Credentials → Approve/Reject →
Monitor Purchases → Resolve Disputes
```

---

## 📅 Development Phases

| Phase | Nội dung | Priority |
|-------|----------|----------|
| **Phase 1** | Database Seeds + Base APIs | High |
| **Phase 2** | Frontend Layout & Router | High |
| **Phase 3** | Marketplace Listing UI | High |
| **Phase 4** | Google OAuth | High |
| **Phase 5** | Escrow Checkout Logic | High |
| **Phase 6** | Admin Dashboard | Medium |
| **Phase 7** | Billing & Wallet | Medium |
| **Phase 8** | Dispute System | Medium |

---

## ✅ Decisions Made

| Decision | Choice | Reason |
|----------|--------|--------|
| Role Model | `member` / `admin` | User có thể vừa mua vừa bán |
| Escrow Period | 3 days | Thời gian bảo hành |
| Auto-complete | 7 days | Sau 7 ngày không dispute → auto complete |
| Platform Fee | 0% (Phase 1) | Miễn phí để thu hút users |
| Session Timeout | 7 days | Balance giữa security và UX |
| Credentials | Plain text + Access control | Admin cần đổi password khi verify |

---

## 🚀 Getting Started

1. Đọc qua tất cả spec files trong folder này
2. Chạy `/opsx:ff "phase-1-database-seeds"` để bắt đầu implement
3. Follow các phases theo thứ tự

---

*Tài liệu được tạo ngày: 2026-02-26*
*Version: 1.0*
