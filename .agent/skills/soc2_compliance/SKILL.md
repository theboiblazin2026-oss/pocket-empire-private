---
name: SOC2 Compliance
description: Security controls, audit preparation, and trust service criteria
---

# SOC2 Compliance Skill

## Trust Service Criteria

| Criteria | Focus |
|----------|-------|
| Security | Protection against unauthorized access |
| Availability | System operational when needed |
| Processing Integrity | Complete, accurate processing |
| Confidentiality | Restricted information protection |
| Privacy | Personal information handling |

**Most audits focus on Security (required) + 1-2 others.**

## Key Controls

### Access Control
- [ ] Unique user IDs
- [ ] Role-based access
- [ ] MFA for all users
- [ ] Access reviews (quarterly)
- [ ] Offboarding within 24 hours

### Change Management
- [ ] All changes through version control
- [ ] Code review required
- [ ] Separate dev/staging/prod
- [ ] Change approval process
- [ ] Rollback procedures

### Monitoring & Logging
- [ ] Centralized logging
- [ ] Log retention (1 year+)
- [ ] Alerting on anomalies
- [ ] Incident response plan
- [ ] Regular log reviews

### Vendor Management
- [ ] Vendor inventory
- [ ] Security assessments
- [ ] Contract requirements
- [ ] Annual reviews

## Evidence Collection

| Control | Evidence |
|---------|----------|
| Access control | User list, access reviews |
| MFA | Configuration screenshots |
| Code review | PR history, approval records |
| Backups | Backup logs, restore tests |
| Training | Completion records |

## Type I vs Type II

| Type | Duration | Tests |
|------|----------|-------|
| Type I | Point in time | Design only |
| Type II | 6-12 months | Design + operating effectiveness |

**Type II is more valuable and expected by enterprises.**

## Common Gaps

- Missing access reviews
- No formal incident response plan
- Incomplete vendor assessments
- Undocumented policies
- No security training records

## When to Apply
Use when preparing for SOC2 audit, implementing controls, or gap assessments.
