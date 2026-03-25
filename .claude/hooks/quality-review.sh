#!/usr/bin/env bash
# PreToolUse hook: review code quality before git add

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

# Only act on git add commands
if ! echo "$COMMAND" | grep -q 'git add'; then
  exit 0
fi

cat <<'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "additionalContext": "QUALITY REVIEW REQUIRED: Before staging files, you MUST:\n1. Read .claude/CLAUDE.md to refresh the project's code standards.\n2. Run `git diff` (or `git diff --cached` if files are already staged) and review every changed line against those standards.\n3. Fix any violations BEFORE running git add.\n\nDo NOT proceed with git add until the review is complete and all issues are resolved."
  }
}
EOF
