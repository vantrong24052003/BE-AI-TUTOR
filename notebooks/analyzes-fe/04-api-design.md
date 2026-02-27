# AI TUTOR - API Design

## 1. API Architecture

### 1.1 Base Configuration

```typescript
// Base URL
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

// Request timeout
const API_TIMEOUT = 10000 // 10 seconds
```

### 1.2 Response Format

```typescript
// Success Response
interface APIResponse<T> {
  data: T
  message: string
  meta?: {
    page?: number
    limit?: number
    total?: number
  }
}

// Error Response
interface APIError {
  message: string
  code: string
  status: number
  errors?: Record<string, string[]>
}
```

---

## 2. Endpoints

### 2.1 Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login user |
| POST | `/auth/logout` | Logout user |
| POST | `/auth/refresh` | Refresh access token |
| POST | `/auth/forgot-password` | Request password reset |
| POST | `/auth/reset-password` | Reset password with token |
| GET | `/auth/me` | Get current user |

#### Register
```typescript
// POST /auth/register
// Request
{
  email: string
  password: string
  name: string
}

// Response
{
  data: {
    user: User
    accessToken: string
    refreshToken: string
  }
  message: "Registration successful"
}
```

#### Login
```typescript
// POST /auth/login
// Request
{
  email: string
  password: string
  rememberMe?: boolean
}

// Response
{
  data: {
    user: User
    accessToken: string
    refreshToken: string
  }
  message: "Login successful"
}
```

### 2.2 Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/me` | Get current user profile |
| PUT | `/users/me` | Update profile |
| PUT | `/users/me/password` | Change password |
| GET | `/users/me/courses` | Get enrolled courses |
| GET | `/users/me/progress` | Get learning progress |
| GET | `/users/me/certificates` | Get certificates |

#### Update Profile
```typescript
// PUT /users/me
// Request
{
  name?: string
  avatar?: string
  bio?: string
}

// Response
{
  data: User
  message: "Profile updated successfully"
}
```

### 2.3 Courses

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/courses` | Get all courses |
| GET | `/courses/:id` | Get course by ID |
| GET | `/courses/:id/lessons` | Get course lessons |
| POST | `/courses/:id/enroll` | Enroll in course |
| GET | `/courses/:id/progress` | Get course progress |
| GET | `/courses/categories` | Get categories |

#### Get Courses
```typescript
// GET /courses?page=1&limit=10&category=programming&level=beginner&search=react
// Query Params
{
  page?: number
  limit?: number
  category?: string
  level?: 'beginner' | 'intermediate' | 'advanced'
  search?: string
  sort?: 'popular' | 'newest' | 'rating'
}

// Response
{
  data: Course[]
  meta: {
    page: 1
    limit: 10
    total: 100
  }
}
```

#### Course Detail
```typescript
// GET /courses/:id
// Response
{
  data: {
    id: string
    title: string
    description: string
    thumbnail: string
    instructor: Instructor
    category: Category
    level: 'beginner' | 'intermediate' | 'advanced'
    duration: number // in minutes
    lessonsCount: number
    enrollmentsCount: number
    rating: number
    reviewsCount: number
    price: number
    isEnrolled: boolean
    curriculum: Module[]
  }
}
```

### 2.4 Lessons

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/lessons/:id` | Get lesson detail |
| PUT | `/lessons/:id/complete` | Mark lesson complete |
| GET | `/lessons/:id/notes` | Get lesson notes |
| POST | `/lessons/:id/notes` | Create note |
| PUT | `/lessons/:id/notes/:noteId` | Update note |
| DELETE | `/lessons/:id/notes/:noteId` | Delete note |

#### Lesson Detail
```typescript
// GET /lessons/:id
// Response
{
  data: {
    id: string
    title: string
    description: string
    type: 'video' | 'article' | 'quiz'
    duration: number
    videoUrl?: string
    content?: string
    isCompleted: boolean
    order: number
    moduleId: string
    prevLessonId?: string
    nextLessonId?: string
  }
}
```

### 2.5 Quiz

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/quiz/:lessonId` | Get quiz for lesson |
| POST | `/quiz/:quizId/submit` | Submit quiz answers |
| GET | `/quiz/:quizId/result` | Get quiz result |
| GET | `/quiz/:quizId/history` | Get quiz history |

#### Get Quiz
```typescript
// GET /quiz/:lessonId
// Response
{
  data: {
    id: string
    title: string
    description: string
    timeLimit: number // in minutes, 0 = no limit
    passingScore: number
    questions: Question[]
  }
}

