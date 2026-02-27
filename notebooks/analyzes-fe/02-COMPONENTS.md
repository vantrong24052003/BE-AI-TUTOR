# FE AI TUTOR - Components Library

> Danh sách components cần build cho FE

---

## 1. COMPONENTS OVERVIEW

| STT | Category | Component | Dùng ở đâu | Mô tả |
|-----|----------|-----------|------------|-------|
| **LAYOUT** |
| 1 | Layout | `Navbar` | Tất cả pages | Thanh nav trên |
| 2 | Layout | `Sidebar` | App pages | Sidebar bên trái |
| 3 | Layout | `Footer` | Landing page | Chân trang |
| 4 | Layout | `MainLayout` | App pages | Layout chính |
| 5 | Layout | `AuthLayout` | Auth pages | Layout auth |
| **COMMON** |
| 6 | Common | `PageLoader` | Tất cả | Loading spinner |
| 7 | Common | `EmptyState` | List pages | Không có data |
| 8 | Common | `ErrorMessage` | Tất cả | Hiển thị lỗi |
| 9 | Common | `ConfirmDialog` | Tất cả | Dialog xác nhận |
| 10 | Common | `StatsCard` | Dashboard | Card thống kê |
| **AUTH** |
| 11 | Auth | `LoginForm` | Login page | Form đăng nhập |
| 12 | Auth | `RegisterForm` | Register page | Form đăng ký |
| **COURSES** |
| 13 | Courses | `CourseCard` | Course list | Card khóa học |
| 14 | Courses | `CourseFilters` | Course list | Bộ lọc |
| 15 | Courses | `Curriculum` | Course detail | Danh sách bài |
| **LEARNING** |
| 16 | Learning | `VideoPlayer` | Learning page | Player video |
| 17 | Learning | `CourseSidebar` | Learning page | Sidebar bài học |
| 18 | Learning | `NotePanel` | Learning page | Ghi chú |
| **QUIZ** |
| 19 | Quiz | `QuizPlayer` | Quiz page | Làm quiz |
| 20 | Quiz | `QuestionCard` | Quiz page | Câu hỏi |
| 21 | Quiz | `QuizResult` | Quiz page | Kết quả |
| **AI** |
| 22 | AI | `ChatWindow` | AI page | Cửa sổ chat |
| 23 | AI | `ChatMessage` | AI page | Tin nhắn |
| 24 | AI | `ChatInput` | AI page | Input chat |

---

## 2. LAYOUT COMPONENTS

### 2.1 Navbar

**Vị trí:** Tất cả pages (sau login)

**UI Elements:**
| Element | Loại | Mô tả |
|---------|------|-------|
| Logo | Image/Link | Click về dashboard |
| Search | Input | Tìm kiếm khóa học |
| Notification | Icon + Badge | Thông báo |
| Avatar | Image + Dropdown | Menu: Profile, Settings, Logout |

**Code Structure:**
```tsx
// components/layout/Navbar.tsx
export function Navbar() {
  return (
    <header className="h-16 border-b">
      <Logo />
      <SearchBar />
      <NotificationBell />
      <UserMenu />
    </header>
  )
}
```

---

### 2.2 Sidebar

**Vị trí:** App pages

**UI Elements:**
| Element | Loại | Mô tả |
|---------|------|-------|
| Dashboard | Link | → /app/dashboard |
| Courses | Link | → /app/courses |
| My Learning | Link | → /app/my-courses |
| AI Tutor | Link | → /app/ai-tutor |
| Profile | Link | → /app/profile |

**Code Structure:**
```tsx
// components/layout/Sidebar.tsx
export function Sidebar() {
  return (
    <aside className="w-64 border-r">
      <NavItem icon={Home} label="Dashboard" href="/app/dashboard" />
      <NavItem icon={Book} label="Courses" href="/app/courses" />
      <NavItem icon={GraduationCap} label="My Learning" href="/app/my-courses" />
      <NavItem icon={Bot} label="AI Tutor" href="/app/ai-tutor" />
      <NavItem icon={User} label="Profile" href="/app/profile" />
    </aside>
  )
}
```

---

## 3. COMMON COMPONENTS

### 3.1 PageLoader

**Vị trí:** Route transitions, data loading

**UI:** Spinner toàn trang

```tsx
// components/common/PageLoader.tsx
export function PageLoader() {
  return (
    <div className="flex h-[50vh] items-center justify-center">
      <Loader2 className="h-8 w-8 animate-spin text-primary" />
    </div>
  )
}
```

