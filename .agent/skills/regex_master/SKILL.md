---
name: Regex Master
description: Pattern matching recipes and common regex patterns
---

# Regex Master Skill

## Common Patterns

| Pattern | Regex | Example Match |
|---------|-------|---------------|
| Email | `[\w.-]+@[\w.-]+\.\w+` | user@domain.com |
| Phone (US) | `\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}` | (555) 123-4567 |
| URL | `https?://[\w.-]+(?:/[\w./-]*)` | https://example.com/page |
| IP Address | `\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}` | 192.168.1.1 |
| Date (MM/DD/YYYY) | `\d{2}/\d{2}/\d{4}` | 12/25/2024 |
| Zip Code | `\d{5}(-\d{4})?` | 12345 or 12345-6789 |
| Credit Card | `\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}` | 1234-5678-9012-3456 |

## Metacharacters

| Char | Meaning |
|------|---------|
| `.` | Any character |
| `\d` | Digit [0-9] |
| `\w` | Word char [a-zA-Z0-9_] |
| `\s` | Whitespace |
| `^` | Start of line |
| `$` | End of line |
| `*` | 0 or more |
| `+` | 1 or more |
| `?` | 0 or 1 |
| `{n,m}` | Between n and m |

## Capture Groups

```regex
# Capture parts of a match
(\d{3})-(\d{4})   # Captures 555 and 1234 from 555-1234

# Named groups (Python)
(?P<area>\d{3})-(?P<number>\d{4})

# Non-capturing group
(?:prefix-)?word   # Matches "prefix-word" or "word"
```

## Lookahead/Lookbehind

```regex
# Positive lookahead: match X followed by Y
foo(?=bar)        # Matches "foo" in "foobar"

# Negative lookahead: match X not followed by Y
foo(?!bar)        # Matches "foo" in "foobaz"

# Positive lookbehind: match X preceded by Y
(?<=@)\w+         # Matches "domain" in "@domain"

# Negative lookbehind
(?<!@)\bword\b    # "word" not preceded by @
```

## Find/Replace Examples

| Find | Replace | Result |
|------|---------|--------|
| `(\w+), (\w+)` | `$2 $1` | "Doe, John" → "John Doe" |
| `\s+` | ` ` | Collapse multiple spaces |
| `^` | `> ` | Add quote to start of lines |

## Flags

| Flag | Meaning |
|------|---------|
| `i` | Case-insensitive |
| `g` | Global (all matches) |
| `m` | Multiline (^ $ match line starts/ends) |
| `s` | Dotall (. matches newlines) |

## When to Apply
Use when parsing text, validating input, or doing find/replace operations.
