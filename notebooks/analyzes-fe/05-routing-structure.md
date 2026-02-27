# AI TUTOR - Routing Structure

## 1. Route Overview

### 1.1 Route Tree

```
/                           → Landing Page (Public)
├── /auth                   → Auth Layout
│   ├── /login              → Login Page
│   ├── /register           → Register Page
│   ├── /forgot-password    → Forgot Password
│   └── /reset-password     → Reset Password
├── /app                    → Main App Layout (Protected)
│   ├── /dashboard          → Dashboard
│   ├── /courses            → Course List
│   │   └── /:courseId      → Course Detail
│   ├── /learn              → Learning Layout
│   │   └── /:courseId
│   │       └── /lesson/:lessonId
│   ├── /quiz               → Quiz
│   │   └── /:quizId        → Quiz Detail
│   ├── /profile            → Profile
│   │   ├── /               → Overview
│   │   ├── /settings       → Settings
│   │   ├── /certificates   → Certificates
│   │   └── /history        → Learning History
│   └── /ai-tutor           → AI Tutor Chat
└── /admin                  → Admin Layout (Protected + Admin)
    ├── /                   → Admin Dashboard
    ├── /courses            → Course Management
    │   ├── /               → Course List
    │   ├── /create         → Create Course
    │   └── /:id            → Edit Course
    ├── /users              → User Management
    ├── /content            → Content Management
    └── /analytics          → Analytics
```

---

## 2. Route Configuration

```typescript
// router/index.tsx
import { createBrowserRouter, RouterProvider } from 'react-router'

const router = createBrowserRouter([
  // Public Routes
  {
    path: '/',
    element: <LandingPage />,
  },

  // Auth Routes
  {
    path: '/auth',
    element: <AuthLayout />,
    children: [
      { path: 'login', element: <LoginPage /> },
      { path: 'register', element: <RegisterPage /> },
      { path: 'forgot-password', element: <ForgotPasswordPage /> },
      { path: 'reset-password', element: <ResetPasswordPage /> },
    ],
  },

  // Protected Routes
  {
    path: '/app',
    element: <ProtectedRoute><MainLayout /></ProtectedRoute>,
    children: [
      { index: true, element: <Navigate to="/app/dashboard" /> },
      { path: 'dashboard', element: <DashboardPage /> },
      { path: 'courses', element: <CoursesPage /> },
      { path: 'courses/:courseId', element: <CourseDetailPage /> },
      {
        path: 'learn/:courseId',
        element: <LearningLayout />,
        children: [
          { index: true, element: <Navigate to="lesson" /> },
          { path: 'lesson', element: <LearningPage /> },
          { path: 'lesson/:lessonId', element: <LearningPage /> },
        ],
      },
      { path: 'quiz/:quizId', element: <QuizPage /> },
      {
        path: 'profile',
        children: [
          { index: true, element: <ProfilePage /> },
          { path: 'settings', element: <SettingsPage /> },
          { path: 'certificates', element: <CertificatesPage /> },
          { path: 'history', element: <HistoryPage /> },
        ],
      },
      { path: 'ai-tutor', element: <AITutorPage /> },
    ],
  },

  // Admin Routes
  {
    path: '/admin',
    element: <ProtectedRoute requiredRole="admin"><AdminLayout /></ProtectedRoute>,
    children: [
      { index: true, element: <AdminDashboard /> },
      { path: 'courses', element: <AdminCourses /> },
      { path: 'courses/create', element: <CreateCourse /> },
      { path: 'courses/:id', element: <EditCourse /> },
      { path: 'users', element: <AdminUsers /> },
      { path: 'content', element: <AdminContent /> },
      { path: 'analytics', element: <AdminAnalytics /> },
    ],
  },

  // 404
  { path: '*', element: <NotFoundPage /> },
])

export function AppRouter() {
  return <RouterProvider router={router} />
}
```

---

## 3. Route Protection

### 3.1 Protected Route Component

```typescript
// components/auth/ProtectedRoute.tsx
import { Navigate, useLocation } from 'react-router'
import { useAuthStore } from '@/stores/auth.store'

interface ProtectedRouteProps {
  children: React.ReactNode
  requiredRole?: 'student' | 'instructor' | 'admin'
}

export function ProtectedRoute({ children, requiredRole }: ProtectedRouteProps) {
  const { isAuthenticated, user } = useAuthStore()
  const location = useLocation()

  if (!isAuthenticated) {
    return <Navigate to="/auth/login" state={{ from: location }} replace />
  }

  if (requiredRole && user?.role !== requiredRole) {
    return <Navigate to="/app/dashboard" replace />
  }

  return <>{children}</>
}
```

### 3.2 Guest Route Component

```typescript
// components/auth/GuestRoute.tsx
import { Navigate } from 'react-router'
import { useAuthStore } from '@/stores/auth.store'

export function GuestRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuthStore()

  if (isAuthenticated) {
    return <Navigate to="/app/dashboard" replace />
  }

  return <>{children}</>
}
```

---

## 4. Layout Components

### 4.1 Auth Layout