---

### 3.2 EmptyState

**Vị trí:** List pages khi không có data

**UI Elements:**
| Element | Loại | Mô tả |
|---------|------|-------|
| Icon | Icon | Icon minh họa |
| Title | Text | Tiêu đề |
| Description | Text | Mô tả |
| Action | Button | Nút hành động (optional) |

```tsx
// components/common/EmptyState.tsx
interface EmptyStateProps {
  icon?: React.ComponentType
  title: string
  description?: string
  action?: {
    label: string
    onClick: () => void
  }
}

export function EmptyState({ icon: Icon, title, description, action }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center py-12">
      {Icon && <Icon className="h-12 w-12 text-muted-foreground" />}
      <h3 className="mt-4 text-lg font-semibold">{title}</h3>
      {description && <p className="text-muted-foreground">{description}</p>}
      {action && <Button onClick={action.onClick}>{action.label}</Button>}
    </div>
  )
}
```

---

### 3.3 StatsCard

**Vị trí:** Dashboard

**UI Elements:**
| Element | Loại | Mô tả |
|---------|------|-------|
| Icon | Icon | Icon |
| Title | Text | Tiêu đề stat |
| Value | Text | Giá trị |
| Trend | Text + Icon | Xu hướng (optional) |

```tsx
// components/common/StatsCard.tsx
interface StatsCardProps {
  title: string
  value: string | number
  icon?: React.ComponentType
  trend?: { value: number; isPositive: boolean }
}

export function StatsCard({ title, value, icon: Icon, trend }: StatsCardProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        {Icon && <Icon className="h-4 w-4 text-muted-foreground" />}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        {trend && (
          <p className={trend.isPositive ? 'text-green-600' : 'text-red-600'}>
            {trend.isPositive ? '+' : '-'}{trend.value}%
          </p>
        )}
      </CardContent>
    </Card>
  )
}
```

---

## 4. COURSE COMPONENTS

### 4.1 CourseCard

**Vị trí:** Course list, Dashboard

**UI Elements:**
| Element | Loại | Field | Mô tả |
|---------|------|-------|-------|
| Thumbnail | Image | `thumbnail` | Ảnh khóa |
| Title | Text | `title` | Tên khóa |
| Instructor | Text | `instructor.name` | Tên GV |
| Rating | Stars + Text | `rating` | Đánh giá |
| Students | Text | `studentsCount` | Số HV |
| Price | Text | `price` | Giá |
| Progress | Bar | `progress` | Tiến độ (optional) |
| Button | Button | - | Enroll/Continue |

```tsx
// features/courses/components/CourseCard.tsx
interface CourseCardProps {
  course: {
    id: string
    title: string
    thumbnail: string
    instructor: { name: string }
    rating: number
    studentsCount: number
    price: number
    isEnrolled?: boolean
    progress?: number
  }
}

export function CourseCard({ course }: CourseCardProps) {
  return (
    <Card>
      <img src={course.thumbnail} className="h-48 w-full object-cover" />
      <CardContent>
        <h3 className="font-semibold">{course.title}</h3>
        <p className="text-sm text-muted-foreground">{course.instructor.name}</p>
        <div className="flex items-center gap-2">
          <StarRating value={course.rating} />
          <span>({course.studentsCount})</span>
        </div>
        {course.isEnrolled && <Progress value={course.progress} />}
      </CardContent>
      <CardFooter>
        <Button asChild>
          <Link to={`/courses/${course.id}`}>
            {course.isEnrolled ? 'Continue' : course.price === 0 ? 'Free' : `$${course.price}`}
          </Link>
        </Button>
      </CardFooter>
    </Card>
  )
}
```

---

### 4.2 Curriculum

**Vị trí:** Course detail

**UI Elements:**
| Element | Loại | Mô tả |
|---------|------|-------|
| Module | Accordion | Tiêu đề module |
| Lesson | List Item | Tên bài + duration |
| Status | Icon | Completed/In Progress/Locked |

```tsx
// features/courses/components/Curriculum.tsx
interface CurriculumProps {
  modules: Array<{
    id: string
    title: string
    lessons: Array<{
      id: string
      title: string
      duration: number
      isCompleted: boolean
    }>
  }>
}

export function Curriculum({ modules }: CurriculumProps) {
  return (
    <div className="space-y-4">
      {modules.map(module => (
        <Accordion key={module.id} type="single">
          <AccordionItem value={module.id}>
            <AccordionTrigger>{module.title}</AccordionTrigger>
            <AccordionContent>
              {module.lessons.map(lesson => (
                <LessonItem key={lesson.id} lesson={lesson} />
              ))}
            </AccordionContent>
          </AccordionItem>
        </Accordion>
      ))}
    </div>
  )
}
```

