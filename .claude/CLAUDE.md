# Computer Use 101

Python experiments with Claude computer use.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Runtime | Python 3.12 |
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
