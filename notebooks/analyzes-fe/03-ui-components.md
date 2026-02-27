# AI TUTOR - UI Components Library

## 1. Design System

### 1.1 Color Palette

```css
/* Primary Colors */
--primary-50: #EFF6FF;
--primary-100: #DBEAFE;
--primary-200: #BFDBFE;
--primary-300: #93C5FD;
--primary-400: #60A5FA;
--primary-500: #3B82F6;  /* Main */
--primary-600: #2563EB;
--primary-700: #1D4ED8;
--primary-800: #1E40AF;
--primary-900: #1E3A8A;

/* Secondary Colors */
--secondary-500: #8B5CF6;

/* Semantic Colors */
--success-500: #22C55E;
--warning-500: #EAB308;
--error-500: #EF4444;
--info-500: #3B82F6;

/* Neutral Colors */
--gray-50: #F9FAFB;
--gray-100: #F3F4F6;
--gray-200: #E5E7EB;
--gray-300: #D1D5DB;
--gray-400: #9CA3AF;
--gray-500: #6B7280;
--gray-600: #4B5563;
--gray-700: #374151;
--gray-800: #1F2937;
--gray-900: #111827;
```

### 1.2 Typography

```css
/* Font Family */
font-family: 'Inter', system-ui, sans-serif;

/* Font Sizes */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */

/* Font Weights */
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

### 1.3 Spacing

```css
/* Spacing Scale */
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
```

### 1.4 Border Radius

```css
--radius-sm: 0.25rem;  /* 4px */
--radius-md: 0.375rem; /* 6px */
--radius-lg: 0.5rem;   /* 8px */
--radius-xl: 0.75rem;  /* 12px */
--radius-2xl: 1rem;    /* 16px */
--radius-full: 9999px;
```

---

## 2. shadcn/ui Components Used

### 2.1 Already Installed

| Component | Usage |
|-----------|-------|
| Button | Primary actions, links |
| Card | Course cards, content containers |
| Input | Forms, search |
| Dialog | Modals, confirmations |
| Dropdown | Menus, selects |
| Avatar | User avatars |
| Badge | Status, labels |
| Progress | Progress bars |
| Skeleton | Loading states |
| Tabs | Content organization |
| Toast | Notifications |

### 2.2 Components to Add

```bash
# Layout
npx shadcn@latest add separator
npx shadcn@latest add scroll-area
npx shadcn@latest add sheet

# Forms
npx shadcn@latest add form
npx shadcn@latest add select
npx shadcn@latest add checkbox
npx shadcn@latest add radio-group
npx shadcn@latest add switch
npx shadcn@latest add textarea
npx shadcn@latest add label

# Feedback
npx shadcn@latest add alert
npx shadcn@latest add popover
npx shadcn@latest add tooltip

# Data Display
npx shadcn@latest add table
npx shadcn@latest add pagination
npx shadcn@latest add calendar

# Navigation
npx shadcn@latest add navigation-menu
npx shadcn@latest add breadcrumb
```

---

## 3. Custom Components

### 3.1 Layout Components

#### Navbar
```tsx
interface NavbarProps {
  user?: User | null
  onLogout?: () => void
}

// Features:
// - Logo + Brand
// - Navigation links
// - Search bar
// - User menu (avatar, dropdown)
// - Mobile responsive
```

#### Sidebar
```tsx
interface SidebarProps {
  items: SidebarItem[]
  collapsed?: boolean
  onToggle?: () => void
}

interface SidebarItem {
  icon: LucideIcon
  label: string
  href: string
  badge?: number
  children?: SidebarItem[]
}

// Features:
// - Collapsible
// - Nested items
// - Active state
// - Badge support
```

#### Footer
```tsx
interface FooterProps {
  links: FooterLink[]
  socials?: SocialLink[]
}

// Features:
// - Links organized by category
// - Social media icons
// - Copyright
```

### 3.2 Course Components

#### CourseCard
```tsx
interface CourseCardProps {
  course: Course
  variant?: 'default' | 'compact' | 'horizontal'
  showProgress?: boolean
  showInstructor?: boolean
}

