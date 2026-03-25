---
name: main
description: Switch to main branch and pull latest. Handles unstashed changes by asking the user what to do.
allowed-tools: Bash(git *)
---

Switch to the main branch and pull latest changes.

## Steps

### 1. Check for uncommitted changes

```bash
git status --porcelain
```

If there is ANY output (staged, unstaged, or untracked files), **stop and ask the user** what they want to do. Present the status output and ask:

- Stash the changes?
- Commit them to the current branch first?
- Discard them? (confirm twice before doing this)

**Do NOT assume.** Wait for the user's answer before proceeding.

### 2. Switch to main and pull

Only after the working tree is clean:

```bash
git checkout main && git pull
```

### 3. Report

Confirm the switch and show the latest commit:

```bash
git log --oneline -3
```
