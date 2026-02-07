---
name: Notion Expert
description: Databases, formulas, templates, and workspace design
---

# Notion Expert Skill

## Core Concepts

### Pages vs Databases

| Pages | Databases |
|-------|-----------|
| Documents | Structured data |
| Linear content | Filterable, sortable |
| One-off notes | Collections of items |

## Database Properties

| Type | Use For |
|------|---------|
| Text | Titles, descriptions |
| Number | Quantities, ratings |
| Select | Single category |
| Multi-select | Tags, labels |
| Date | Deadlines, events |
| Checkbox | Done/not done |
| URL | Links |
| Relation | Link to other database |
| Rollup | Aggregate related data |
| Formula | Calculations |

## Useful Formulas

### Days Until Due
```
dateBetween(prop("Due Date"), now(), "days")
```

### Status Emoji
```
if(prop("Done"), "✅", if(prop("In Progress"), "🔄", "⏳"))
```

### Progress Bar
```
slice("██████████", 0, round(prop("Progress") / 10)) + 
slice("░░░░░░░░░░", 0, 10 - round(prop("Progress") / 10))
```

### Overdue Check
```
if(prop("Due Date") < now() and not prop("Done"), "🔴 OVERDUE", "")
```

## Database Views

| View | Best For |
|------|----------|
| Table | Data entry, bulk editing |
| Board | Kanban, status tracking |
| Calendar | Time-based items |
| Gallery | Visual items (with covers) |
| List | Simple lists |
| Timeline | Gantt-style planning |

## Linked Databases

Create a filtered view of a database anywhere:
1. Type `/linked`
2. Select source database
3. Add filters specific to that view

**Example:** Tasks database → filtered to "This Week" on homepage

## Templates

Create repeatable structures:
- Meeting notes template
- Project template
- Weekly review template

**Button + Template = Automation**

## Workspace Structure

```
Home/
├── Inbox (quick capture)
├── Dashboard (linked DBs)
├── Areas/
│   ├── Work
│   ├── Personal
│   └── Learning
├── Projects/ (database)
├── Tasks/ (database)
└── Resources/ (database)
```

## When to Apply
Use when building Notion workspaces, creating databases, or writing formulas.
