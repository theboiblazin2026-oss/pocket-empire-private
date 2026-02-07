---
name: SaaS
description: Pricing models, churn, MRR/ARR, feature flags
---

# SaaS Skill

## Pricing Models

| Model | Description |
|-------|-------------|
| Flat-rate | One price for all |
| Per-seat | Per user pricing |
| Usage-based | Pay for what you use |
| Freemium | Free tier + paid upgrades |
| Tiered | Good/Better/Best |

## Key Metrics

| Metric | Formula |
|--------|---------|
| MRR | Monthly Recurring Revenue |
| ARR | MRR × 12 |
| Churn Rate | Lost Customers / Total Customers |
| Net Revenue Retention | (MRR - Churn + Expansion) / Starting MRR |
| LTV | ARPU × (1 / Churn Rate) |
| CAC | Sales + Marketing / New Customers |
| LTV:CAC | Should be > 3:1 |

## Churn Reduction

| Tactic | Implementation |
|--------|----------------|
| Onboarding | First 7 days critical |
| Engagement | Track feature usage |
| Success | Customer check-ins |
| Win-back | Target churned users |

## Feature Flags

```javascript
if (featureFlags.isEnabled('new_dashboard', userId)) {
  showNewDashboard();
} else {
  showOldDashboard();
}
```

**Use for:**
- Gradual rollouts
- A/B testing
- Kill switches
- Beta features

## Growth Levers

1. Acquisition (more users)
2. Activation (faster time-to-value)
3. Retention (reduce churn)
4. Revenue (upsell/expansion)
5. Referral (viral growth)

## When to Apply
Use when building SaaS products, optimizing pricing, or reducing churn.
