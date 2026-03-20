#!/usr/bin/env bash
# UserPromptSubmit hook: Detect when the user asks for brainstorming/design
# discussion and inject a reminder to invoke the brainstorming skill.
#
# Triggers on keywords: brainstorm, think through, design options, let's discuss,
# explore tradeoffs, explore options, how should we, what's the best approach.
#
# Input: JSON on stdin with user_prompt

set -euo pipefail

INPUT=$(cat)

# Extract user prompt
USER_PROMPT=$(python3 -c "
import json, sys
data = json.loads(sys.stdin.read())
print(data.get('user_prompt', ''))
" <<< "$INPUT" 2>/dev/null) || true

[ -z "$USER_PROMPT" ] && exit 0

# Check for brainstorming intent keywords
export HOOK_PROMPT="$USER_PROMPT"

NEEDS_BRAINSTORM=$(python3 << 'PYEOF'
import re, os, sys

prompt = os.environ.get("HOOK_PROMPT", "").lower()
if not prompt:
    print("no")
    sys.exit(0)

# Keywords that signal brainstorming intent
PATTERNS = [
    r"\bbrainstorm\b",
    r"\bthink through\b",
    r"\bdesign options?\b",
    r"\blet'?s discuss\b",
    r"\bexplore (the )?(tradeoffs?|options?|approaches?)\b",
    r"\bhow should we\b",
    r"\bwhat'?s the best (approach|way|design)\b",
    r"\btalk through\b",
    r"\bweigh (the )?(options?|pros|tradeoffs?)\b",
    r"\bbefore (we |you )?(code|implement|build|start)\b.*\b(think|discuss|design)\b",
]

for pattern in PATTERNS:
    if re.search(pattern, prompt):
        print("yes")
        sys.exit(0)

print("no")
PYEOF
) || true

if [ "$NEEDS_BRAINSTORM" != "yes" ]; then
  exit 0
fi

# Inject reminder
python3 << 'PYEOF'
import json, sys

output = {
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": (
            "The user is asking for brainstorming/design discussion. "
            "You MUST invoke the brainstorming skill using the Skill tool:\n\n"
            "  Skill(skill: \"look-before-you-leap:brainstorming\")\n\n"
            "Do NOT brainstorm inline by just talking. The skill has structured "
            "phases, challenges assumptions, and produces a design.md that feeds "
            "into planning. Ad-hoc conversation does not replicate this."
        )
    }
}
json.dump(output, sys.stdout)
PYEOF
