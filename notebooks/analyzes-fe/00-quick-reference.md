# AI TUTOR - Quick Reference Index

## Tài liệu phân tích

| STT | File | Nội dung |
|-----|------|----------|
| 01 | [project-overview.md](./01-project-overview.md) | Tổng quan dự án, tech stack, features |
| 02 | [feature-analysis.md](./02-feature-analysis.md) | Phân tích chi tiết từng feature |
| 03 | [ui-components.md](./03-ui-components.md) | Design system, shadcn components |
| 04 | [api-design.md](./04-api-design.md) | API endpoints, types, services |
| 05 | [routing-structure.md](./05-routing-structure.md) | Routing, layouts, guards |
| 06 | [source-code-structure.md](./06-source-code-structure.md) | Cấu trúc code, conventions |
| 07 | [api-documentation.md](./07-api-documentation.md) | **Chi tiết API & JSON structure** |
| 08 | [ui-components-documentation.md](./08-ui-components-documentation.md) | **Chi tiết UI Components** |

---

## Quick Links

### API Reference

| Feature | Endpoints |
|---------|-----------|
| Auth | `POST /auth/register`, `POST /auth/login`, `POST /auth/logout` |
| Users | `GET /users/me`, `PUT /users/me`, `GET /users/me/courses` |
| Courses | `GET /courses`, `GET /courses/:id`, `POST /courses/:id/enroll` |
| Lessons | `GET /lessons/:id`, `PUT /lessons/:id/complete` |
| Quiz | `GET /quiz/:lessonId`, `POST /quiz/:quizId/submit` |
| AI | `POST /ai/chat` |

👉 [Xem chi tiết API](./07-api-documentation.md)

---

### Components Reference

| Category | Components |
|----------|------------|
| Layout | `MainLayout`, `AuthLayout`, `Navbar`, `Sidebar` |
| Common | `PageLoader`, `EmptyState`, `ErrorMessage`, `ConfirmDialog`, `StatsCard` |
| Auth | `LoginForm`, `RegisterForm`, `SocialLogin` |
| Courses | `CourseCard`, `CourseGrid`, `CourseFilters`, `Curriculum` |
| Learning | `VideoPlayer`, `CourseSidebar`, `NotePanel`, `ProgressIndicator` |
| Quiz | `QuizPlayer`, `QuestionCard`, `QuizTimer`, `QuizResult` |
| AI | `ChatWindow`, `ChatMessage`, `ChatInput`, `SuggestionChips` |

👉 [Xem chi tiết Components](./08-ui-components-documentation.md)

---

### Folder Structure

```
src/
├── app/           # Router, providers
├── components/    # Shared components (ui, layout, common)
├── features/      # Feature modules
├── pages/         # Page components
├── hooks/         # Global hooks
├── lib/           # Utilities
├── services/      # API services
├── stores/        # Zustand stores
├── types/         # TypeScript types
└── test/          # Test utilities
```

👉 [Xem chi tiết cấu trúc](./06-source-code-structure.md)

---

## Development Checklist

### Trước khi code

- [ ] Đọc tài liệu phân tích
- [ ] Hiểu feature requirements
- [ ] Xác định components cần tạo
- [ ] Xác định API cần gọi

### Khi code

- [ ] Đặt file đúng vị trí theo cấu trúc
- [ ] Follow naming conventions
- [ ] Define types rõ ràng
- [ ] Viết barrel exports
- [ ] Comment complex logic

### Sau khi code

- [ ] Chạy `npm run lint`
- [ ] Chạy `npm run prettier:fix`
- [ ] Chạy `npm run test`
- [ ] Tạo commit đúng format

---

## Common Commands

```bash
# Development
npm run dev

# Build
npm run build

# Linting
npm run lint
npm run lint:fix

# Formatting
npm run prettier
npm run prettier:fix

# Testing
npm run test
npm run test:ui
npm run test:coverage

# E2E Testing
npm run test:e2e
npm run test:e2e:ui

# Add shadcn component
npx shadcn@latest add [component-name]
```
