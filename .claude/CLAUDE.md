# Computer Use 101

Python experiments with Claude computer use.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Runtime | Python 3.14 via `uv` (`.python-version`) |
| AI | TBD (computer use) |

## Code Standards

- **Clean**: Readable code that doesn't need comments
- **Document sparingly**: Only docstrings for 50+ line functions/classes or complex logic
- **Test-driven**: Write minimal unit tests for core functionality first
- **Iterate small**: Test small pieces at a time
- **Single responsibility**: Functions/classes do one thing well
- **Early returns**: Exit early for edge cases and errors
- **Meaningful names**: Variables and functions should self-document
- **No re-exports from `__init__.py`**: Keep `__init__.py` files empty. Import directly from the module.
- **No `__all__`**: Do not define `__all__` in any module.
- **Imports at top**: All imports at the top of the file. Never `try/except ImportError` around imports — env issues must not be masked. No lazy/deferred imports hiding dependency issues.
- **Resource initialization**: External resources (DB clients, wandb, API clients) must be initialized in the entrypoint script and passed into all classes that need them. See `docs/patterns/resource-initialization.md`.
- **Config from files**: Use `config/default.json` for defaults. CLI overrides via `click`. No hardcoded config in library code. See `docs/patterns/configs.md`.
- **CLI with click**: Use `click` for all CLI scripts. Never `argparse`.
- **Lint**: `ruff check .` must pass with zero violations. Line length 120.

## Pre-Commit Checklist

Before committing, complete these steps in order:

1. **Review the diff.** Ask: would a staff software engineer approve this? Iterate until the answer is yes.
2. **Run `/test`** — runs unit tests, lint, smoke test, and opens the game for manual verification.

## Gotchas

- **Free-threaded Python (3.14t)**: Playwright/greenlet crash with bus error on the free-threaded build. Use standard `3.14` for now. Revisit when greenlet ships `3.14t` wheels.
- **Setup**: `uv venv --python 3.14 .venv && source .venv/bin/activate && uv pip install -e ".[dev]" && playwright install chromium`

## Explore This Repo

Use subagents to explore these file groups for key design decisions:

- **Gameplay**: `computer_use_101/minesweeper/env.py`, `computer_use_101/minesweeper/game.html`, `computer_use_101/minesweeper/reward.py`
