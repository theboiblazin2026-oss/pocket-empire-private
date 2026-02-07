---
name: HIPAA Compliance
description: Healthcare data rules, BAAs, and breach protocols
---

# HIPAA Compliance Skill

## Protected Health Information (PHI)

PHI includes any health data that can identify an individual:

| PHI Elements |
|--------------|
| Name, address, SSN, DOB |
| Medical record numbers |
| Health conditions/diagnoses |
| Treatment information |
| Billing information |
| Photos, biometrics |

## Key Rules

### Privacy Rule
- Who can access PHI
- Patient rights (access, amend, accounting)
- Minimum necessary standard

### Security Rule
- Administrative safeguards (policies, training)
- Physical safeguards (facility access)
- Technical safeguards (encryption, access controls)

### Breach Notification Rule
- Notify individuals within 60 days
- Notify HHS (portal.hhs.gov)
- If 500+: Notify media

## Business Associate Agreement (BAA)

Required when third parties handle PHI:

| Must Include |
|--------------|
| Permitted uses of PHI |
| Safeguards required |
| Breach notification process |
| Return/destroy PHI terms |
| Subcontractor requirements |

## Technical Requirements

| Requirement | Implementation |
|-------------|----------------|
| Encryption at rest | AES-256 |
| Encryption in transit | TLS 1.2+ |
| Access controls | Role-based, MFA |
| Audit logs | All PHI access |
| Backup | Regular, tested |

## Common Violations

- Unencrypted laptops/drives
- Unauthorized access by employees
- Improper disposal of records
- Missing BAAs
- Insufficient access controls

## Penalties

| Tier | Fine per Violation |
|------|-------------------|
| Unknowing | $100 - $50,000 |
| Reasonable cause | $1,000 - $50,000 |
| Willful neglect (corrected) | $10,000 - $50,000 |
| Willful neglect (not corrected) | $50,000+ |

## When to Apply
Use when building healthcare apps, handling PHI, or ensuring HIPAA compliance.
