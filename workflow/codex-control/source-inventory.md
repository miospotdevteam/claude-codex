# Codex Source Inventory

This inventory maps likely source material from the current Codex setup repo
into the future `workflow/codex-control/` landing zones.

## Current Source Repo

- `~/Projects/codex-setup`

## Current Staged Copy And Working Tree

- `workflow/codex-control/plugin/source/`

Copied in this migration stage:

- `README.md`
- `LICENSE`
- `AGENTS.md`
- `codex-skills/`
- `scripts/`
- `usage-errors/`

## Candidate Inputs

- `codex-skills/`
- selected upstream-only skills from
  `workflow/claude-control/plugin/source/look-before-you-leap/skills/`
- Codex-native worker/verifier prompts
- install helpers under `scripts/`
- adaptation notes that currently live in the repo README

## Target Landing Zones

- `workflow/codex-control/skills/`
- `workflow/codex-control/wrappers/`
- `workflow/codex-control/migration-map.md`

## Shadow-Copy Status

The temporary `source/` shadow copies that previously lived under
`skills/pack/` and `wrappers/` have been removed.

## Important Constraint

Codex-control should consume the shared contract, not duplicate it as its own
source of truth.

The original repo at `~/Projects/codex-setup` should stay untouched. The
staged tree under `plugin/source/` is now the editable working copy
inside this repo.

See `workflow/core/migration/transitional-shadow-audit.md` for the current
shadow-copy audit.
