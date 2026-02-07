---
name: Prompt Engineer
description: Writing effective AI prompts and chain-of-thought techniques
---

# Prompt Engineer Skill

## Prompt Structure

### Clear Instruction Pattern
```
[Role/Context]
[Task]
[Format Requirements]
[Constraints]
[Examples (optional)]
```

### Example
```
You are an expert copywriter.

Write a product description for a wireless keyboard.

Requirements:
- 150 words max
- Include 3 key features
- End with a call-to-action

Tone: Professional but friendly
Audience: Remote workers
```

## Techniques

### Chain-of-Thought (CoT)
> "Think step by step. First, analyze the problem. Then, list possible solutions. Finally, recommend the best approach."

### Few-Shot Learning
```
Q: What is the capital of France?
A: Paris

Q: What is the capital of Germany?
A: Berlin

Q: What is the capital of Italy?
A: [Model completes: Rome]
```

### Role Playing
> "You are a senior software engineer reviewing code. Point out potential bugs and suggest improvements."

### Constraint Setting
> "Respond in exactly 3 bullet points."
> "Use only information from the provided context."
> "Do not include any code examples."

## Output Formatting

### JSON Output
```
Respond in JSON format:
{
  "summary": "...",
  "key_points": ["...", "..."],
  "recommendation": "..."
}
```

### Markdown Tables
> "Format your response as a markdown table with columns: Feature, Benefit, Priority"

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Vague instructions | Be specific and concrete |
| Too many asks | One primary task per prompt |
| No format guidance | Specify desired output format |
| Missing context | Provide relevant background |

## Temperature Guide

| Setting | Use For |
|---------|---------|
| 0.0-0.3 | Factual, consistent outputs |
| 0.4-0.7 | Balanced creativity |
| 0.8-1.0 | Creative, varied outputs |

## When to Apply
Use when crafting prompts, optimizing AI interactions, or building AI-powered features.
