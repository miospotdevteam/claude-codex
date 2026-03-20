# Codex Package Boundary Map

This file maps the staged Codex source tree into the future package,
skills, and wrapper landing zones.

## Skill Inputs

| Staged source | Future landing zone | Notes |
|---|---|---|
| `plugin/source/codex-skills/` | `skills/pack/` | Primary Codex-native skill source |
| `plugin/source/AGENTS.md` | `skills/pack/` or runtime defaults | Codex-facing repo guidance should point back to shared core |
| `workflow/claude-control/plugin/source/look-before-you-leap/skills/` | External shared dependency | Upstream-only skills consumed from the canonical Claude staged tree, not vendored here |

## Wrapper Inputs

| Staged source | Future landing zone | Notes |
|---|---|---|
| `plugin/source/scripts/install-codex-skills.sh` | `wrappers/installers/` | Installer behavior stays Codex-specific |
| `plugin/source/scripts/bootstrap-codex-skills-from-github.sh` | `wrappers/installers/` | Distribution/bootstrap behavior stays Codex-specific |
| `plugin/source/scripts/log-usage-error.sh` | `wrappers/runtime/` | Runtime helper, not shared-core policy |
| `plugin/source/usage-errors/` | `wrappers/runtime/` or package docs | Operational feedback surface |

## Shared-Core Dependencies

These package surfaces should consume, not duplicate:

- `workflow/core/contracts/agent-ownership.md`
- `workflow/core/contracts/routing-matrix.md`
- `workflow/core/contracts/tool-adapter-rules.md`
- `workflow/core/contracts/parallel-workflows.md`
- `workflow/core/schemas/plan-schema.md`
- `workflow/core/schemas/master-plan-format.md`
- `workflow/core/references/exploration-protocol.md`
- `workflow/core/references/dependency-mapping.md`
