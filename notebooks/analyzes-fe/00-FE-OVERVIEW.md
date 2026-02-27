# FE AI TUTOR - UI Specification

> Tài liệu mô tả UI cho Frontend - Tập trung vào GIAO DIỆN và DATA cần hiển thị

---

## 📋 Mục Lục

| File | Mô tả |
|------|-------|
| [00-FE-OVERVIEW.md](./00-FE-OVERVIEW.md) | Tổng quan (file này) |
| [01-UI-SPECIFICATION.md](./01-UI-SPECIFICATION.md) | Chi tiết từng màn hình UI |
| [02-COMPONENTS.md](./02-COMPONENTS.md) | Component library |
| [03-ROUTING.md](./03-ROUTING.md) | Routing structure |
| [04-CODE-STRUCTURE.md](./04-CODE-STRUCTURE.md) | Code structure & conventions |

---

## 🎯 Vai Trò Của FE

**FE chỉ cần biết:**
1. ✅ UI trông như thế nào
2. ✅ Trên UI có những field nào
3. ✅ Data cần để hiển thị là gì
4. ✅ User tương tác như thế nào

**FE KHÔNG cần quan tâm:**
- ❌ Database schema
- ❌ API implementation
- ❌ Business logic phức tạp
- ❌ Security layers

---

## 🖥️ Tổng Quan Các Màn Hình

### Public Pages (Không cần đăng nhập)

| STT | Màn hình | Route | Mô tả |
|-----|----------|-------|-------|
| 1 | Landing Page | `/` | Trang chủ giới thiệu |
| 2 | Login | `/auth/login` | Đăng nhập |
| 3 | Register | `/auth/register` | Đăng ký |
| 4 | Forgot Password | `/auth/forgot-password` | Quên mật khẩu |

### Protected Pages (Cần đăng nhập)

| STT | Màn hình | Route | Role | Mô tả |
|-----|----------|-------|------|-------|
| 5 | Dashboard | `/app/dashboard` | Student | Trang chính sau đăng nhập |
| 6 | Course List | `/app/courses` | Student | Danh sách khóa học |
| 7 | Course Detail | `/app/courses/:id` | Student | Chi tiết khóa học |
| 8 | Learning | `/app/learn/:courseId/lesson/:lessonId` | Student | Giao diện học |
| 9 | Quiz | `/app/quiz/:quizId` | Student | Làm bài kiểm tra |
| 10 | AI Chat | `/app/ai-tutor` | Student | Chat với AI |
| 11 | Profile | `/app/profile` | Student | Thông tin cá nhân |
| 12 | My Courses | `/app/my-courses` | Student | Khóa đã đăng ký |

---

## 👥 User Roles & Permissions

| Role | Quyền hạn |
|------|-----------|
| **Student** | Xem khóa học, học bài, làm quiz, chat AI |

---

## 🎨 Design System Quick Reference

### Colors
- **Primary**: Blue (#3B82F6)
- **Secondary**: Purple (#8B5CF6)
- **Success**: Green (#22C55E)
- **Warning**: Yellow (#EAB308)
- **Error**: Red (#EF4444)

### Typography
- **Font**: Inter
- **Heading**: 600-700 weight
- **Body**: 400-500 weight

### Breakpoints
- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

---

## 📦 Tech Stack FE

| Công nghệ | Version | Mục đích |
|-----------|---------|----------|
| React | 19.x | UI Framework |
| Vite | 8.x | Build tool |
| TypeScript | 5.9 | Type safety |
| Tailwind CSS | 4.x | Styling |
| shadcn/ui | Latest | Components |
| React Router | 7.x | Routing |
| React Query | 5.x | Server state |
| Zustand | 4.x | Client state |
| MSW | 2.x | API mocking |
| Vitest | 4.x | Unit testing |
| Playwright | Latest | E2E testing |

---

## 🔄 Data Flow (FE Perspective)

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    USER     │────▶│  UI/COMP    │────▶│  API CALL   │
│  (Clicks)   │     │  (Render)   │     │ (React Qry) │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │   BACKEND   │
                                        │   (REST)    │
                                        └─────────────┘
```

**FE chỉ cần biết:**
- Gửi request gì
- Nhận response gì
- Hiển thị data nào

---

## 📝 Quy Tắc Viết Tài Liệu UI

Mỗi màn hình sẽ có format:

```markdown
## [Tên Màn hình]

### Mô tả
- Màn hình này dùng để làm gì

### Screenshot
- [Hình ảnh mockup]

### UI Elements
| Element | Loại | Data Field | Mô tả |
|---------|------|------------|-------|
| ... | ... | ... | ... |

### User Actions
- User có thể làm gì trên màn hình này

### Data Cần Thiết
- Data gì cần để render màn hình này
```

---

*Version: 1.0 - Updated: 2026-02-27*
