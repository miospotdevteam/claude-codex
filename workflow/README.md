# Workflow

This directory is the future home of the globally shared workflow layer.

It is split into:

- `core/` for shared contracts and eventually shared schemas/checklists/scripts
- `claude-control/` for Claude-specific runtime and orchestration behavior
- `codex-control/` for Codex-specific worker/verifier behavior

The rule is simple:

- shared policy lives in `core/`
- tool-specific adapters live in the control layers
- integration examples live outside this directory in `orchestration/`

Migration rules:

- original external setup repos stay untouched
- staged `plugin/source` trees in this repo are editable migration copies
- shared core must allow parallel workflows in the same repo
