---
name: API Designer
description: REST API design patterns, OpenAPI specs, error handling, and versioning
---

# API Designer Skill

Apply these patterns when designing or reviewing REST APIs.

## URL Design

### Resource Naming
```
✅ Good:
GET    /users              # List users
GET    /users/123          # Get user 123
POST   /users              # Create user
PATCH  /users/123          # Update user 123
DELETE /users/123          # Delete user 123

GET    /users/123/orders   # User's orders (nested resource)

❌ Avoid:
/getUsers
/user/delete/123
/api/v1/usersList
```

### Query Parameters
```
GET /users?page=2&limit=20           # Pagination
GET /users?sort=created_at:desc      # Sorting
GET /users?status=active&role=admin  # Filtering
GET /users?fields=id,name,email      # Sparse fields
```

## HTTP Methods

| Method | Action | Idempotent? | Body? |
|--------|--------|-------------|-------|
| GET | Read | ✅ | ❌ |
| POST | Create | ❌ | ✅ |
| PUT | Replace | ✅ | ✅ |
| PATCH | Partial Update | ✅ | ✅ |
| DELETE | Remove | ✅ | ❌ |

## Response Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET/PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation error |
| 401 | Unauthorized | Missing/invalid auth |
| 403 | Forbidden | Valid auth, no permission |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate/constraint violation |
| 422 | Unprocessable | Semantic error |
| 429 | Too Many Requests | Rate limited |
| 500 | Server Error | Unexpected failure |

## Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {"field": "email", "issue": "Invalid email format"},
      {"field": "age", "issue": "Must be positive number"}
    ]
  }
}
```

## Pagination

### Offset-based
```json
GET /users?page=2&limit=20

{
  "data": [...],
  "pagination": {
    "page": 2,
    "limit": 20,
    "total": 150,
    "total_pages": 8
  }
}
```

### Cursor-based (for large datasets)
```json
GET /users?cursor=abc123&limit=20

{
  "data": [...],
  "pagination": {
    "next_cursor": "xyz789",
    "has_more": true
  }
}
```

## Versioning

| Strategy | Example | Pros/Cons |
|----------|---------|-----------|
| URL Path | `/v1/users` | Simple, clear |
| Header | `Accept: application/vnd.api+json;version=1` | Clean URLs |
| Query Param | `/users?version=1` | Easy testing |

**Recommendation:** Use URL path (`/v1/`) for simplicity.

## Authentication

### Bearer Token (JWT)
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### API Key
```
X-API-Key: sk_live_abc123
```

## Rate Limiting Headers
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```

## OpenAPI Spec Structure
```yaml
openapi: 3.0.0
info:
  title: My API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      responses:
        '200':
          description: OK
```

## When to Apply
Use when designing new APIs, reviewing API contracts, or debugging API issues.
