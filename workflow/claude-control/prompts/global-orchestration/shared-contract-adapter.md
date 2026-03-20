# Claude Shared-Contract Adapter

This file binds shared-core placeholders to Claude-specific runtime surfaces.

## Shared-Core Inputs

- `workflow/core/contracts/agent-ownership.md`
- `workflow/core/contracts/routing-matrix.md`
- `workflow/core/contracts/tool-adapter-rules.md`
- `workflow/core/contracts/parallel-workflows.md`
- `workflow/core/schemas/plan-schema.md`
- `workflow/core/schemas/master-plan-format.md`
- `workflow/core/references/exploration-protocol.md`
- `workflow/core/references/dependency-mapping.md`

## Claude Binding

| Shared placeholder | Claude binding |
|---|---|
| `<repo-guidance-file>` | `CLAUDE.md` |
| `<core-engineering-skill-id>` | `look-before-you-leap:engineering-discipline` |
| `<frontend-design-skill-id>` | `look-before-you-leap:frontend-design` |
| `<writing-plans-skill-id>` | `look-before-you-leap:writing-plans` |
| `<dep-query-command>` | Claude plugin `deps-query.py` command from the installed conductor |
| `<dep-config-path>` | `.claude/look-before-you-leap.local.md` |

## Parallel Workflow Binding

Claude already has session-aware plan routing in its upstream runtime. Claude
control should preserve and refine that behavior through:

- session-owned active-plan selection
- tangent and cross-session read-only context loading
- stale-lock recovery
- no silent attachment to another active session's plan

## Claude-Specific Responsibilities

Claude control is allowed to specialize:

- orchestration wording aimed at Claude Code
- hook-based enforcement timing
- user-facing discussion and planning tone
- global defaults that determine when Claude delegates to Codex

Claude control must not redefine:

- who owns intent, planning, frontend, backend, and verification
- the eight discovery questions
- the `plan.json` and `masterPlan.md` relationship
- the rule that `masterPlan.md` freezes after approval
