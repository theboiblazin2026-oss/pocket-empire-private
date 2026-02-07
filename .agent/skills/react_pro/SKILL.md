---
name: React Pro
description: Modern React best practices including Hooks, TypeScript, Tailwind CSS, and performance optimization
---

# React Pro Skill

Apply these patterns when building or reviewing React code.

## Component Design

### Functional Components Only
```tsx
// ✅ Good
const Button = ({ onClick, children }: ButtonProps) => (
  <button onClick={onClick}>{children}</button>
);

// ❌ Avoid class components
```

### Props Interface Pattern
```tsx
interface CardProps {
  title: string;
  children: React.ReactNode;
  variant?: 'default' | 'outlined';
}

const Card = ({ title, children, variant = 'default' }: CardProps) => { ... }
```

## Hooks Best Practices

### useState
- Keep state minimal and derived values computed
- Use functional updates for state that depends on previous value
```tsx
setCount(prev => prev + 1)  // ✅
setCount(count + 1)         // ❌ stale closure risk
```

### useEffect
- Always specify dependencies
- Clean up subscriptions/timers
- Avoid object/array literals in deps (use useMemo)
```tsx
useEffect(() => {
  const subscription = subscribe();
  return () => subscription.unsubscribe();
}, [dependency]);
```

### useMemo / useCallback
- Use for expensive calculations or stable references
- Don't over-optimize — profile first
```tsx
const expensiveValue = useMemo(() => computeExpensive(data), [data]);
const handleClick = useCallback(() => doSomething(id), [id]);
```

### Custom Hooks
- Extract reusable logic into `use*` functions
- Return tuple for simple state: `[value, setValue]`
- Return object for complex state: `{ data, loading, error }`

## State Management

| Scope | Solution |
|-------|----------|
| Component-local | useState |
| Shared (2-3 components) | Lift state up |
| App-wide (simple) | Context + useReducer |
| App-wide (complex) | Zustand or Redux Toolkit |

## Performance

### Avoid Unnecessary Re-renders
- Memoize expensive children with `React.memo()`
- Use `useMemo` for computed values
- Split context by update frequency

### Code Splitting
```tsx
const HeavyComponent = React.lazy(() => import('./HeavyComponent'));

<Suspense fallback={<Spinner />}>
  <HeavyComponent />
</Suspense>
```

## Tailwind CSS Patterns

### Responsive Design
```tsx
<div className="p-4 md:p-8 lg:p-12">...</div>
```

### Dark Mode
```tsx
<div className="bg-white dark:bg-gray-900">...</div>
```

### Conditional Classes
```tsx
<button className={`btn ${isActive ? 'bg-blue-500' : 'bg-gray-500'}`}>
```

### Common Utility Groups
| Purpose | Classes |
|---------|---------|
| Centering | `flex items-center justify-center` |
| Card | `rounded-lg shadow-md p-6 bg-white` |
| Transition | `transition-all duration-200 ease-in-out` |

## File Structure
```
src/
├── components/     # Reusable UI components
├── hooks/          # Custom hooks
├── pages/          # Route-level components
├── utils/          # Helper functions
├── types/          # TypeScript interfaces
└── context/        # React contexts
```

## When to Apply This Skill
Use when:
- Building new React components
- Reviewing React code for improvements
- Debugging performance issues
- Setting up new React projects
