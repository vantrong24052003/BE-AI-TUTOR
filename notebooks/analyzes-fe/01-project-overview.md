# AI TUTOR - Project Overview

## 1. Giới thiệu dự án

**AI TUTOR** là nền tảng học tập trực tuyến thông minh, được thiết kế để cung cấp trải nghiệm học tập cá nhân hóa với sự hỗ trợ của AI.

### 1.1 Mục tiêu dự án

- Cung cấp nền tảng học tập trực tuyến hiện đại, dễ sử dụng
- Tích hợp AI Tutor để hỗ trợ người học 24/7
- Theo dõi tiến độ học tập chi tiết
- Hệ thống quiz thông minh với phản hồi tức thì
- Gamification để tăng động lực học tập

### 1.2 Đối tượng người dùng

| Người dùng | Mô tả |
|------------|-------|
| **Student** | Người học, có thể đăng ký khóa học, theo dõi tiến độ |
| **Instructor** | Giảng viên, tạo và quản lý nội dung khóa học |
| **Admin** | Quản trị viên, quản lý hệ thống |

## 2. Tech Stack

### 2.1 Frontend

| Công nghệ | Version | Mô tả |
|-----------|---------|-------|
| React | 19.x | UI Framework |
| Vite | 8.x | Build tool |
| TypeScript | 5.9 | Type safety |
| Tailwind CSS | 4.x | Styling |
| shadcn/ui | Latest | Component library |
| React Router | 7.x | Routing |
| React Query | 5.x | Server state |
| Zustand | 4.x | Client state |
| MSW | 2.x | API mocking |

### 2.2 Testing

| Công nghệ | Mô tả |
|-----------|-------|
| Vitest | Unit testing |
| React Testing Library | Component testing |
| Playwright | E2E testing |
| MSW | API mocking |

### 2.3 Tools

| Công cụ | Mô tả |
|---------|-------|
| ESLint | Linting |
| Prettier | Formatting |
| Husky | Git hooks |
| OpenSpec | Workflow management |

## 3. Cấu trúc dự án

```
FE-AI-TUTOR/
├── src/
│   ├── components/        # Shared components
│   │   ├── ui/           # shadcn/ui components
│   │   ├── layout/       # Layout components
│   │   └── common/       # Common components
│   ├── features/         # Feature modules
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── courses/
│   │   ├── learning/
│   │   ├── quiz/
│   │   └── profile/
│   ├── hooks/            # Custom hooks
│   ├── lib/              # Utilities
│   ├── services/         # API services
│   ├── stores/           # Zustand stores
│   ├── types/            # TypeScript types
│   ├── test/             # Test utilities
│   └── pages/            # Page components
├── e2e/                  # E2E tests
├── notebooks/            # Documentation
│   └── analyzes/         # Analysis docs
├── public/               # Static assets
└── configuration files
```

## 4. Features Overview

### 4.1 Authentication Module
- Login / Register / Logout
- Password recovery
- Social login (Google, Facebook)
- JWT authentication
- Role-based access

### 4.2 Dashboard Module
- Learning overview
- Progress statistics
- Recent courses
- AI recommendations

### 4.3 Course Module
- Course catalog
- Course detail
- Search & filter
- Categories
- Enrollment

### 4.4 Learning Module
- Video player
- Course content
- Note taking
- Progress tracking
- AI Tutor chat

### 4.5 Quiz Module
- Multiple choice
- Timed tests
- Instant feedback
- Score history

### 4.6 Profile Module
- Personal info
- Learning history
- Certificates
- Settings

### 4.7 Admin Module
- Course management
- User management
- Analytics
- Content moderation

## 5. Timeline dự kiến

| Phase | Thời gian | Nội dung |
|-------|-----------|----------|
| Phase 1 | 2 tuần | Setup, Auth, Layout |
| Phase 2 | 3 tuần | Dashboard, Courses |
| Phase 3 | 3 tuần | Learning, Quiz |
| Phase 4 | 2 tuần | Profile, Admin |
| Phase 5 | 2 tuần | Testing, Polish |

## 6. Success Metrics

| Metric | Target |
|--------|--------|
| Page Load Time | < 3s |
| First Contentful Paint | < 1.5s |
| Test Coverage | > 80% |
| Accessibility Score | > 90 |
| Lighthouse Score | > 90 |
