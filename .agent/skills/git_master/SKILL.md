---
name: Git Master
description: Advanced Git workflows including branching strategies, rebasing, and conflict resolution
---

# Git Master Skill

## Branching Strategies

### GitFlow
```
main ────────●──────────●────────
              ↑          ↑
develop ──●──●──●──●──●──●──●────
           ↑        ↑
feature ──●●●      ●●●
```

### Trunk-Based (Recommended for CI/CD)
- Short-lived feature branches (< 2 days)
- Merge to main frequently
- Use feature flags for incomplete work

## Essential Commands

| Task | Command |
|------|---------|
| Undo last commit (keep changes) | `git reset --soft HEAD~1` |
| Undo last commit (discard) | `git reset --hard HEAD~1` |
| Amend last commit | `git commit --amend` |
| Interactive rebase | `git rebase -i HEAD~3` |
| Cherry-pick commit | `git cherry-pick <sha>` |
| Stash with message | `git stash push -m "WIP feature"` |
| View stash diff | `git stash show -p stash@{0}` |

## Conflict Resolution

```bash
# During merge conflict:
git status                    # See conflicted files
# Edit files, remove <<<< ==== >>>> markers
git add <file>
git commit                    # Complete merge

# Abort and start over:
git merge --abort
```

## Rebase vs Merge

| Situation | Use |
|-----------|-----|
| Feature branch → main | Rebase (clean history) |
| Shared branch | Merge (preserve history) |
| After push | Never rebase |

## Hooks (Pre-commit)

```bash
# .git/hooks/pre-commit
#!/bin/sh
npm run lint || exit 1
npm test || exit 1
```

## When to Apply
Use when managing branches, resolving conflicts, or cleaning up commit history.
