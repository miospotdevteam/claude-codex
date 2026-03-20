# Codex Shared-Contract Adapter

This file binds shared-core placeholders to Codex-specific runtime surfaces.

## Shared-Core Inputs

- `workflow/core/contracts/agent-ownership.md`
- `workflow/core/contracts/routing-matrix.md`
- `workflow/core/contracts/tool-adapter-rules.md`
- `workflow/core/contracts/parallel-workflows.md`
- `workflow/core/schemas/plan-schema.md`
- `workflow/core/schemas/master-plan-format.md`
- `workflow/core/references/exploration-protocol.md`
- `workflow/core/references/dependency-mapping.md`

## Codex Binding

| Shared placeholder | Codex binding |
|---|---|
| `<repo-guidance-file>` | `AGENTS.md` |
| `<core-engineering-skill-id>` | `lbyl-engineering-discipline` |
| `<frontend-design-skill-id>` | `lbyl-frontend-design` |
| `<writing-plans-skill-id>` | `lbyl-writing-plans` |
| `<dep-query-command>` | Codex skill `deps-query.py` command from the installed conductor |
| `<dep-config-path>` | `.codex/lbyl-deps.json` |

## Parallel Workflow Binding

Codex control must reach parity with Claude's same-repo parallel workflow
behavior. That means Codex needs:

- session-owned active-plan selection
- resume behavior that prefers the current session's plan
- explicit foreign-plan targeting for tangent or review work
- stale-ownership recovery

Codex migration is not complete until those behaviors exist in Codex-native
helpers or wrappers.

Current implemented parity tranche:

- `plugin/source/codex-skills/lbyl-conductor/scripts/plan_utils.py`
- `plugin/source/codex-skills/lbyl-conductor/scripts/resume.sh`
- `plugin/source/codex-skills/lbyl-conductor/scripts/plan-status.sh`

## Codex-Specific Responsibilities

Codex control is allowed to specialize:

- skill-pack wording aimed at Codex sessions
- wrapper and installer behavior
- worker/verifier-specific prompt surfaces
- Codex-specific helper utilities that operate on shared plan semantics

Codex control must not redefine:

- who owns intent, planning, frontend, backend, and verification
- the eight discovery questions
- the `plan.json` and `masterPlan.md` relationship
- the rule that `masterPlan.md` freezes after approval
