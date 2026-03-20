# Claude Package Boundary Map

This file maps the immutable staged Claude mirror into the future package and
runtime landing zones.

## Package Inputs

| Staged source | Future landing zone | Notes |
|---|---|---|
| `plugin/source/look-before-you-leap/.claude-plugin/plugin.json` | `runtime/manifests/` | Claude plugin manifest stays Claude-specific |
| `plugin/source/.claude-plugin/marketplace.json` | `plugin/package/` | Packaging and distribution metadata |
| `plugin/source/look-before-you-leap/commands/` | `plugin/package/` or `runtime/` | Keep only if still part of the installed Claude surface |

## Runtime Inputs

| Staged source | Future landing zone | Notes |
|---|---|---|
| `plugin/source/look-before-you-leap/hooks/` | `runtime/hooks/` | Hook model is Claude-specific and should remain here |
| `plugin/source/.claude/CLAUDE.md` | `prompts/global-orchestration/` | Canonical Claude wording should point back to shared core |
| `plugin/source/anthropic.md` | `runtime/defaults/` or `plugin/package/` | Keep only if still needed for installation/runtime defaults |

## Shared-Core Dependencies

These runtime/package surfaces should consume, not duplicate:

- `workflow/core/contracts/agent-ownership.md`
- `workflow/core/contracts/routing-matrix.md`
- `workflow/core/contracts/tool-adapter-rules.md`
- `workflow/core/contracts/parallel-workflows.md`
- `workflow/core/schemas/plan-schema.md`
- `workflow/core/schemas/master-plan-format.md`
- `workflow/core/references/exploration-protocol.md`
- `workflow/core/references/dependency-mapping.md`
