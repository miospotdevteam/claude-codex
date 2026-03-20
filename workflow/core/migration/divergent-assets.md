# Divergent Assets

These assets exist in both the staged Claude and Codex source trees but are not
currently identical, so they must not be treated as shared automatically.

## Divergent Same-Name Reference Files

Claude source:

- `workflow/claude-control/plugin/source/look-before-you-leap/skills/look-before-you-leap/references/`

Codex source:

- `workflow/codex-control/plugin/source/codex-skills/lbyl-conductor/references/`

Current unresolved divergent files:

- `api-contracts-checklist.md`
- `claude-md-snippet.md`
- `exploration-guide.md`
- `frontend-design-guide.md`
- `git-checklist.md`
- `recommended-plugins.md`
- `verification-commands.md`

## Reconciled Into Shared Core

The following same-name assets were divergent upstream but have now been
reconciled into tool-agnostic shared-core documents:

- `dependency-mapping.md` -> `workflow/core/references/dependency-mapping.md`
- `exploration-protocol.md` -> `workflow/core/references/exploration-protocol.md`
- `master-plan-format.md` -> `workflow/core/schemas/master-plan-format.md`
- `plan-schema.md` -> `workflow/core/schemas/plan-schema.md`

Parallel same-repo workflow behavior is also now defined centrally in:

- `workflow/core/contracts/parallel-workflows.md`

## Same-Name Conductor Scripts

Claude source:

- `workflow/claude-control/plugin/source/look-before-you-leap/skills/look-before-you-leap/scripts/`

Codex source:

- `workflow/codex-control/plugin/source/codex-skills/lbyl-conductor/scripts/`

Semantically reconciled but still adapter-specific:

- `deps-generate.py`
- `deps-query.py`
- `init-plan-dir.sh`
- `plan-status.sh`
- `plan_utils.py`
- `resume.sh`

These files now share the same underlying behavior across Claude and Codex, but
retain tool-specific bindings for config loading, config file locations, skill
names, and local runtime conventions.

## Skill Set Shape Difference

Claude upstream skill tree currently includes:

- `brainstorming`
- `doc-coauthoring`
- `engineering-discipline`
- `frontend-design`
- `immersive-frontend`
- `look-before-you-leap`
- `mcp-builder`
- `persistent-plans`
- `react-native-mobile`
- `refactoring`
- `skill-review-standard`
- `svg-art`
- `systematic-debugging`
- `test-driven-development`
- `webapp-testing`
- `writing-plans`

Codex-native skill tree currently includes:

- `lbyl-agent-setup`
- `lbyl-brainstorming`
- `lbyl-conductor`
- `lbyl-cost-optimization`
- `lbyl-engineering-discipline`
- `lbyl-frontend-design`
- `lbyl-persistent-plans`
- `lbyl-refactoring`
- `lbyl-skill-creator`
- `lbyl-systematic-debugging`
- `lbyl-test-driven-development`
- `lbyl-writing-plans`

This means the migration cannot assume one-to-one skill parity. Some future
shared assets will need adapter mappings rather than literal moves.
