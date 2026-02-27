# AI TUTOR - UI Components Documentation

## 1. UI Components Overview

### 1.1 Bảng tổng hợp Components

| STT | Category | Component | Tác dụng | Fields (Props) |
|-----|----------|-----------|----------|----------------|
| **LAYOUT** |
| 1 | Layout | `MainLayout` | Layout chính cho app | `children` |
| 2 | Layout | `AuthLayout` | Layout cho trang auth | `children` |
| 3 | Layout | `AdminLayout` | Layout cho admin panel | `children` |
| 4 | Layout | `Navbar` | Thanh navigation trên | - |
| 5 | Layout | `Sidebar` | Thanh sidebar bên trái | `collapsed`, `onToggle` |
| 6 | Layout | `Footer` | Chân trang | - |
| **COMMON** |
| 7 | Common | `PageLoader` | Loading toàn trang | - |
| 8 | Common | `EmptyState` | Hiển thị khi không có data | `icon`, `title`, `description`, `action` |
| 9 | Common | `ErrorMessage` | Hiển thị lỗi | `error`, `onRetry` |
| 10 | Common | `ConfirmDialog` | Dialog xác nhận | `open`, `title`, `message`, `onConfirm`, `onCancel` |
| 11 | Common | `StatsCard` | Card hiển thị thống kê | `title`, `value`, `icon`, `trend` |
| **AUTH** |
| 12 | Auth | `LoginForm` | Form đăng nhập | `onSuccess` |
| 13 | Auth | `RegisterForm` | Form đăng ký | `onSuccess` |
| 14 | Auth | `SocialLogin` | Nút đăng nhập social | `onGoogleLogin`, `onFacebookLogin` |
| **COURSES** |
| 15 | Courses | `CourseCard` | Card hiển thị khóa học | `course`, `variant`, `showProgress` |
| 16 | Courses | `CourseGrid` | Grid danh sách khóa học | `courses`, `loading` |
| 17 | Courses | `CourseFilters` | Bộ lọc khóa học | `filters`, `onChange` |
| 18 | Courses | `CourseHeader` | Header trang course detail | `course` |
| 19 | Courses | `Curriculum` | Danh sách modules/lessons | `modules`, `progress` |
| **LEARNING** |
| 20 | Learning | `VideoPlayer` | Player video bài học | `src`, `poster`, `onComplete`, `onProgress` |
| 21 | Learning | `CourseSidebar` | Sidebar danh sách bài | `course`, `currentLessonId`, `onSelect` |
| 22 | Learning | `LessonContent` | Nội dung bài học | `lesson` |
| 23 | Learning | `NotePanel` | Panel ghi chú | `lessonId`, `notes`, `onSave` |
| 24 | Learning | `ProgressIndicator` | Thanh tiến độ | `completed`, `total` |
| **QUIZ** |
| 25 | Quiz | `QuizPlayer` | Component quiz chính | `quiz`, `onComplete` |
| 26 | Quiz | `QuestionCard` | Card câu hỏi | `question`, `selectedAnswer`, `onAnswer`, `showResult` |
| 27 | Quiz | `QuizTimer` | Đồng hồ đếm ngược | `duration`, `onTimeUp` |
| 28 | Quiz | `QuizResult` | Hiển thị kết quả | `result`, `onRetry`, `onReview` |
| **AI TUTOR** |
| 29 | AI | `ChatWindow` | Cửa sổ chat | `messages`, `onSend`, `loading` |
| 30 | AI | `ChatMessage` | Tin nhắn đơn | `message` |
| 31 | AI | `ChatInput` | Ô nhập tin nhắn | `onSend`, `disabled` |
| 32 | AI | `SuggestionChips` | Gợi ý nhanh | `suggestions`, `onSelect` |

---

## 2. Chi tiết Components

### 2.1 LAYOUT COMPONENTS

---

#### LAYOUT-01: MainLayout
**Tác dụng:** Layout chính cho toàn bộ app (sau khi đăng nhập)

**Props:**
```typescript
interface MainLayoutProps {
  children: React.ReactNode
}
```

**Usage:**
```tsx
import { MainLayout } from '@/components/layout/MainLayout'

function AppRoutes() {
  return (
    <Routes>
      <Route path="/app" element={<MainLayout />}>
        <Route path="dashboard" element={<DashboardPage />} />
        <Route path="courses" element={<CoursesPage />} />
      </Route>
    </Routes>
  )
}
```

