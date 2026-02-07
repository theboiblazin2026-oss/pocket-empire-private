---
name: Obsidian Pro
description: Linking, plugins, workflows, and knowledge graphs
---

# Obsidian Pro Skill

## Core Philosophy

Obsidian is a **local-first, Markdown-based** knowledge system built on:
- **Bidirectional linking** - Notes connect to each other
- **Graph view** - Visualize connections
- **Plain text** - Future-proof, portable

## Linking

### Basic Link
```markdown
[[Note Name]]
[[Note Name|Display Text]]
[[Note Name#Heading]]
```

### Unlinked Mentions
Obsidian finds text matching note titles even without explicit links.

### Backlinks
Every note shows what links TO it (automatic).

## Folder Structure vs Tags vs Links

| Method | Best For |
|--------|----------|
| Folders | Broad categories, projects |
| Tags | Cross-cutting themes |
| Links | Relationships between ideas |

**Recommendation:** Use all three. Links > Tags > Folders in importance.

## Essential Plugins

### Core Plugins
- **Daily Notes** - Journaling, quick capture
- **Templates** - Repeatable structures
- **Graph View** - Visualize connections
- **Backlinks** - See what links to current note

### Community Plugins (must-have)
| Plugin | Purpose |
|--------|---------|
| Dataview | Query notes like a database |
| Templater | Advanced templates with logic |
| Calendar | Navigate daily notes |
| Periodic Notes | Weekly/monthly notes |
| Excalidraw | Visual thinking |
| QuickAdd | Rapid capture |

## Dataview Examples

### List all notes tagged #project
```dataview
LIST
FROM #project
SORT file.mtime DESC
```

### Table of tasks
```dataview
TABLE status, due
FROM "Tasks"
WHERE !completed
SORT due ASC
```

## Zettelkasten Method

1. **Fleeting Notes** - Quick captures
2. **Literature Notes** - From sources
3. **Permanent Notes** - Your own ideas
4. **Link everything** - Build a web of thought

## Daily Note Template

```markdown
# {{date:YYYY-MM-DD}}

## Morning
- [ ] Review yesterday
- [ ] Top 3 priorities

## Notes


## Evening
- What went well?
- What could improve?
```

## When to Apply
Use when building knowledge bases, linking ideas, or optimizing Obsidian workflows.
