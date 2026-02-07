---
name: React Pro
description: Standards and patterns for building high-performance, maintainable React applications.
---

# React Professional Standards

Use these patterns when writing React code for the user's projects.

## Core Principles
1. **Functional Components**: Always use FCs with Hooks. No Class components.
2. **TypeScript**: Default to strict TypeScript for type safety.
3. **Tailwind CSS**: Use Tailwind for all styling. No external CSS files unless necessary.

## State Management
- **Local State**: Use `useState` for simple component state.
- **Complex State**: Use `useReducer` or Context API for feature-level state.
- **Server State**: Use `TanStack Query` (React Query) for API data fetching/caching.
- **Global State**: Minimal usage (Zustand or Redux compatibility if requested), but prefer Context.

## Performance Optimization
- **Memoization**: Use `useMemo` for expensive calculations and `useCallback` for stable function references passed to children.
- **Code Splitting**: Use `React.lazy` and `Suspense` for route-based splitting.
- **Virtualization**: Use `react-window` or `tanstack/virtual` for long lists (crucial for Dispatch logs).

## Component Structure
```tsx
import { useState } from 'react';
import { type ComponentProps } from '@/types';

export const MyComponent = ({ prop1, prop2 }: ComponentProps) => {
  // 1. Hooks
  const [value, setValue] = useState(0);

  // 2. Derived State
  const isEnabled = prop1 && value > 0;

  // 3. Handlers
  const handleClick = () => setValue(v => v + 1);

  // 4. Render
  return (
    <div className="flex flex-col p-4 bg-white shadow-md rounded-lg">
      <h2 className="text-xl font-bold">{prop1}</h2>
      <button 
        onClick={handleClick}
        className="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
      >
        Click me
      </button>
    </div>
  );
};
```
