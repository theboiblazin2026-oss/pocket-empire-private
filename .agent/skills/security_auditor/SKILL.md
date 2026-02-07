---
name: Security Auditor
description: OWASP top 10, authentication patterns, and secrets management
---

# Security Auditor Skill

Apply these security checks when reviewing code or designing systems.

## OWASP Top 10 (2021)

| # | Vulnerability | Prevention |
|---|---------------|------------|
| 1 | Broken Access Control | Verify permissions on every request |
| 2 | Cryptographic Failures | Use TLS, hash passwords with bcrypt |
| 3 | Injection | Parameterized queries, input validation |
| 4 | Insecure Design | Threat modeling, secure defaults |
| 5 | Security Misconfiguration | Disable debug, update dependencies |
| 6 | Vulnerable Components | Regular dependency audits |
| 7 | Auth Failures | MFA, rate limiting, secure sessions |
| 8 | Data Integrity Failures | Verify signatures, use CSP |
| 9 | Logging Failures | Log security events, monitor alerts |
| 10 | SSRF | Allowlist URLs, validate redirects |

## SQL Injection Prevention

```python
# ❌ VULNERABLE
query = f"SELECT * FROM users WHERE id = {user_input}"

# ✅ SAFE (parameterized)
cursor.execute("SELECT * FROM users WHERE id = %s", (user_input,))

# ✅ SAFE (ORM)
User.query.filter_by(id=user_input).first()
```

## XSS Prevention

```javascript
// ❌ VULNERABLE
element.innerHTML = userInput;

// ✅ SAFE
element.textContent = userInput;  // Automatically escaped

// React is safe by default (escapes in JSX)
<div>{userInput}</div>  // ✅
```

## Authentication Best Practices

### Password Storage
```python
import bcrypt

# Hash on signup
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Verify on login
bcrypt.checkpw(password.encode(), stored_hash)
```

### Session Management
- Use secure, httpOnly, sameSite cookies
- Regenerate session ID after login
- Set reasonable expiration (15-30 min for sensitive apps)

### JWT Security
```python
# ✅ Required claims
{
  "sub": "user_id",
  "exp": 1700000000,  # Expiration
  "iat": 1699999000,  # Issued at
  "aud": "your-app"   # Audience
}

# ✅ Use short expiration (15 min) + refresh tokens
# ❌ Don't store sensitive data in JWT payload
```

## Secrets Management

### Never Commit Secrets
```bash
# .gitignore
.env
*.pem
secrets.json
```

### Environment Variables
```python
import os
API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not set")
```

### Secret Rotation
- API keys: Rotate every 90 days
- Passwords: On security events
- SSL certs: Before expiration

## Rate Limiting

```python
from flask_limiter import Limiter

limiter = Limiter(app, default_limits=["100 per minute"])

@app.route("/login")
@limiter.limit("5 per minute")  # Prevent brute force
def login():
    ...
```

## Security Headers

```
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

## Dependency Auditing

```bash
# Python
pip-audit

# Node.js
npm audit

# General
snyk test
```

## Code Review Checklist

- [ ] Input validation on all user data
- [ ] Parameterized queries (no string concatenation)
- [ ] Auth check on every protected endpoint
- [ ] Secrets not hardcoded
- [ ] Error messages don't leak sensitive info
- [ ] HTTPS enforced
- [ ] Dependencies up to date

## When to Apply
Use when reviewing code for security, designing auth systems, or auditing applications.