```typescript
// layouts/AuthLayout.tsx
export function AuthLayout() {
  return (
    <div className="min-h-screen flex">
      {/* Left side - Form */}
      <div className="flex-1 flex items-center justify-center p-8">
        <Outlet />
      </div>

      {/* Right side - Branding */}
      <div className="hidden lg:flex flex-1 bg-primary items-center justify-center">
        <div className="text-white text-center">
          <h1 className="text-4xl font-bold">AI TUTOR</h1>
          <p className="mt-4 text-lg">Learn smarter, not harder</p>
        </div>
      </div>
    </div>
  )
}
```

### 4.2 Main Layout

```typescript
// layouts/MainLayout.tsx
export function MainLayout() {
  return (
    <div className="min-h-screen flex">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Navbar />
        <main className="flex-1 p-6 bg-gray-50">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
```

### 4.3 Learning Layout

```typescript
// layouts/LearningLayout.tsx
export function LearningLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <div className="h-screen flex flex-col">
      {/* Top bar */}
      <div className="h-14 border-b flex items-center px-4">
        <Button variant="ghost" onClick={() => setSidebarOpen(!sidebarOpen)}>
          <MenuIcon />
        </Button>
        <CourseTitle />
      </div>

      {/* Main content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Course sidebar */}
        {sidebarOpen && <CourseSidebar />}

        {/* Content area */}
        <div className="flex-1 overflow-auto">
          <Outlet />
        </div>

        {/* AI Tutor panel (optional) */}
        <AITutorPanel />
      </div>
    </div>
  )
}
```

### 4.4 Admin Layout

```typescript
// layouts/AdminLayout.tsx
export function AdminLayout() {
  return (
    <div className="min-h-screen flex">
      <AdminSidebar />
      <div className="flex-1 flex flex-col">
        <AdminHeader />
        <main className="flex-1 p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
```

---

## 5. Page Components

### 5.1 Public Pages

| Page | Path | Description |
|------|------|-------------|
| LandingPage | `/` | Homepage with features, testimonials |
| LoginPage | `/auth/login` | Login form |
| RegisterPage | `/auth/register` | Registration form |
| ForgotPasswordPage | `/auth/forgot-password` | Password recovery |
| ResetPasswordPage | `/auth/reset-password` | Reset password with token |

### 5.2 Protected Pages

| Page | Path | Description |
|------|------|-------------|
| DashboardPage | `/app/dashboard` | User dashboard |
| CoursesPage | `/app/courses` | Course catalog |
| CourseDetailPage | `/app/courses/:id` | Course detail |
| LearningPage | `/app/learn/:courseId/lesson/:lessonId` | Learning interface |
| QuizPage | `/app/quiz/:quizId` | Quiz interface |
| ProfilePage | `/app/profile` | User profile |
| SettingsPage | `/app/profile/settings` | Account settings |
| CertificatesPage | `/app/profile/certificates` | User certificates |
| HistoryPage | `/app/profile/history` | Learning history |
| AITutorPage | `/app/ai-tutor` | Standalone AI tutor |

### 5.3 Admin Pages

| Page | Path | Description |
|------|------|-------------|
| AdminDashboard | `/admin` | Admin overview |
| AdminCourses | `/admin/courses` | Course management |
| CreateCourse | `/admin/courses/create` | Create new course |
| EditCourse | `/admin/courses/:id` | Edit course |
| AdminUsers | `/admin/users` | User management |
| AdminContent | `/admin/content` | Content management |
| AdminAnalytics | `/admin/analytics` | Analytics dashboard |

---

## 6. Navigation Guards

### 6.1 Course Enrollment Guard

```typescript
// Ensures user is enrolled before accessing learning content
function EnrolledRoute({ children, courseId }: { children: React.ReactNode, courseId: string }) {
  const { data: enrollment, isLoading } = useEnrollment(courseId)

  if (isLoading) return <PageLoader />
  if (!enrollment) return <Navigate to={`/app/courses/${courseId}`} />

  return <>{children}</>
}
```

### 6.2 Lesson Progress Guard

```typescript
// Ensures previous lessons are completed (optional)
function LessonGuard({ children, lessonId }: { children: React.ReactNode, lessonId: string }) {
  const { data: progress } = useLessonProgress(lessonId)

  if (!progress?.canAccess) {
    return <Navigate to="/app/courses" state={{ message: "Complete previous lessons first" }} />
  }

  return <>{children}</>
}
```

---

## 7. Breadcrumb Configuration

```typescript
// config/breadcrumbs.ts
export const breadcrumbConfig = {
  '/app/dashboard': [{ label: 'Home', path: '/app/dashboard' }],
  '/app/courses': [
    { label: 'Home', path: '/app/dashboard' },
    { label: 'Courses', path: '/app/courses' },
  ],
  '/app/courses/:courseId': [
    { label: 'Home', path: '/app/dashboard' },
    { label: 'Courses', path: '/app/courses' },
    { label: ':courseId', path: '/app/courses/:courseId' }, // Dynamic
  ],
  '/app/learn/:courseId': [
    { label: 'Home', path: '/app/dashboard' },
    { label: 'Courses', path: '/app/courses' },
    { label: ':courseId', path: '/app/courses/:courseId' },
    { label: 'Learning', path: '/app/learn/:courseId' },
  ],
}
```
