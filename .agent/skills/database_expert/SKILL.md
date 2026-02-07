---
name: Database Expert
description: SQL optimization, indexing strategies, migrations, and NoSQL patterns
---

# Database Expert Skill

Apply these patterns when working with databases.

## SQL Optimization

### Indexing Rules
| Scenario | Index Type |
|----------|------------|
| Equality lookup (`WHERE id = 5`) | B-tree (default) |
| Range queries (`WHERE date > X`) | B-tree |
| Full-text search | GIN / Full-text |
| JSON fields | GIN |
| Geospatial | GiST / R-tree |

### Index Best Practices
```sql
-- ✅ Good: Index columns used in WHERE, JOIN, ORDER BY
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);

-- ❌ Avoid: Over-indexing (slows writes)
-- ❌ Avoid: Indexing low-cardinality columns (status: 'active'/'inactive')
```

### Query Optimization
```sql
-- ✅ Select only needed columns
SELECT id, name, email FROM users WHERE active = true;

-- ❌ Avoid SELECT *
SELECT * FROM users;

-- ✅ Use EXPLAIN to analyze
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123;
```

## Common Patterns

### Pagination
```sql
-- Offset (simple but slow for large offsets)
SELECT * FROM posts ORDER BY id LIMIT 20 OFFSET 100;

-- Keyset (faster for large datasets)
SELECT * FROM posts WHERE id > 100 ORDER BY id LIMIT 20;
```

### Soft Deletes
```sql
-- Add deleted_at column instead of DELETE
UPDATE users SET deleted_at = NOW() WHERE id = 123;

-- Query active records
SELECT * FROM users WHERE deleted_at IS NULL;
```

### Upsert
```sql
-- PostgreSQL
INSERT INTO users (email, name) VALUES ('a@b.com', 'Alice')
ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name;

-- MySQL
INSERT INTO users (email, name) VALUES ('a@b.com', 'Alice')
ON DUPLICATE KEY UPDATE name = VALUES(name);
```

## Migrations

### Best Practices
- [ ] Use a migration tool (Alembic, Prisma, Knex)
- [ ] Make migrations reversible
- [ ] Test rollback before deploying
- [ ] Avoid data loss operations

### Safe Schema Changes
| Change | Safe? | Notes |
|--------|-------|-------|
| Add column (nullable) | ✅ | Default to NULL |
| Add column (NOT NULL) | ⚠️ | Need default or backfill first |
| Drop column | ⚠️ | Deploy code change first |
| Rename column | ❌ | Use add+migrate+drop |
| Add index | ✅ | Use CONCURRENTLY in Postgres |

## NoSQL (MongoDB) Patterns

### Document Design
```javascript
// Embed when: 1-to-few, always accessed together
{
  _id: ObjectId("..."),
  name: "Order",
  items: [
    { product: "Widget", qty: 2, price: 10.00 }
  ]
}

// Reference when: 1-to-many, independent access
{
  _id: ObjectId("..."),
  name: "Order",
  user_id: ObjectId("...")  // Reference to users collection
}
```

### Indexing in MongoDB
```javascript
db.users.createIndex({ email: 1 }, { unique: true });
db.orders.createIndex({ user_id: 1, created_at: -1 });
```

## Connection Pooling

```python
# ✅ Use connection pools
from sqlalchemy import create_engine
engine = create_engine(
    "postgresql://...",
    pool_size=5,
    max_overflow=10
)
```

## When to Apply
Use when designing schemas, optimizing queries, or planning migrations.
