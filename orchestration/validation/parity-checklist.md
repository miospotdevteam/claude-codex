# Parity Checklist

Use this checklist before changing any global install path.

## Tree Parity

- Claude staged copy includes the expected plugin runtime, hooks, commands,
  manifests, and repo-level support files
- Codex staged copy includes the expected skill pack, installer scripts,
  usage-error helpers, and references to shared Claude skills where required

## Shared-Core Parity

- Shared contracts exist only in `workflow/core/contracts/`
- Parallel workflow behavior is defined in shared core rather than hidden in a
  single tool runtime
- Canonical planning/discovery schema docs live in `workflow/core/schemas/`
- Extracted shared checklists and references are documented in
  `workflow/core/migration/shared-inventory.md`
- Divergent same-name assets are not silently treated as shared

## Install-Surface Parity

- Claude plugin/package boundary is defined under `workflow/claude-control/plugin/`
- Codex package boundary is defined under `workflow/codex-control/plugin/`
- Original external repos remain untouched
- Staged plugin trees in this repo are the canonical editable plugin sources
- Install/cutover docs identify what global path would change and how to roll back

## Orchestration Parity

- Root compatibility wrappers still work
- Canonical orchestration scripts still work
- Canonical orchestration agent definitions remain aligned with the shared contract
- Parallel same-repo workflows have an explicit ownership and resume story for
  both Claude and Codex
- Codex copied helper scripts support session-owned resume and unclaimed-plan
  claiming before any global cutover
- Codex copied status tooling exposes ownership state clearly enough to debug
  multi-session repo usage
