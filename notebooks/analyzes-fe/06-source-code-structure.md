# AI TUTOR - Source Code Structure Guide

## Quick Reference

### Folder Structure

```
src/
├── app/           # App config, router, providers
├── components/    # Shared components (ui, layout, common)
├── features/      # Feature modules (auth, courses, learning, etc.)
├── pages/         # Page components (route-level)
├── hooks/         # Global custom hooks
├── lib/           # Utilities
├── services/      # Base services (axios config)
├── stores/        # Global state (Zustand)
├── types/         # Global TypeScript types
├── test/          # Test utilities & mocks
├── assets/        # Static assets
└── styles/        # Global styles
```

### Feature Module Structure

```
features/[feature]/
├── components/    # Feature-specific components
├── hooks/         # Feature-specific hooks
├── api/           # Feature-specific API calls
├── types.ts       # Feature types
├── schemas.ts     # Zod schemas (optional)
├── constants.ts   # Feature constants (optional)
└── index.ts       # Public API (barrel export)
```

---

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Component file | PascalCase.tsx | `CourseCard.tsx` |
| Hook file | camelCase.ts | `useCourse.ts` |
| API file | camelCase.ts | `courseApi.ts` |
| Type file | types.ts or *.types.ts | `types.ts` |
| Store file | *.store.ts | `auth.store.ts` |
| Test file | *.test.tsx | `CourseCard.test.tsx` |
| Feature folder | kebab-case | `ai-tutor/` |

---

## Import/Export Rules

### Exports
```tsx
// ✅ Named export for components
export function CourseCard() {}

// ✅ Barrel export in index.ts
export { CourseCard } from './components/CourseCard'
export { useCourse } from './hooks/useCourse'
export type { Course } from './types'
```

### Imports
```tsx
// ✅ Barrel import
import { Button, Card } from '@/components/ui'

// ✅ Feature import
import { CourseCard, useCourse } from '@/features/courses'

// ❌ Avoid deep imports
import { CourseCard } from '@/features/courses/components/CourseCard'
```

---

## Component Template

```tsx
// 1. Imports
import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
import type { Course } from '../types'

// 2. Types
interface CourseCardProps {
  course: Course
  className?: string
}

// 3. Component
export function CourseCard({ course, className }: CourseCardProps) {
  // Hooks
  const [isOpen, setIsOpen] = useState(false)

  // Derived state
  const progress = Math.round(course.progress || 0)

  // Early returns
  if (!course) return null

  // Handlers
  const handleClick = () => setIsOpen(!isOpen)

  // Render
  return (
    <div className={cn('p-4', className)}>
      <h3>{course.title}</h3>
      <Button onClick={handleClick}>Click</Button>
    </div>
  )
}
```

---

## State Management

| State Type | Tool | Location |
|------------|------|----------|
| Server data | React Query | Feature hooks |
| Auth state | Zustand | `stores/auth.store.ts` |
| UI state | Zustand | `stores/ui.store.ts` |
| Form state | React Hook Form | Component |
| Local state | useState | Component |

---

## Folder Decision

```
Component dùng ở:
- 1 feature  → features/[feature]/components/
- 2 features → features/[main]/components/ + import
- 3+ features → components/

Hook dùng ở:
- 1 feature  → features/[feature]/hooks/
- 2+ features → hooks/

Type dùng ở:
- 1 feature  → features/[feature]/types.ts
- 2+ features → types/
```

---

## Checklist Before Commit

- [ ] File in correct location
- [ ] Named export (not default)
- [ ] Types defined
- [ ] No `any` type
- [ ] Import from barrel when possible
- [ ] Props interface defined
- [ ] Tests written
- [ ] ESLint & Prettier pass