**Structure:**
```
┌─────────────────────────────────────┐
│             Navbar                  │
├──────────┬──────────────────────────┤
│          │                          │
│ Sidebar  │      Content Area        │
│          │      (children)          │
│          │                          │
└──────────┴──────────────────────────┘
```

---

#### LAYOUT-02: AuthLayout
**Tác dụng:** Layout cho các trang authentication

**Props:**
```typescript
interface AuthLayoutProps {
  children: React.ReactNode
}
```

**Usage:**
```tsx
import { AuthLayout } from '@/components/layout/AuthLayout'

function LoginPage() {
  return (
    <AuthLayout>
      <LoginForm />
    </AuthLayout>
  )
}
```

**Structure:**
```
┌─────────────────────┬─────────────────────┐
│                     │                     │
│    Form Area        │    Branding Area    │
│    (children)       │    (image/text)     │
│                     │                     │
└─────────────────────┴─────────────────────┘
```

---

#### LAYOUT-03: Navbar
**Tác dụng:** Thanh navigation trên cùng của app

**Props:** Không có (lấy data từ useAuthStore)

**Usage:**
```tsx
import { Navbar } from '@/components/layout/Navbar'

// Used inside MainLayout
<Navbar />
```

**UI Elements:**
- Logo + App name
- Search bar
- Notification bell
- User avatar dropdown (Profile, Settings, Logout)

---

#### LAYOUT-04: Sidebar
**Tác dụng:** Thanh sidebar điều hướng

**Props:**
```typescript
interface SidebarProps {
  collapsed?: boolean
  onToggle?: () => void
}
```

**Usage:**
```tsx
import { Sidebar } from '@/components/layout/Sidebar'

function MainLayout() {
  const { sidebarCollapsed, toggleSidebar } = useUIStore()

  return (
    <Sidebar collapsed={sidebarCollapsed} onToggle={toggleSidebar} />
  )
}
```

**UI Elements:**
- Dashboard link
- Courses link
- My Learning link
- AI Tutor link
- Profile link
- Admin section (if admin)

---

### 2.2 COMMON COMPONENTS

---

#### COMMON-01: PageLoader
**Tác dụng:** Loading spinner toàn trang (cho route transitions)

**Props:** Không có

**Usage:**
```tsx
import { PageLoader } from '@/components/common/PageLoader'

function CoursePage() {
  const { isLoading } = useCourse(id)

  if (isLoading) return <PageLoader />

  return <CourseContent />
}
```

---

#### COMMON-02: EmptyState
**Tác dụng:** Hiển thị khi không có data

**Props:**
```typescript
interface EmptyStateProps {
  icon?: React.ComponentType<{ className?: string }>
  title: string
  description?: string
  action?: {
    label: string
    onClick: () => void
  }
}
```

**Usage:**
```tsx
import { EmptyState } from '@/components/common/EmptyState'
import { BookOpen } from 'lucide-react'

function CoursesList({ courses }) {
  if (courses.length === 0) {
    return (
      <EmptyState
        icon={BookOpen}
        title="Chưa có khóa học nào"
        description="Bắt đầu khám phá các khóa học ngay"
        action={{
          label: "Khám phá",
          onClick: () => navigate('/courses')
        }}
      />
    )
  }

  return <CourseGrid courses={courses} />
}
```

---

#### COMMON-03: ErrorMessage
**Tác dụng:** Hiển thị lỗi với nút retry

**Props:**
```typescript
interface ErrorMessageProps {
  error: Error | string | APIError
  onRetry?: () => void
}
```

**Usage:**
```tsx
import { ErrorMessage } from '@/components/common/ErrorMessage'

function CoursePage() {
  const { data, isLoading, error, refetch } = useCourse(id)

  if (isLoading) return <PageLoader />
  if (error) return <ErrorMessage error={error} onRetry={refetch} />

  return <CourseContent course={data} />
}
```

---

#### COMMON-04: ConfirmDialog
**Tác dụng:** Dialog xác nhận hành động

**Props:**
```typescript
interface ConfirmDialogProps {
  open: boolean
  title: string
  message: string
  confirmText?: string
  cancelText?: string
  variant?: 'default' | 'destructive'
  onConfirm: () => void
  onCancel: () => void
}
```

