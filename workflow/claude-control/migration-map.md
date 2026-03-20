# Claude Control Migration Map

Source repo today:

- `~/Projects/claude-code-setup`

## Likely Inputs

- Claude plugin runtime and hook model from `look-before-you-leap/`
- existing Claude-oriented documentation and conductor logic
- future orchestration defaults that should apply globally in Claude Code

## Target Role

Move Claude-specific consumption of the shared contract here:

- default orchestration instructions for Claude
- task-routing defaults that point work to Codex when appropriate
- future globally installed control surfaces that tell Claude when to:
  - keep work local
  - delegate to Codex worker
  - trigger Codex verifier

## Non-Goals

- Do not move shared routing policy here as the source of truth
- Do not copy Codex-specific wrappers or worker/verifier prompts here

## Initial Scaffold

This directory is now adapter-first. The future migration should add:

- Claude orchestration prompt surfaces
- install/runtime wiring
- tests or smoke prompts for global Claude behavior

## Current Migration Status

- A curated staged copy of the current Claude source repo now lives under
  `workflow/claude-control/plugin/source/`
- Shared-core extraction has started separately in `workflow/core/`
- The planning/discovery contract cluster now points at shared-core canonical
  docs under `workflow/core/schemas/` and `workflow/core/references/`
- Parallel same-repo workflow behavior is now treated as a shared-core
  requirement, not a Claude-only convenience
- Claude adapter and boundary documents now define how the staged plugin tree
  maps into runtime and package surfaces
- The staged Claude plugin tree is now the canonical editable source in this
  repo; the original external repo remains untouched
- The staged Claude conductor reference cluster now aligns with shared-core
  semantics for `plan-schema.md`, `master-plan-format.md`,
  `exploration-protocol.md`, and `dependency-mapping.md`
- The staged Claude dep-map script cluster now aligns with shared-core
  semantics for flexible query invocation, dynamic-import discovery,
  tsconfig path/baseUrl resolution, and cross-tool project-root detection in
  `init-plan-dir.sh`
- The staged Claude session-management script cluster now aligns with
  shared-core semantics for session-aware resume/status output,
  unclaimed-plan claiming, and safe `complete-plan` handling
- Transitional `source/` shadow copies have been removed. The staged
  `plugin/source/` tree is now the only editable source surface in
  this repo for Claude-control assets
