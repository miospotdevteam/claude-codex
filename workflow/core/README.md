# Core

`workflow/core/` owns the contracts that must not drift between Claude and
Codex.

This is the intended single source of truth for:

- agent ownership
- routing policy
- planning and discovery contracts
- parallel same-repo workflow rules
- shared references
- shared migration inventory
- future schemas, checklists, and reusable prompt fragments

Nothing in here should assume Claude-only hooks or Codex-only runtime
behavior. Those adaptations belong in the control layers.

Current canonical contracts:

- `contracts/agent-ownership.md`
- `contracts/routing-matrix.md`
- `contracts/tool-adapter-rules.md`
- `contracts/parallel-workflows.md`
- `schemas/plan-schema.md`
- `schemas/master-plan-format.md`
- `references/exploration-protocol.md`
- `references/dependency-mapping.md`
