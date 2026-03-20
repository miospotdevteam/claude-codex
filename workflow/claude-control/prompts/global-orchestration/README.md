# Global Orchestration Prompts

This directory is the future landing zone for Claude-specific prompt surfaces
that make the shared ownership contract apply by default in Claude Code.

These prompts should consume:

- `workflow/core/contracts/agent-ownership.md`
- `workflow/core/contracts/routing-matrix.md`
- `workflow/core/contracts/tool-adapter-rules.md`
- `workflow/core/contracts/parallel-workflows.md`
- `workflow/core/schemas/plan-schema.md`
- `workflow/core/schemas/master-plan-format.md`
- `workflow/core/references/exploration-protocol.md`
- `workflow/core/references/dependency-mapping.md`

They should not duplicate the contract text as their own source of truth.

Canonical editable source:

- `workflow/claude-control/plugin/source/.claude/CLAUDE.md`
- related prompt/runtime surfaces inside
  `workflow/claude-control/plugin/source/`

The temporary `source/` shadow copy has been removed. Edit the staged
`plugin/source/` tree directly.
