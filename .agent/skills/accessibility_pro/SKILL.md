---
name: Accessibility Pro
description: WCAG compliance, ARIA, and inclusive design
---

# Accessibility Pro Skill

## WCAG Principles (POUR)

| Principle | Meaning |
|-----------|---------|
| Perceivable | Can users perceive the content? |
| Operable | Can users navigate and interact? |
| Understandable | Is content clear and predictable? |
| Robust | Does it work with assistive tech? |

## Common Issues & Fixes

### Images
```html
<!-- ❌ Bad -->
<img src="chart.png">

<!-- ✅ Good -->
<img src="chart.png" alt="Sales increased 50% from Q1 to Q2">
```

### Form Labels
```html
<!-- ❌ Bad -->
<input type="email" placeholder="Email">

<!-- ✅ Good -->
<label for="email">Email</label>
<input type="email" id="email">
```

### Color Contrast
- Normal text: 4.5:1 ratio minimum
- Large text: 3:1 ratio minimum
- Tool: WebAIM Contrast Checker

### Keyboard Navigation
- All interactive elements focusable via Tab
- Visible focus indicator
- Logical tab order

## ARIA Basics

```html
<!-- Landmark roles -->
<nav role="navigation">
<main role="main">

<!-- State -->
<button aria-expanded="false">Menu</button>

<!-- Live regions -->
<div aria-live="polite">Updated content here</div>

<!-- Labels -->
<button aria-label="Close dialog">×</button>
```

## Checklist

- [ ] All images have alt text
- [ ] Form fields have labels
- [ ] Color contrast meets WCAG AA
- [ ] Keyboard navigation works
- [ ] Skip link to main content
- [ ] Focus states visible
- [ ] No content relies on color alone
- [ ] Video has captions

## Testing Tools

- axe DevTools (browser extension)
- WAVE (wave.webaim.org)
- Lighthouse (Chrome DevTools)
- Screen reader (VoiceOver, NVDA)

## When to Apply
Use when building accessible websites, auditing for compliance, or fixing a11y issues.