---

## 5. LEARNING COMPONENTS

### 5.1 VideoPlayer

**Vị trí:** Learning page

**UI Elements:**
| Element | Loại | Mô tả |
|---------|------|-------|
| Video | HTML5 Video | Player video |
| Controls | Custom | Play, Pause, Volume, Progress, Fullscreen |
| Progress | Bar | Tiến độ video |

```tsx
// features/learning/components/VideoPlayer.tsx
interface VideoPlayerProps {
  src: string
  poster?: string
  onComplete?: () => void
  onProgress?: (progress: number) => void
}

export function VideoPlayer({ src, poster, onComplete, onProgress }: VideoPlayerProps) {
  const videoRef = useRef<HTMLVideoElement>(null)

  return (
    <div className="relative aspect-video bg-black">
      <video
        ref={videoRef}
        src={src}
        poster={poster}
        className="h-full w-full"
        controls
      />
    </div>
  )
}
```

---

### 5.2 CourseSidebar

**Vị trí:** Learning page

**UI Elements:**
| Element | Loại | Mô tả |
|---------|------|-------|
| Course Info | Header | Tên khóa |
| Progress | Bar | Tiến độ tổng |
| Module List | Accordion | Danh sách modules |
| Lesson | List Item | Click để chuyển bài |

```tsx
// features/learning/components/CourseSidebar.tsx
interface CourseSidebarProps {
  course: Course
  currentLessonId: string
  onLessonSelect: (lessonId: string) => void
}

export function CourseSidebar({ course, currentLessonId, onLessonSelect }: CourseSidebarProps) {
  return (
    <aside className="w-80 border-l">
      <div className="p-4">
        <h2 className="font-semibold">{course.title}</h2>
        <Progress value={course.progress} className="mt-2" />
      </div>
      <ScrollArea>
        {course.modules.map(module => (
          <ModuleSection
            key={module.id}
            module={module}
            currentLessonId={currentLessonId}
            onLessonSelect={onLessonSelect}
          />
        ))}
      </ScrollArea>
    </aside>
  )
}
```

---

## 6. QUIZ COMPONENTS

### 6.1 QuizPlayer

**Vị trí:** Quiz page

**UI Elements:**
| Element | Loại | Mô tả |
|---------|------|-------|
| Header | Bar | Title, Timer, Progress |
| Question | Card | Câu hỏi + options |
| Navigation | Buttons | Prev, Next, Submit |
| Progress | Dots | Trạng thái từng câu |

```tsx
// features/quiz/components/QuizPlayer.tsx
interface QuizPlayerProps {
  quiz: {
    id: string
    title: string
    timeLimit: number
    questions: Question[]
  }
  onComplete: (answers: Answers) => void
}

export function QuizPlayer({ quiz, onComplete }: QuizPlayerProps) {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [answers, setAnswers] = useState<Record<string, string[]>>({})

  return (
    <div>
      <QuizHeader title={quiz.title} timeLimit={quiz.timeLimit} />
      <QuestionCard
        question={quiz.questions[currentIndex]}
        selectedAnswer={answers[quiz.questions[currentIndex].id]}
        onAnswer={(options) => setAnswers(prev => ({ ...prev, [quiz.questions[currentIndex].id]: options }))}
      />
      <QuizNavigation
        currentIndex={currentIndex}
        total={quiz.questions.length}
        onPrev={() => setCurrentIndex(i => i - 1)}
        onNext={() => setCurrentIndex(i => i + 1)}
        onSubmit={() => onComplete(answers)}
      />
    </div>
  )
}
```

---

### 6.2 QuestionCard

**Vị trí:** Quiz page

**UI Elements:**
| Element | Loại | Mô tả |
|---------|------|-------|
| Question Text | Text | Nội dung câu hỏi |
| Options | Radio/Checkbox | A, B, C, D |
| Result | Icon + Color | Đúng/Sai (khi show result) |

