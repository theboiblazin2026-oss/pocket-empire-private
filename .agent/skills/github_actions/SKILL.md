---
name: GitHub Actions
description: Workflows, actions marketplace, secrets, matrix builds
---

# GitHub Actions Skill

## Workflow Structure

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - run: npm ci
      - run: npm test
      - run: npm run build
```

## Matrix Builds

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
        node: [18, 20]
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
```

## Secrets

```yaml
- name: Deploy
  env:
    API_KEY: ${{ secrets.API_KEY }}
  run: ./deploy.sh
```

## Triggers

```yaml
on:
  push:
  pull_request:
  schedule:
    - cron: '0 0 * * *'  # Daily
  workflow_dispatch:      # Manual
```

## When to Apply
Use when setting up CI/CD for GitHub repositories.