**Usage:**
```tsx
import { ConfirmDialog } from '@/components/common/ConfirmDialog'

function CourseCard({ course }) {
  const [showConfirm, setShowConfirm] = useState(false)

  const handleUnenroll = () => {
    unenrollMutation.mutate(course.id)
    setShowConfirm(false)
  }

  return (
    <>
      <Button variant="destructive" onClick={() => setShowConfirm(true)}>
        Hủy đăng ký
      </Button>

      <ConfirmDialog
        open={showConfirm}
        title="Hủy đăng ký khóa học?"
        message="Bạn có chắc muốn hủy đăng ký? Tiến độ học tập sẽ bị mất."
        variant="destructive"
        onConfirm={handleUnenroll}
        onCancel={() => setShowConfirm(false)}
      />
    </>
  )
}
```

---

#### COMMON-05: StatsCard
**Tác dụng:** Card hiển thị thống kê

**Props:**
```typescript
interface StatsCardProps {
  title: string
  value: string | number
  icon?: React.ComponentType<{ className?: string }>
  trend?: {
    value: number
    isPositive: boolean
  }
  className?: string
}
```

**Usage:**
```tsx
import { StatsCard } from '@/components/common/StatsCard'
import { BookOpen, Clock, Trophy, TrendingUp } from 'lucide-react'

function DashboardStats({ stats }) {
  return (
    <div className="grid grid-cols-4 gap-4">
      <StatsCard
        title="Khóa học"
        value={stats.totalCourses}
        icon={BookOpen}
      />
      <StatsCard
        title="Giờ học"
        value={stats.learningHours}
        icon={Clock}
        trend={{ value: 12, isPositive: true }}
      />
      <StatsCard
        title="Hoàn thành"
        value={stats.completedLessons}
        icon={Trophy}
      />
      <StatsCard
        title="Streak"
        value={`${stats.streak} ngày`}
        icon={TrendingUp}
      />
    </div>
  )
}
```

---

### 2.3 COURSES COMPONENTS

---

#### CRS-01: CourseCard
**Tác dụng:** Card hiển thị thông tin khóa học

**Props:**
```typescript
interface CourseCardProps {
  course: Course
  variant?: 'default' | 'compact' | 'horizontal'
  showProgress?: boolean
  showInstructor?: boolean
  className?: string
}
```

**Usage:**
```tsx
import { CourseCard } from '@/features/courses/components/CourseCard'

function CourseGrid({ courses }) {
  return (
    <div className="grid grid-cols-3 gap-6">
      {courses.map(course => (
        <CourseCard
          key={course.id}
          course={course}
          showProgress={course.isEnrolled}
        />
      ))}
    </div>
  )
}

// Compact variant cho sidebar
<CourseCard course={course} variant="compact" />

// Horizontal variant cho list view
<CourseCard course={course} variant="horizontal" />
```

**UI Structure:**
```
┌─────────────────────────┐
│      Thumbnail          │
├─────────────────────────┤
│ Title                   │
│ Instructor name         │
│ Rating ⭐ | Students    │
│ [Progress Bar] (opt)    │
│ [Button: Enroll/Continue]│
└─────────────────────────┘
```

---

#### CRS-02: CourseFilters
**Tác dụng:** Bộ lọc cho danh sách khóa học

**Props:**
```typescript
interface CourseFiltersProps {
  filters: {
    category?: string
    level?: 'beginner' | 'intermediate' | 'advanced'
    price?: 'free' | 'paid'
    search?: string
  }
  categories: Category[]
  onChange: (filters: Filters) => void
}
```

**Usage:**
```tsx
import { CourseFilters } from '@/features/courses/components/CourseFilters'

function CoursesPage() {
  const [filters, setFilters] = useState({})
  const { data: categories } = useCategories()

  return (
    <div>
      <CourseFilters
        filters={filters}
        categories={categories}
        onChange={setFilters}
      />
      <CourseGrid filters={filters} />
    </div>
  )
}
```

---

#### CRS-03: Curriculum
**Tác dụng:** Hiển thị danh sách modules và lessons

**Props:**
```typescript
interface CurriculumProps {
  modules: Module[]
  currentLessonId?: string
  progress?: CourseProgress
  onLessonSelect?: (lessonId: string) => void
}
```

