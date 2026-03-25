---
name: test
description: Run the full testing protocol for the minesweeper RL environment. Use when changes are made to computer_use_101/ or tests/ and need verification before committing.
argument-hint: "[env-name]"
allowed-tools: Bash(pytest *, ruff *, python *, open *)
---

Run the full testing protocol for the minesweeper RL environment.

## Steps

### 1. Unit tests

```bash
pytest tests/ -v
```

All tests must pass. No skips unless documented.

### 2. Lint

```bash
ruff check .
```

Zero violations.

### 3. Smoke test

```bash
python ${CLAUDE_SKILL_DIR}/smoke_test.py
```

Sanity check: mean reward should be negative (random play hits mines), mean length should be less than total cells.

### 4. Manual play

Open the game for the user to verify visually:

```bash
open computer_use_101/minesweeper/game.html
```

Verify:
- Cells reveal on click
- Flood-fill works on zero-neighbor cells
- Mine click ends the game with blood splatter
- Win triggers confetti
- Numbers and colors are correct

### 5. Report

Summarize results: tests passed/failed, lint status, smoke test stats, and confirm the game opened.
