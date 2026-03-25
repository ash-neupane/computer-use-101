#!/usr/bin/env bash
# Stop hook: block Claude from finishing if source or test files changed without /test
set -euo pipefail

CHANGED=$(git diff --name-only HEAD 2>/dev/null || git diff --name-only 2>/dev/null || echo "")

if echo "$CHANGED" | grep -qE '^(computer_use_101/|tests/)'; then
  echo '{"decision":"block","reason":"Source or test files changed. Run /test before finishing."}'
fi