**Usage:**
```tsx
import { Curriculum } from '@/features/courses/components/Curriculum'

function CourseDetailPage() {
  const { data: course } = useCourse(courseId)

  return (
    <div>
      <CourseHeader course={course} />
      <Curriculum
        modules={course.curriculum}
        progress={course.progress}
      />
    </div>
  )
}
```

---

### 2.4 LEARNING COMPONENTS

---

#### LRN-01: VideoPlayer
**Tác dụng:** Player video cho bài học

**Props:**
```typescript
interface VideoPlayerProps {
  src: string
  poster?: string
  onComplete?: () => void
  onProgress?: (progress: VideoProgress) => void
}

interface VideoProgress {
  currentTime: number
  duration: number
  percentage: number
}
```

**Usage:**
```tsx
import { VideoPlayer } from '@/features/learning/components/VideoPlayer'

function LearningPage() {
  const { data: lesson } = useLesson(lessonId)
  const completeMutation = useCompleteLesson()

  const handleComplete = () => {
    completeMutation.mutate(lesson.id)
  }

  const handleProgress = (progress) => {
    // Save progress to server
    saveProgress(lesson.id, progress)
  }

  return (
    <VideoPlayer
      src={lesson.videoUrl}
      poster={lesson.thumbnail}
      onComplete={handleComplete}
      onProgress={handleProgress}
    />
  )
}
```

---

#### LRN-02: CourseSidebar
**Tác dụng:** Sidebar danh sách bài học

**Props:**
```typescript
interface CourseSidebarProps {
  course: CourseDetail
  currentLessonId?: string
  onLessonSelect: (lessonId: string) => void
}
```

**Usage:**
```tsx
import { CourseSidebar } from '@/features/learning/components/CourseSidebar'

function LearningLayout() {
  const { data: course } = useCourse(courseId)
  const [currentLessonId, setCurrentLessonId] = useState()

  return (
    <div className="flex">
      <CourseSidebar
        course={course}
        currentLessonId={currentLessonId}
        onLessonSelect={setCurrentLessonId}
      />
      <LessonContent lessonId={currentLessonId} />
    </div>
  )
}
```

---

#### LRN-03: NotePanel
**Tác dụng:** Panel ghi chú cá nhân

**Props:**
```typescript
interface NotePanelProps {
  lessonId: string
  notes: Note[]
  onSave: (content: string) => void
  onDelete?: (noteId: string) => void
}

interface Note {
  id: string
  content: string
  timestamp: number // Video timestamp
  createdAt: string
}
```

**Usage:**
```tsx
import { NotePanel } from '@/features/learning/components/NotePanel'

function LearningPage() {
  const { data: notes } = useNotes(lessonId)
  const saveNoteMutation = useSaveNote()

  return (
    <div className="flex">
      <VideoPlayer src={videoUrl} />
      <NotePanel
        lessonId={lessonId}
        notes={notes}
        onSave={(content) => saveNoteMutation.mutate({ lessonId, content })}
      />
    </div>
  )
}
```

---

### 2.5 QUIZ COMPONENTS

---

#### QIZ-01: QuizPlayer
**Tác dụng:** Component chính để làm quiz

**Props:**
```typescript
interface QuizPlayerProps {
  quiz: Quiz
  onComplete: (result: QuizResult) => void
}

interface Quiz {
  id: string
  title: string
  timeLimit: number
  passingScore: number
  questions: Question[]
}
```

**Usage:**
```tsx
import { QuizPlayer } from '@/features/quiz/components/QuizPlayer'

function QuizPage() {
  const { data: quiz } = useQuiz(lessonId)

  const handleComplete = (result) => {
    // Navigate to result page or show result modal
    navigate(`/quiz/${quiz.id}/result`, { state: result })
  }

  return <QuizPlayer quiz={quiz} onComplete={handleComplete} />
}
```

---

#### QIZ-02: QuestionCard
**Tác dụng:** Card hiển thị câu hỏi

**Props:**
```typescript
interface QuestionCardProps {
  question: Question
  questionNumber: number
  selectedAnswer?: string[]
  onAnswer: (optionIds: string[]) => void
  showResult?: boolean
  correctOptions?: string[]
}
```

