# Shared Inventory

This file inventories the kinds of material that should migrate into
`workflow/core/` instead of staying duplicated in the Claude and Codex setup
repos.

## Strong Shared-Core Candidates

- ownership contract
- routing matrix
- discovery and planning schemas
- parallel workflow semantics
- shared checklists
- reusable verification criteria
- future common scripts that are tool-agnostic
- prompt fragments that are agent-agnostic

## Already Extracted First Tranche

The following files were verified as byte-identical between:

- `workflow/claude-control/plugin/source/look-before-you-leap/skills/look-before-you-leap/references/`
- `workflow/codex-control/plugin/source/codex-skills/lbyl-conductor/references/`

Shared checklists now extracted into `workflow/core/checklists/`:

- `dependency-checklist.md`
- `frontend-design-checklist.md`
- `linting-checklist.md`
- `security-checklist.md`
- `testing-checklist.md`
- `ui-consistency-checklist.md`

Shared references now extracted into `workflow/core/references/`:

- `anti-slop.md`
- `api-contracts-guide.md`
- `color-palettes.md`
- `debugging-condition-based-waiting.md`
- `debugging-defense-in-depth.md`
- `debugging-root-cause-tracing.md`
- `security-guide.md`
- `sub-plan-format.md`
- `testing-strategy.md`
- `ui-consistency-guide.md`

## Reconciled Shared Contract Cluster

The first non-identical but semantically shared planning/discovery cluster now
lives in shared core as canonical reconciled documents:

- `workflow/core/contracts/parallel-workflows.md`
- `workflow/core/schemas/plan-schema.md`
- `workflow/core/schemas/master-plan-format.md`
- `workflow/core/references/exploration-protocol.md`
- `workflow/core/references/dependency-mapping.md`

These are intentionally tool-agnostic. Claude and Codex consume them through
adapter documents in their respective control layers.

## Divergent Same-Name Assets

These filenames exist in both source trees but currently differ and require
manual reconciliation before extraction into core:

- `api-contracts-checklist.md`
- `claude-md-snippet.md`
- `exploration-guide.md`
- `frontend-design-guide.md`
- `git-checklist.md`
- `recommended-plugins.md`
- `verification-commands.md`

See also: `workflow/core/migration/divergent-assets.md`

## Must Stay Out Of Shared Core

- Claude-only hooks and runtime enforcement
- Codex-only wrappers and CLI assumptions
- auth and install behavior tied to one tool
- tool-specific user experience conventions
- plugin manifests and installation surfaces

## Current Source Repos

- `~/Projects/claude-code-setup`
- `~/Projects/codex-setup`

## Migration Standard

- extract shared contracts into `workflow/core/`
- adapt them into `workflow/claude-control/` and `workflow/codex-control/`
- do not duplicate the same policy text in both control layers
