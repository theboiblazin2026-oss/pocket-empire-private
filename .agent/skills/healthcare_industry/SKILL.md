---
name: Healthcare Industry
description: HIPAA, HL7, FHIR, EHR integration
---

# Healthcare Industry Skill

## Key Regulations

| Regulation | Focus |
|------------|-------|
| HIPAA | Patient privacy |
| HITECH | EHR adoption |
| 21st Century Cures | Interoperability |
| FDA | Device/drug approval |

## Data Standards

### HL7 v2 (Legacy)
Pipe-delimited messages:
```
MSH|^~\&|SENDER|HOSPITAL|RECEIVER|...
PID|||12345^^^MRN||DOE^JOHN||19800101|M
```

### FHIR (Modern)
JSON-based RESTful API:
```json
{
  "resourceType": "Patient",
  "id": "12345",
  "name": [{"family": "Doe", "given": ["John"]}],
  "birthDate": "1980-01-01"
}
```

## FHIR Resources

| Resource | Purpose |
|----------|---------|
| Patient | Demographics |
| Observation | Lab results, vitals |
| Medication | Prescriptions |
| Encounter | Visits |
| Condition | Diagnoses |

## EHR Integration Patterns

- **SMART on FHIR**: Launch apps in EHR context
- **Bulk Data**: Large dataset exports
- **Subscriptions**: Real-time notifications

## Common Challenges

- Complex consent management
- Data matching across systems
- Terminology mapping
- Legacy system integration
- Audit trail requirements

## When to Apply
Use when building healthcare apps, integrating with EHRs, or handling PHI.
