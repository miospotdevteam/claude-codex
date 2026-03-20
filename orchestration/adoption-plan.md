# Adoption Plan

This file describes the staged migration from the current global repos to the
transition layout in this repository.

## Stage 0: Lock Ownership

- Define the Claude/Codex ownership contract in shared core
- Define the routing matrix in shared core
- Keep these as the canonical source of truth

## Stage 1: Duplicate Existing Global Repos Into Control-Layer Intent

- Treat `~/Projects/claude-code-setup` as the source input for
  `workflow/claude-control/`
- Treat `~/Projects/codex-setup` as the source input for
  `workflow/codex-control/`
- Do not break the existing global installs yet
- Keep the original external repos untouched
- Treat staged `plugin/source` directories in this repo as editable migration
  copies

Current status:

- staged Claude copy at `workflow/claude-control/plugin/source/`
- staged Codex copy at `workflow/codex-control/plugin/source/`
- those staged trees are now the canonical editable plugin sources in this repo

## Stage 2: Extract Shared Material Into Core

- Move shared policy, contracts, and future common assets into `workflow/core/`
- Remove duplicated policy text from the control layers
- Keep only adaptation logic in `claude-control` and `codex-control`

Current status:

- ownership and routing contracts already live in `workflow/core/contracts/`
- parallel workflow rules now live in `workflow/core/contracts/parallel-workflows.md`
- planning/discovery schemas now live in `workflow/core/schemas/`
- first safe shared tranche has been extracted into:
  - `workflow/core/checklists/`
  - `workflow/core/references/`
- divergent same-name assets are tracked in
  `workflow/core/migration/shared-inventory.md`

## Stage 3: Wire Claude To The Shared Contract

- Make Claude-control consume the shared contract as always-on orchestration behavior
- Ensure Claude defaults to:
  - owning ambiguity and planning
  - delegating the right bounded work to Codex
  - triggering Codex verification after significant work
- Preserve and refine Claude's session-aware parallel workflow behavior

## Stage 4: Wire Codex To The Shared Contract

- Make Codex-control consume the same shared contract as worker/verifier guidance
- Keep Codex-specific runtime assumptions localized to the Codex layer
- Reach parity with same-repo parallel workflow support instead of assuming one
  active workflow per repo

## Stage 5: Validate Integration

- Add orchestration smoke prompts and example tasks
- Verify that Claude behavior and Codex behavior both match the shared contract
- Only then consider whether `workflow/core/` should later become its own repo

Supporting artifacts:

- `orchestration/smoke-tests.md`
- `orchestration/validation/parity-checklist.md`
