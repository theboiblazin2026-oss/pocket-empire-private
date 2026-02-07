---
name: Node.js Expert
description: Express, middleware, streams, performance, and best practices
---

# Node.js Expert Skill

## Express Patterns

```javascript
const express = require('express');
const app = express();

// Middleware
app.use(express.json());
app.use(cors());

// Route
app.get('/users/:id', async (req, res, next) => {
  try {
    const user = await db.users.findById(req.params.id);
    if (!user) return res.status(404).json({ error: 'Not found' });
    res.json(user);
  } catch (err) {
    next(err);
  }
});

// Error handler (must be last)
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ error: 'Internal error' });
});
```

## Middleware Pattern

```javascript
const authMiddleware = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'Unauthorized' });
  
  try {
    req.user = jwt.verify(token, SECRET);
    next();
  } catch {
    res.status(401).json({ error: 'Invalid token' });
  }
};

app.use('/api', authMiddleware);
```

## Streams

```javascript
const fs = require('fs');
const { pipeline } = require('stream/promises');

// File copy with streams
await pipeline(
  fs.createReadStream('input.txt'),
  zlib.createGzip(),
  fs.createWriteStream('output.txt.gz')
);

// Stream to response
app.get('/download', (req, res) => {
  res.setHeader('Content-Type', 'application/octet-stream');
  fs.createReadStream('file.pdf').pipe(res);
});
```

## Performance Tips

| Tip | Implementation |
|-----|----------------|
| Use clustering | `cluster.fork()` for each CPU |
| Cache responses | Redis, in-memory |
| Compress responses | `compression` middleware |
| Connection pooling | Database pools |
| Async all I/O | Never block event loop |

## Environment Config

```javascript
require('dotenv').config();

const config = {
  port: process.env.PORT || 3000,
  db: process.env.DATABASE_URL,
  nodeEnv: process.env.NODE_ENV || 'development',
};
```

## When to Apply
Use when building Node.js APIs, debugging performance, or designing middleware.