interface Question {
  id: string
  text: string
  type: 'single' | 'multiple'
  options: {
    id: string
    text: string
  }[]
}
```

#### Submit Quiz
```typescript
// POST /quiz/:quizId/submit
// Request
{
  answers: {
    questionId: string
    selectedOptions: string[]
  }[]
}

// Response
{
  data: {
    score: number
    passed: boolean
    correctAnswers: number
    totalQuestions: number
    timeSpent: number
    details: {
      questionId: string
      isCorrect: boolean
      correctOptions: string[]
    }[]
  }
}
```

### 2.6 AI Tutor

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/ai/chat` | Send message to AI |
| GET | `/ai/chat/:sessionId` | Get chat history |
| POST | `/ai/chat/:sessionId/clear` | Clear chat history |

#### AI Chat
```typescript
// POST /ai/chat
// Request
{
  message: string
  context?: {
    courseId?: string
    lessonId?: string
    quizId?: string
  }
}

// Response (Streaming)
{
  data: {
    message: string
    sessionId: string
  }
}
```

### 2.7 Admin

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/users` | Get all users |
| PUT | `/admin/users/:id` | Update user |
| DELETE | `/admin/users/:id` | Delete user |
| GET | `/admin/courses` | Get all courses (admin view) |
| POST | `/admin/courses` | Create course |
| PUT | `/admin/courses/:id` | Update course |
| DELETE | `/admin/courses/:id` | Delete course |
| GET | `/admin/analytics` | Get analytics |

---

## 3. TypeScript Types

```typescript
// User
interface User {
  id: string
  email: string
  name: string
  avatar?: string
  role: 'student' | 'instructor' | 'admin'
  createdAt: string
  updatedAt: string
}

// Course
interface Course {
  id: string
  title: string
  description: string
  thumbnail: string
  instructor: Instructor
  category: Category
  level: 'beginner' | 'intermediate' | 'advanced'
  duration: number
  lessonsCount: number
  enrollmentsCount: number
  rating: number
  reviewsCount: number
  price: number
  isEnrolled?: boolean
  progress?: number
}

// Module
interface Module {
  id: string
  title: string
  order: number
  lessons: Lesson[]
}

// Lesson
interface Lesson {
  id: string
  title: string
  type: 'video' | 'article' | 'quiz'
  duration: number
  isCompleted?: boolean
  order: number
}

// Instructor
interface Instructor {
  id: string
  name: string
  avatar?: string
  bio?: string
}

// Category
interface Category {
  id: string
  name: string
  slug: string
}

// Quiz Result
interface QuizResult {
  id: string
  quizId: string
  score: number
  passed: boolean
  correctAnswers: number
  totalQuestions: number
  timeSpent: number
  completedAt: string
}
```

---

## 4. Service Layer

```typescript
// services/course.service.ts
import api from './api'
import type { Course, Module, Lesson } from '@/types'

export const courseService = {
  getAll: (params?: CourseQueryParams) =>
    api.get<APIResponse<Course[]>>('/courses', { params }),

  getById: (id: string) =>
    api.get<APIResponse<Course>>(`/courses/${id}`),

  enroll: (id: string) =>
    api.post<APIResponse<void>>(`/courses/${id}/enroll`),

  getProgress: (id: string) =>
    api.get<APIResponse<CourseProgress>>(`/courses/${id}/progress`),

  getLessons: (id: string) =>
    api.get<APIResponse<Module[]>>(`/courses/${id}/lessons`),
}
```

---

## 5. React Query Hooks

```typescript
// features/courses/hooks/useCourses.ts
import { useQuery } from '@tanstack/react-query'
import { courseService } from '@/services/course.service'

export function useCourses(params?: CourseQueryParams) {
  return useQuery({
    queryKey: ['courses', params],
    queryFn: () => courseService.getAll(params),
  })
}

export function useCourse(id: string) {
  return useQuery({
    queryKey: ['course', id],
    queryFn: () => courseService.getById(id),
    enabled: !!id,
  })
}

export function useCourseLessons(courseId: string) {
  return useQuery({
    queryKey: ['course-lessons', courseId],
    queryFn: () => courseService.getLessons(courseId),
    enabled: !!courseId,
  })
}
```
