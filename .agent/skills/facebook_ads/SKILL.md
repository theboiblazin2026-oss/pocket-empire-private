---
name: Facebook Ads
description: Audiences, pixels, lookalikes, creative best practices
---

# Facebook Ads Skill

## Campaign Structure

```
Campaign (Objective)
└── Ad Set (Targeting, Budget)
    └── Ad (Creative)
```

## Objectives

| Objective | Use Case |
|-----------|----------|
| Awareness | Brand reach |
| Traffic | Website visits |
| Engagement | Likes, comments |
| Leads | Form submissions |
| Conversions | Purchases |

## Audience Types

### Core Audiences
- Demographics (age, gender, location)
- Interests
- Behaviors

### Custom Audiences
- Website visitors (pixel)
- Customer list upload
- App users
- Video viewers

### Lookalike Audiences
- Similar to your best customers
- 1% = most similar, 10% = broader reach

## Facebook Pixel

```html
<!-- Base code in <head> -->
<script>
  fbq('init', 'YOUR_PIXEL_ID');
  fbq('track', 'PageView');
</script>

<!-- Event tracking -->
<script>
  fbq('track', 'Purchase', {value: 99.99, currency: 'USD'});
</script>
```

## Creative Best Practices

- First 3 seconds grab attention
- Mobile-first (9:16 or 1:1)
- Clear CTA
- Test multiple creatives
- Refresh every 2-4 weeks

## When to Apply
Use when running Facebook/Instagram ads or building audiences.
