---
name: No-Code Automation
description: n8n, Zapier, and Make workflows for business automation
---

# No-Code Automation Skill

## Platform Comparison

| Platform | Cost | Best For |
|----------|------|----------|
| Zapier | $20+/mo | Simplest, most integrations |
| Make | $9+/mo | Visual, powerful |
| n8n | Free (self-host) | Developer-friendly, no limits |

## Common Automation Recipes

### Lead Capture
```
New form submission (Typeform)
    ↓
Add to CRM (HubSpot)
    ↓
Send email sequence (Mailchimp)
    ↓
Notify on Slack
```

### Invoice Automation
```
Invoice paid (Stripe)
    ↓
Update Google Sheet
    ↓
Send thank you email
    ↓
Add to accounting (QuickBooks)
```

### Social Media
```
New blog post (WordPress)
    ↓
Create tweet (Twitter)
    ↓
Create LinkedIn post
    ↓
Schedule reminder for engagement
```

## n8n Self-Hosting

```bash
docker run -it --rm \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

## Key Concepts

### Triggers
- Webhook (instant)
- Schedule (cron)
- New record (polling)
- App event

### Actions
- Create/update record
- Send email/message
- HTTP request
- Transform data

### Filters & Logic
- If/then branches
- Filters (only proceed if...)
- Loops
- Error handling

## Best Practices

- Start simple, add complexity
- Test with real data
- Add error notifications
- Document your workflows
- Version control (n8n exports)

## When to Apply
Use when automating repetitive tasks, connecting apps, or building workflows.
