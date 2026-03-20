## LBYL Codex Setup

This repository contains a Codex port of the `look-before-you-leap` discipline plugin.

### Skills in this repo

Codex-native skills:
- `codex-skills/lbyl-conductor`
- `codex-skills/lbyl-cost-optimization`
- `codex-skills/lbyl-engineering-discipline`
- `codex-skills/lbyl-persistent-plans`
- `codex-skills/lbyl-writing-plans`
- `codex-skills/lbyl-test-driven-development`
- `codex-skills/lbyl-systematic-debugging`
- `codex-skills/lbyl-refactoring`
- `codex-skills/lbyl-frontend-design`
- `codex-skills/lbyl-brainstorming`
- `codex-skills/lbyl-agent-setup`
- `codex-skills/lbyl-skill-creator`

Shared Claude skills consumed from the staged Claude tree in this monorepo:
- `workflow/claude-control/plugin/source/look-before-you-leap/skills/look-before-you-leap`
- `workflow/claude-control/plugin/source/look-before-you-leap/skills/engineering-discipline`
- `workflow/claude-control/plugin/source/look-before-you-leap/skills/persistent-plans`
- `workflow/claude-control/plugin/source/look-before-you-leap/skills/writing-plans`
- `workflow/claude-control/plugin/source/look-before-you-leap/skills/test-driven-development`
- `workflow/claude-control/plugin/source/look-before-you-leap/skills/systematic-debugging`
- `workflow/claude-control/plugin/source/look-before-you-leap/skills/refactoring`
- `workflow/claude-control/plugin/source/look-before-you-leap/skills/immersive-frontend`
- `workflow/claude-control/plugin/source/look-before-you-leap/skills/brainstorming`
- `workflow/claude-control/plugin/source/look-before-you-leap/skills/doc-coauthoring`
- `workflow/claude-control/plugin/source/look-before-you-leap/skills/mcp-builder`
- `workflow/claude-control/plugin/source/look-before-you-leap/skills/react-native-mobile`
- `workflow/claude-control/plugin/source/look-before-you-leap/skills/skill-review-standard`
- `workflow/claude-control/plugin/source/look-before-you-leap/skills/svg-art`
- `workflow/claude-control/plugin/source/look-before-you-leap/skills/webapp-testing`

### Operating rules
- Default to `lbyl-conductor` + `lbyl-engineering-discipline` for coding work.
- Before editing source, create `.temp/plan-mode/active/<plan-name>/plan.json` and `.temp/plan-mode/active/<plan-name>/masterPlan.md`.
- Present non-trivial plans through Orbit review before source edits unless the user explicitly skips that review.
- Update plan progress every 2-3 file edits.
- Verify with project typecheck, lint, and relevant tests before declaring done.
- If a future session uncovers a failure caused by the LBYL skill pack itself, log it here under `usage-errors/`, preferably via `bash scripts/log-usage-error.sh "short title"`.
- Never silently drop requested scope.

### Install

```bash
bash scripts/install-codex-skills.sh
bash scripts/bootstrap-codex-skills-from-github.sh
```

This installs the Codex-native `lbyl-*` skills plus the shared Claude skill
set from
`workflow/claude-control/plugin/source/look-before-you-leap/skills/`,
except `frontend-design`, into `~/.codex/skills`. The Claude
`frontend-design` source remains available in the Claude staged tree for sync
purposes, but Codex sessions use `lbyl-frontend-design` as the single standard
frontend design skill. The Claude-sourced skills such as `doc-coauthoring`,
`mcp-builder`, `svg-art`, and `webapp-testing` are also installed from that
Claude staged tree. `immersive-frontend` remains installed as the separate
motion-heavy frontend skill. For multi-machine use, prefer
`scripts/bootstrap-codex-skills-from-github.sh` so each machine clones or
pulls the GitHub repo and then runs the local installer.
