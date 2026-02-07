---
name: Deploy Master
description: Zero-downtime deployment strategies, CI/CD pipelines, and rollback procedures
---

# Deploy Master Skill

Use this checklist and knowledge for safe, reliable deployments.

## Pre-Deploy Checklist

### Code Quality
- [ ] All tests passing (`npm test`)
- [ ] Linting clean (`npm run lint`)
- [ ] TypeScript compiles (`npm run build`)
- [ ] No console.log/debugger statements in production code

### Environment
- [ ] Environment variables documented and set
- [ ] Secrets not committed to repo
- [ ] Database migrations ready (if applicable)
- [ ] API version compatibility checked

### Version Control
- [ ] Changes committed to feature branch
- [ ] PR reviewed and approved
- [ ] Conflicts resolved
- [ ] Version bumped (if applicable)

## Deployment Strategies

### 1. Direct Deploy (Simple)
```
main branch → Build → Deploy
```
- **Use when:** Small apps, minimal traffic
- **Risk:** Downtime during deploy

### 2. Blue-Green Deployment
```
[Blue: Current] ←── Load Balancer ──→ [Green: New]
                    (switch when ready)
```
- **Use when:** Zero downtime required
- **Benefit:** Instant rollback (point back to Blue)

### 3. Canary Deployment
```
Traffic: 95% → Current Version
         5% → New Version (monitor, then increase)
```
- **Use when:** Testing in production with real traffic
- **Benefit:** Catch issues before full rollout

### 4. Rolling Deployment
```
Server 1: Update → Server 2: Update → Server 3: Update
          (one at a time)
```
- **Use when:** Multiple servers, gradual rollout
- **Benefit:** Partial rollback possible

## CI/CD Platforms

### GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm test
      - run: npm run build
      - run: npx vercel --prod --token=${{ secrets.VERCEL_TOKEN }}
```

### Vercel
- Auto-deploys on push to main
- Preview deployments on PRs
- Rollback via dashboard or CLI: `vercel rollback`

### Firebase
```bash
firebase deploy --only hosting
firebase hosting:rollback  # Revert to previous
```

## Rollback Procedures

### Immediate Rollback Checklist
1. **Identify the issue** (error logs, monitoring alerts)
2. **Revert to previous version**
   - Vercel: Dashboard → Deployments → Promote previous
   - Firebase: `firebase hosting:rollback`
   - Git: `git revert HEAD && git push`
3. **Notify team** (Slack/Discord alert)
4. **Post-mortem** (document what went wrong)

### Database Rollback
- Always have a backup before migrations
- Use reversible migrations when possible
- Test rollback in staging first

## Post-Deploy Monitoring

### Health Checks
- `/health` endpoint returning 200
- Response time < 500ms
- No spike in error rates

### Tools
| Tool | Purpose |
|------|---------|
| Sentry | Error tracking, stack traces |
| Vercel Analytics | Performance, Web Vitals |
| UptimeRobot | Uptime monitoring |
| LogRocket | Session replay |

### Alert Thresholds
- Error rate > 1% → Warning
- Error rate > 5% → Critical
- Response time > 2s → Warning
- Uptime < 99.9% → Investigate

## Secrets Management

### Local Development
```bash
# .env.local (gitignored)
DATABASE_URL=postgres://...
API_KEY=sk_live_...
```

### Production
- Use platform secrets (Vercel, GitHub, AWS)
- Never hardcode in source
- Rotate keys periodically

## When to Apply This Skill
Use when:
- Deploying to production/staging
- Setting up CI/CD pipelines
- Something breaks after deploy
- Reviewing deployment procedures
