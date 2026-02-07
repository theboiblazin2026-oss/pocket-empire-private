---
name: Deploy Master
description: Strategies for secure, zero-downtime deployment and CI/CD pipelines.
---

# Deployment Master

Follow these guidelines for deploying the user's applications (Firebase, Cloud Run, Vercel).

## Deployment Checklist

### Pre-Flight Check
- [ ] **Linting**: Run `npm run lint` - ensure zero errors.
- [ ] **Build**: Run `npm run build` - verify production assets generate correctly.
- [ ] **Tests**: Run `npm test` - ensure critical paths pass.
- [ ] **Environment**: Verify `.env.production` variables are set in the dashboard (NOT in the repo).

### Firebase Hosting (Frontend)
1. **Configure**: `firebase.json` must map rewrites to `index.html` for SPAs.
   ```json
   "rewrites": [ { "source": "**", "destination": "/index.html" } ]
   ```
2. **Deploy**: `firebase deploy --only hosting`
3. **Verify**: Check the provided URL immediately on mobile and desktop.

### Cloud Run (Backend Containers)
1. **Dockerfile Optimization**:
   - Use multi-stage builds to keep image size small.
   - Use `node:alpine` or `distroless` images for production.
2. **Command**:
   ```bash
   gcloud run deploy [SERVICE_NAME] --source . --region us-central1 --allow-unauthenticated
   ```

### CI/CD Pipeline (GitHub Actions)
- Always trigger deployments on `push` to `main` branch.
- Use `actions/checkout@v3` and `auth/dependency-review-action`.
- Store secrets (API Keys) in GitHub repository secrets, never in code.

## Rollback Strategy
- **Firebase**: `firebase hosting:channel:deploy` creates preview channels.
- **Cloud Run**: Use "Manage Traffic" to split traffic or revert to previous revision instantly.
