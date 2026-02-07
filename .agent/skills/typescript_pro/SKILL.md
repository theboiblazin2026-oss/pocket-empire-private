---
name: TypeScript Pro
description: Advanced types, generics, utility types, and best practices
---

# TypeScript Pro Skill

## Utility Types

```typescript
// Partial - all properties optional
type PartialUser = Partial<User>;

// Required - all properties required
type RequiredUser = Required<User>;

// Pick - select properties
type UserName = Pick<User, 'name' | 'email'>;

// Omit - exclude properties
type UserWithoutId = Omit<User, 'id'>;

// Record - key-value mapping
type UserRoles = Record<string, Role>;

// ReturnType - extract return type
type FnReturn = ReturnType<typeof myFunction>;
```

## Generics

```typescript
// Generic function
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}

// Generic interface
interface Response<T> {
  data: T;
  error?: string;
}

// Generic constraint
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

## Type Guards

```typescript
// typeof guard
function process(value: string | number) {
  if (typeof value === 'string') {
    return value.toUpperCase();
  }
  return value * 2;
}

// Custom type guard
function isUser(obj: unknown): obj is User {
  return typeof obj === 'object' && obj !== null && 'name' in obj;
}
```

## Advanced Patterns

```typescript
// Discriminated union
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: string };

// Template literal types
type Event = `on${Capitalize<string>}`;

// Mapped types
type Readonly<T> = {
  readonly [K in keyof T]: T[K];
};
```

## Config

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUnusedLocals": true,
    "esModuleInterop": true
  }
}
```

## When to Apply
Use when writing TypeScript, defining types, or reviewing type safety.