**Usage:**
```tsx
import { QuestionCard } from '@/features/quiz/components/QuestionCard'

function QuizPlayer({ quiz }) {
  const [answers, setAnswers] = useState<Record<string, string[]>>({})
  const [showResults, setShowResults] = useState(false)

  return (
    <div>
      {quiz.questions.map((q, index) => (
        <QuestionCard
          key={q.id}
          question={q}
          questionNumber={index + 1}
          selectedAnswer={answers[q.id]}
          onAnswer={(options) => setAnswers(prev => ({
            ...prev,
            [q.id]: options
          }))}
          showResult={showResults}
        />
      ))}
    </div>
  )
}
```

---

#### QIZ-03: QuizResult
**Tác dụng:** Hiển thị kết quả quiz

**Props:**
```typescript
interface QuizResultProps {
  result: QuizResult
  onRetry?: () => void
  onReview?: () => void
  onContinue?: () => void
}

interface QuizResult {
  score: number
  passed: boolean
  correctAnswers: number
  totalQuestions: number
  timeSpent: number
}
```

**Usage:**
```tsx
import { QuizResult } from '@/features/quiz/components/QuizResult'

function QuizResultPage() {
  const result = useLocation().state

  return (
    <QuizResult
      result={result}
      onRetry={() => navigate(`/quiz/${quizId}`)}
      onReview={() => navigate(`/quiz/${quizId}/review`)}
      onContinue={() => navigate(`/learn/${courseId}`)}
    />
  )
}
```

---

### 2.6 AI TUTOR COMPONENTS

---

#### AI-01: ChatWindow
**Tác dụng:** Cửa sổ chat với AI Tutor

**Props:**
```typescript
interface ChatWindowProps {
  messages: ChatMessage[]
  onSend: (message: string) => void
  isLoading?: boolean
  placeholder?: string
}
```

**Usage:**
```tsx
import { ChatWindow } from '@/features/ai-tutor/components/ChatWindow'

function AITutorPage() {
  const { messages, sendMessage, isLoading } = useChat()

  return (
    <ChatWindow
      messages={messages}
      onSend={sendMessage}
      isLoading={isLoading}
      placeholder="Hỏi AI Tutor về bài học..."
    />
  )
}
```

---

#### AI-02: ChatMessage
**Tác dụng:** Tin nhắn đơn trong chat

**Props:**
```typescript
interface ChatMessageProps {
  message: {
    id: string
    role: 'user' | 'assistant'
    content: string
    createdAt: string
  }
  showTimestamp?: boolean
}
```

**Usage:**
```tsx
import { ChatMessage } from '@/features/ai-tutor/components/ChatMessage'

function ChatWindow({ messages }) {
  return (
    <div className="flex flex-col gap-4">
      {messages.map(msg => (
        <ChatMessage key={msg.id} message={msg} />
      ))}
    </div>
  )
}
```

---

## 3. Component Pattern Template

### 3.1 Standard Component Pattern

```tsx
// features/[feature]/components/[Component].tsx

// 1. Imports
import { useState, useCallback } from 'react'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
import type { SomeType } from '../types'

// 2. Types
interface ComponentProps {
  // Required props first
  data: SomeType
  // Optional props with descriptions
  /** Callback khi user click */
  onClick?: (id: string) => void
  /** Variant style */
  variant?: 'default' | 'compact'
  /** Additional className */
  className?: string
}

// 3. Component
export function Component({
  data,
  onClick,
  variant = 'default',
  className,
}: ComponentProps) {
  // 4. Hooks
  const [isOpen, setIsOpen] = useState(false)

  // 5. Derived state
  const isCompact = variant === 'compact'

  // 6. Callbacks
  const handleClick = useCallback(() => {
    onClick?.(data.id)
  }, [onClick, data.id])

  // 7. Early returns
  if (!data) return null

  // 8. Render
  return (
    <div className={cn('base-classes', className)}>
      {/* Content */}
    </div>
  )
}
```

### 3.2 Component with Children Pattern

```tsx
interface CardProps {
  children: React.ReactNode
  className?: string
}

export function Card({ children, className }: CardProps) {
  return (
    <div className={cn('rounded-lg border bg-card p-4', className)}>
      {children}
    </div>
  )
}

// Usage
<Card>
  <CardHeader>Title</CardHeader>
  <CardContent>Content</CardContent>
</Card>
```