```tsx
// features/quiz/components/QuestionCard.tsx
interface QuestionCardProps {
  question: {
    id: string
    text: string
    type: 'single' | 'multiple'
    options: Array<{ id: string; text: string }>
  }
  selectedAnswer?: string[]
  onAnswer: (optionIds: string[]) => void
  showResult?: boolean
  correctOptions?: string[]
}

export function QuestionCard({ question, selectedAnswer, onAnswer, showResult, correctOptions }: QuestionCardProps) {
  const handleSelect = (optionId: string) => {
    if (question.type === 'single') {
      onAnswer([optionId])
    } else {
      // Multiple - toggle selection
    }
  }

  return (
    <Card>
      <CardContent>
        <p className="text-lg font-medium">{question.text}</p>
        <div className="mt-4 space-y-2">
          {question.options.map(option => (
            <OptionButton
              key={option.id}
              option={option}
              selected={selectedAnswer?.includes(option.id)}
              onClick={() => handleSelect(option.id)}
              showResult={showResult}
              isCorrect={correctOptions?.includes(option.id)}
            />
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
```

---

## 7. AI CHAT COMPONENTS

### 7.1 ChatWindow

**Vị trí:** AI Tutor page

**UI Elements:**
| Element | Loại | Mô tả |
|---------|------|-------|
| Header | Bar | Title + New chat |
| Context | Select | Chọn khóa học context |
| Messages | List | Danh sách tin nhắn |
| Input | Input | Nhập tin nhắn |
| Suggestions | Chips | Gợi ý nhanh |

```tsx
// features/ai-tutor/components/ChatWindow.tsx
interface ChatWindowProps {
  messages: ChatMessage[]
  onSend: (message: string) => void
  isLoading?: boolean
}

export function ChatWindow({ messages, onSend, isLoading }: ChatWindowProps) {
  const [input, setInput] = useState('')

  return (
    <div className="flex h-full flex-col">
      <ChatHeader />
      <ContextSelector />
      <ScrollArea className="flex-1">
        {messages.map(msg => (
          <ChatMessage key={msg.id} message={msg} />
        ))}
        {isLoading && <TypingIndicator />}
      </ScrollArea>
      <SuggestionChips onSelect={setInput} />
      <ChatInput
        value={input}
        onChange={setInput}
        onSend={() => {
          onSend(input)
          setInput('')
        }}
      />
    </div>
  )
}
```

---

### 7.2 ChatMessage

**Vị trí:** Trong ChatWindow

**UI Elements:**
| Element | Loại | Mô tả |
|---------|------|-------|
| Avatar | Image | User hoặc AI avatar |
| Content | Text/Markdown | Nội dung tin nhắn |
| Timestamp | Text | Thời gian |

```tsx
// features/ai-tutor/components/ChatMessage.tsx
interface ChatMessageProps {
  message: {
    id: string
    role: 'user' | 'assistant'
    content: string
    createdAt: string
  }
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user'

  return (
    <div className={cn('flex gap-3 p-4', isUser && 'flex-row-reverse')}>
      <Avatar>
        {isUser ? <UserAvatar /> : <AIAvatar />}
      </Avatar>
      <div className={cn('rounded-lg p-3', isUser ? 'bg-primary text-white' : 'bg-muted')}>
        <Markdown content={message.content} />
      </div>
    </div>
  )
}
```

---

## 8. FILE STRUCTURE

```
src/
├── components/
│   ├── ui/              # shadcn components
│   ├── layout/
│   │   ├── Navbar.tsx
│   │   ├── Sidebar.tsx
│   │   ├── Footer.tsx
│   │   ├── MainLayout.tsx
│   │   └── AuthLayout.tsx
│   └── common/
│       ├── PageLoader.tsx
│       ├── EmptyState.tsx
│       ├── ErrorMessage.tsx
│       ├── ConfirmDialog.tsx
│       └── StatsCard.tsx
│
├── features/
│   ├── auth/components/
│   │   ├── LoginForm.tsx
│   │   └── RegisterForm.tsx
│   ├── courses/components/
│   │   ├── CourseCard.tsx
│   │   ├── CourseFilters.tsx
│   │   └── Curriculum.tsx
│   ├── learning/components/
│   │   ├── VideoPlayer.tsx
│   │   ├── CourseSidebar.tsx
│   │   └── NotePanel.tsx
│   ├── quiz/components/
│   │   ├── QuizPlayer.tsx
│   │   ├── QuestionCard.tsx
│   │   └── QuizResult.tsx
│   └── ai-tutor/components/
│       ├── ChatWindow.tsx
│       ├── ChatMessage.tsx
│       └── ChatInput.tsx
```

---

*Version: 1.0 - Updated: 2026-02-27*
