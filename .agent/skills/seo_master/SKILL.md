---
name: SEO Master
description: On-page SEO, technical SEO, and content optimization
---

# SEO Master Skill

## On-Page SEO Checklist

### Title Tag
- Include primary keyword near beginning
- Length: 50-60 characters
- Format: `Primary Keyword - Secondary | Brand`

### Meta Description
- Include keyword naturally
- Length: 150-160 characters
- Include call-to-action

### Headings
- One H1 per page (include keyword)
- H2-H6 for subheadings (include variations)
- Logical hierarchy

### Content
- Keyword in first 100 words
- Natural keyword density (1-2%)
- Include related terms (LSI keywords)
- Minimum 300 words (1500+ for in-depth)

## Technical SEO

### Site Speed
```html
<!-- Preload critical resources -->
<link rel="preload" href="font.woff2" as="font">
<link rel="preconnect" href="https://api.example.com">
```

### Mobile-Friendly
- Viewport meta tag
- Responsive images
- Touch-friendly buttons (44x44px min)

### Structured Data
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Your Title Here",
  "author": {"@type": "Person", "name": "Author Name"},
  "datePublished": "2024-01-15"
}
```

### Robots.txt
```
User-agent: *
Disallow: /admin/
Disallow: /private/
Sitemap: https://example.com/sitemap.xml
```

## Link Building

| Type | Quality | Effort |
|------|---------|--------|
| Editorial links | High | High |
| Guest posts | Medium | Medium |
| Directories | Low | Low |
| Broken link building | High | Medium |

## Core Web Vitals

| Metric | Good | Needs Work |
|--------|------|------------|
| LCP (Largest Contentful Paint) | < 2.5s | > 4s |
| FID (First Input Delay) | < 100ms | > 300ms |
| CLS (Cumulative Layout Shift) | < 0.1 | > 0.25 |

## When to Apply
Use when optimizing pages, auditing sites, or creating content strategies.
