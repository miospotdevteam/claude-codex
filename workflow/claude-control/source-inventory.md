# Claude Source Inventory

This inventory maps likely source material from the current Claude plugin repo
into the future `workflow/claude-control/` landing zones.

## Current Source Repo

- `~/Projects/claude-code-setup`

## Current Staged Copy And Working Tree

- `workflow/claude-control/plugin/source/`

Copied in this migration stage:

- `README.md`
- `LICENSE`
- `anthropic.md`
- `.claude-plugin/marketplace.json`
- `.claude/CLAUDE.md`
- `look-before-you-leap/`

## Candidate Inputs

- `look-before-you-leap/.claude-plugin/plugin.json`
- `look-before-you-leap/hooks/`
- Claude-oriented conductor/runtime entry points from the current plugin
- future orchestration-specific prompts and defaults

## Target Landing Zones

- `workflow/claude-control/runtime/`
- `workflow/claude-control/prompts/`
- `workflow/claude-control/migration-map.md`

## Shadow-Copy Status

The temporary `source/` shadow copies that previously lived under
`runtime/` and `prompts/` have been removed.

## Important Constraint

Only Claude-specific runtime behavior should land here. Shared policy text
must be referenced from `workflow/core/contracts/`.

The original repo at `~/Projects/claude-code-setup` should stay untouched.
The staged tree under `plugin/source/` is now the editable working
copy inside this repo.

See `workflow/core/migration/transitional-shadow-audit.md` for the current
shadow-copy audit.