// Features:
// - Thumbnail
// - Title & description
// - Instructor info
// - Rating
// - Progress bar (optional)
// - Hover effects
```

#### CourseProgress
```tsx
interface CourseProgressProps {
  completed: number
  total: number
  showLabel?: boolean
}

// Features:
// - Progress bar
// - Percentage text
// - Customizable size
```

#### LessonItem
```tsx
interface LessonItemProps {
  lesson: Lesson
  isCompleted?: boolean
  isActive?: boolean
  isLocked?: boolean
  onClick?: () => void
}

// Features:
// - Duration
// - Completion status
// - Lock state
// - Active state
```

### 3.3 Learning Components

#### VideoPlayer
```tsx
interface VideoPlayerProps {
  src: string
  poster?: string
  onComplete?: () => void
  onProgress?: (progress: number) => void
}

// Features:
// - Play/Pause
// - Volume control
// - Progress bar
// - Fullscreen
// - Playback speed
// - Subtitles support
```

#### AITutorChat
```tsx
interface AITutorChatProps {
  courseId: string
  lessonId?: string
}

// Features:
// - Chat messages
// - Typing indicator
// - Quick suggestions
// - Code highlighting
// - Minimizable
```

#### NotePanel
```tsx
interface NotePanelProps {
  lessonId: string
  onSave?: (note: string) => void
}

// Features:
// - Rich text editor
// - Auto-save
// - Timestamp
// - Export options
```

### 3.4 Quiz Components

#### QuizPlayer
```tsx
interface QuizPlayerProps {
  quiz: Quiz
  onComplete?: (result: QuizResult) => void
}

// Features:
// - Question display
// - Timer
// - Progress tracking
// - Submit confirmation
```

#### QuestionCard
```tsx
interface QuestionCardProps {
  question: Question
  selectedAnswer?: string
  onAnswer: (answer: string) => void
  showResult?: boolean
}

// Features:
// - Question text
// - Answer options
// - Selection state
// - Result feedback
```

#### QuizResult
```tsx
interface QuizResultProps {
  result: QuizResult
  onRetry?: () => void
  onReview?: () => void
}

// Features:
// - Score display
// - Pass/Fail status
// - Statistics
// - Action buttons
```

### 3.5 Common Components

#### PageLoader
```tsx
// Full-page loading spinner
// Used for route transitions
```

#### EmptyState
```tsx
interface EmptyStateProps {
  icon?: LucideIcon
  title: string
  description?: string
  action?: {
    label: string
    onClick: () => void
  }
}

// Features:
// - Icon
// - Title & description
// - Optional action button
```

#### ErrorMessage
```tsx
interface ErrorMessageProps {
  error: Error | string
  onRetry?: () => void
}

// Features:
// - Error icon
// - Error message
// - Retry button
```

#### StatsCard
```tsx
interface StatsCardProps {
  title: string
  value: string | number
  icon?: LucideIcon
  trend?: {
    value: number
    isPositive: boolean
  }
}

// Features:
// - Title
// - Value
// - Icon
// - Trend indicator
```

---

## 4. Component Guidelines

### 4.1 Props Design

```tsx
// ✅ Good - Flexible and clear
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'destructive' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  isLoading?: boolean
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
  children: React.ReactNode
}

// ❌ Bad - Too many boolean props
interface ButtonProps {
  isPrimary?: boolean
  isSecondary?: boolean
  isLarge?: boolean
  isSmall?: boolean
}
```

### 4.2 Composition

```tsx
// ✅ Good - Composable
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
  </CardHeader>
  <CardContent>Content</CardContent>
  <CardFooter>Actions</CardFooter>
</Card>

// ❌ Bad - Props drilling
<Card title="Title" description="Description" content="Content" />
```

### 4.3 Accessibility

- All interactive elements must have focus states
- Use semantic HTML elements
- Include ARIA labels where needed
- Ensure keyboard navigation works
- Maintain color contrast ratios
