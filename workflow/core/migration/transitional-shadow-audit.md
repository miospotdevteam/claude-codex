# Transitional Shadow Audit

This note records the final state of the non-canonical `source/` trees that
previously existed under `workflow/claude-control/` and
`workflow/codex-control/`.

## Canonical Rule

- `workflow/claude-control/plugin/source/` is the canonical staged
  Claude source tree in this repo.
- `workflow/codex-control/plugin/source/` is the canonical staged
  Codex source tree in this repo.
- The `source/` directories were transitional shadow copies only.

## Audit Snapshot Before Removal

Claude:

- `runtime/hooks/source/` matches the staged upstream hooks aside from local
  `__pycache__/` output.
- `runtime/manifests/source/` matched the staged upstream Claude plugin
  manifests at the time of audit.

Codex:

- `skills/pack/source/` has drifted from the canonical staged tree.
- That drift includes older copies of the reconciled conductor references and
  scripts under `lbyl-conductor/`.
- `wrappers/installers/source/` does not fully mirror the staged upstream
  `scripts/` directory.
- `wrappers/runtime/source/` is not a clean mirror of the staged upstream
  runtime/error surface.

## Current State

The temporary `source/` shadow copies have been removed.

Use the staged `plugin/upstream-*` trees as the authoritative editable input
for ongoing migration work.
