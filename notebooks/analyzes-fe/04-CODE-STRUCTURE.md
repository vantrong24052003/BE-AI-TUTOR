# FE AI TUTOR - Code Structure

> Cấu trúc code và conventions

---

## 1. FOLDER STRUCTURE

```
src/
├── app/                    # App-level
│   ├── router/            # Routing config
│   └── providers/         # Context providers
│
├── components/            # Shared components
│   ├── ui/               # shadcn/ui
│   ├── layout/           # Navbar, Sidebar, Footer
│   └── common/           # PageLoader, EmptyState, etc.
│
├── features/             # Feature modules
│   ├── auth/
│   ├── courses/
│   ├── learning/
│   ├── quiz/
│   ├── ai-tutor/
│   └── profile/
│
├── pages/                # Page components
│   ├── public/
│   ├── auth/
│   └── app/
│
├── hooks/                # Global hooks
├── lib/                  # Utilities
├── services/             # API config
├── stores/               # Zustand stores
├── types/                # Global types
└── test/                 # Test utilities
```

---

## 2. FEATURE MODULE STRUCTURE

```
features/[feature]/
├── components/           # Feature components
│   ├── ComponentA.tsx
│   └── ComponentA.test.tsx
├── hooks/               # Feature hooks
│   └── useFeature.ts
├── api/                 # Feature API calls
│   └── featureApi.ts
├── types.ts             # Feature types
└── index.ts             # Barrel export
```

---

## 3. NAMING CONVENTIONS

| Loại | Convention | Ví dụ |
|------|------------|-------|
| Component file | PascalCase.tsx | `CourseCard.tsx` |
| Hook file | camelCase.ts | `useCourse.ts` |
| API file | camelCase.ts | `courseApi.ts` |
| Type file | types.ts | `types.ts` |
| Test file | *.test.tsx | `CourseCard.test.tsx` |
| Feature folder | kebab-case | `ai-tutor/` |

---

## 4. COMPONENT TEMPLATE

```tsx
// components/common/Example.tsx
import { cn } from '@/lib/utils'

interface ExampleProps {
  title: string
  className?: string
}

export function Example({ title, className }: ExampleProps) {
  return (
    <div className={cn('base-class', className)}>
      {title}
    </div>
  )
}
```

---

## 5. HOOK TEMPLATE

```tsx
// features/courses/hooks/useCourse.ts
import { useQuery } from '@tanstack/react-query'
import { courseApi } from '../api/courseApi'

export function useCourse(courseId: string) {
  return useQuery({
    queryKey: ['course', courseId],
    queryFn: () => courseApi.getById(courseId),
    enabled: !!courseId,
  })
}
```

---

## 6. STATE MANAGEMENT

| State Type | Tool | Location |
|------------|------|----------|
| Server data | React Query | Feature hooks |
| Auth state | Zustand | `stores/auth.store.ts` |
| UI state | Zustand | `stores/ui.store.ts` |
| Form state | React Hook Form | Component |

---

## 7. CHECKLIST BEFORE COMMIT

- [ ] File đúng vị trí
- [ ] Named export (không default)
- [ ] Types defined
- [ ] No `any` type
- [ ] ESLint pass
- [ ] Prettier pass
- [ ] Tests pass

---

*Version: 1.0 - Updated: 2026-02-27*
