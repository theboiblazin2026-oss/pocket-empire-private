---
name: Fintech
description: Payment processing, KYC/AML, lending regulations
---

# Fintech Skill

## Payment Processing

### Card Flow
```
Customer → Merchant → Payment Gateway → Processor → Card Network → Issuing Bank
```

### Key Players

| Role | Examples |
|------|----------|
| Gateway | Stripe, Square |
| Processor | First Data, TSYS |
| Network | Visa, Mastercard |
| Issuer | Chase, Capital One |

## KYC (Know Your Customer)

Required verification:
1. **Identity** - Name, DOB, SSN
2. **Address** - Proof of residence
3. **Document** - ID/passport photo
4. **Selfie** - Liveness check

## AML (Anti-Money Laundering)

- Transaction monitoring
- Suspicious activity reports (SAR)
- Customer due diligence (CDD)
- Enhanced due diligence (EDD) for high-risk

## Lending Regulations

| Law | Focus |
|-----|-------|
| TILA | Disclosure requirements |
| ECOA | Equal credit access |
| FCRA | Credit reporting |
| Reg Z | APR, payment terms |

## Key Metrics

| Metric | Definition |
|--------|------------|
| TPV | Total Payment Volume |
| Take Rate | Revenue / TPV |
| Chargeback Rate | Must stay < 1% |
| Default Rate | Loans not repaid |

## Security Requirements

- PCI DSS for card data
- Encryption at rest and in transit
- Tokenization
- Fraud detection

## When to Apply
Use when building payment apps, lending platforms, or financial services.
