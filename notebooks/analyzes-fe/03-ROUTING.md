# FE AI TUTOR - Routing Structure

> Cấu trúc routing cho ứng dụng

---

## 1. ROUTE TREE

```
/                              → Landing Page (Public)
├── /auth
│   ├── /login                 → Login
│   ├── /register              → Register
│   └── /forgot-password       → Forgot Password
│
├── /app                       → Main App (Protected)
│   ├── /dashboard             → Dashboard
│   ├── /courses               → Course List
│   ├── /courses/:id           → Course Detail
│   ├── /my-courses            → Enrolled Courses
│   ├── /learn/:courseId
│   │   └── /lesson/:lessonId  → Learning
│   ├── /quiz/:quizId          → Quiz
│   ├── /ai-tutor              → AI Chat
│   └── /profile               → Profile
│
└── *                          → 404 Not Found
```

---

## 2. ROUTE CONFIGURATION

```tsx
// app/router/index.tsx
const routes = [
  // Public
  { path: '/', element: <LandingPage /> },

  // Auth
  { path: '/auth/login', element: <LoginPage /> },
  { path: '/auth/register', element: <RegisterPage /> },
  { path: '/auth/forgot-password', element: <ForgotPasswordPage /> },

  // Protected - Student
  {
    path: '/app',
    element: <ProtectedRoute><MainLayout /></ProtectedRoute>,
    children: [
      { path: 'dashboard', element: <DashboardPage /> },
      { path: 'courses', element: <CoursesPage /> },
      { path: 'courses/:id', element: <CourseDetailPage /> },
      { path: 'my-courses', element: <MyCoursesPage /> },
      { path: 'learn/:courseId/lesson/:lessonId', element: <LearningPage /> },
      { path: 'quiz/:quizId', element: <QuizPage /> },
      { path: 'ai-tutor', element: <AITutorPage /> },
      { path: 'profile', element: <ProfilePage /> },
    ],
  },

  // 404
  { path: '*', element: <NotFoundPage /> },
]
```

---

## 3. ROUTE GUARDS

```tsx
// components/auth/ProtectedRoute.tsx
interface ProtectedRouteProps {
  children: React.ReactNode
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated } = useAuthStore()
  const location = useLocation()

  if (!isAuthenticated) {
    return <Navigate to="/auth/login" state={{ from: location }} />
  }

  return <>{children}</>
}
```

---

## 4. PAGES CHECKLIST

### Public Pages
- [ ] LandingPage
- [ ] LoginPage
- [ ] RegisterPage
- [ ] ForgotPasswordPage
- [ ] NotFoundPage

### Student Pages
- [ ] DashboardPage
- [ ] CoursesPage
- [ ] CourseDetailPage
- [ ] MyCoursesPage
- [ ] LearningPage
- [ ] QuizPage
- [ ] AITutorPage
- [ ] ProfilePage

---

*Version: 1.1 - Updated: 2026-02-27*
