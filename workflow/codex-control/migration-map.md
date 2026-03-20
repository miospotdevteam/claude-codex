# Codex Control Migration Map

Source repo today:

- `~/Projects/codex-setup`

## Likely Inputs

- Codex-native skill pack under `codex-skills/`
- current Codex-specific adaptation strategy from the repo README
- worker/verifier patterns and install surfaces

## Target Role

Move Codex-specific consumption of the shared contract here:

- worker guidance
- verifier guidance
- Codex-native orchestration awareness
- install and wrapper behavior that is specific to Codex CLI

## Non-Goals

- Do not copy Claude hook/runtime assumptions here
- Do not make this directory the source of truth for ownership policy

## Initial Scaffold

This directory is now adapter-first. The future migration should add:

- Codex-native prompt/control files
- references to worker/verifier patterns
- tests or smoke prompts proving Codex consumes the shared contract correctly

## Current Migration Status

- A curated staged copy of the current Codex source repo now lives under
  `workflow/codex-control/plugin/source/`
- Shared-core extraction has started separately in `workflow/core/`
- The planning/discovery contract cluster now points at shared-core canonical
  docs under `workflow/core/schemas/` and `workflow/core/references/`
- Parallel same-repo workflow behavior is now a required compatibility target
  for Codex migration
- Codex adapter and boundary documents now define how the staged plugin tree
  maps into skill, wrapper, and package surfaces
- The staged Codex plugin tree is now the canonical editable source in this
  repo; the original external repo remains untouched
- The staged Codex conductor reference cluster now aligns with shared-core
  semantics for `plan-schema.md`, `master-plan-format.md`,
  `exploration-protocol.md`, and `dependency-mapping.md`
- The staged Codex conductor now has a first session-aware parallel-workflow
  tranche in
  `plugin/source/codex-skills/lbyl-conductor/scripts/plan_utils.py`,
  `plugin/source/codex-skills/lbyl-conductor/scripts/resume.sh`, and
  `plugin/source/codex-skills/lbyl-conductor/scripts/plan-status.sh`
- The staged Codex dep-map script cluster now aligns with shared-core
  semantics for dynamic-import discovery, tsconfig path/baseUrl resolution,
  flexible query invocation, and cross-tool project-root detection in
  `init-plan-dir.sh`
- The staged Codex session-management script cluster now aligns with
  shared-core semantics for session-aware resume/status output,
  unclaimed-plan claiming, safe `complete-plan` handling, and soft warnings
  when steps are closed without finishing progress/result fields
- Transitional `source/` shadow copies have been removed. The staged
  `plugin/source/` tree is now the only editable source surface in
  this repo for Codex-control assets
