---
name: Next.js
description: SSR, SSG, API routes, App Router, Vercel deployment
---

# Next.js Skill

## App Router (Next.js 13+)

```
app/
├── layout.tsx        # Root layout
├── page.tsx          # Home page (/)
├── about/
│   └── page.tsx      # /about
├── blog/
│   ├── page.tsx      # /blog
│   └── [slug]/
│       └── page.tsx  # /blog/:slug
└── api/
    └── users/
        └── route.ts  # API: /api/users
```

## Server Components (Default)

```tsx
// This runs on server by default
export default async function Page() {
  const data = await fetch('https://api.example.com/data');
  const json = await data.json();
  
  return <div>{json.title}</div>;
}
```

## Client Components

```tsx
'use client';

import { useState } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

## API Routes

```tsx
// app/api/users/route.ts
import { NextResponse } from 'next/server';

export async function GET() {
  const users = await db.users.findAll();
  return NextResponse.json(users);
}

export async function POST(request: Request) {
  const body = await request.json();
  const user = await db.users.create(body);
  return NextResponse.json(user, { status: 201 });
}
```

## When to Apply
Use when building React apps with SSR/SSG needs or full-stack Next.js applications.
