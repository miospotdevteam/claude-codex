# Claude Hook Boundary

Claude hooks are enforcement and reminder surfaces. They are not the source of
truth for ownership, routing, or planning semantics.

## Hooks May Do

- enforce that planning artifacts exist
- remind the agent to run dependency-query when configured
- mark dependency maps stale after relevant edits
- validate step completion against the current `plan.json`
- inject runtime context that points back to shared-core contracts
- maintain session-aware plan selection for parallel workflows

## Hooks Must Not Do

- redefine who owns backend vs frontend work
- change the discovery model independently of shared core
- treat `masterPlan.md` as mutable execution state
- silently weaken verification expectations
- collapse the repo into a single active workflow when multiple sessions are
  allowed

## Upstream Provenance

Source material will be copied from:

- `workflow/claude-control/plugin/source/look-before-you-leap/hooks/`

The staged upstream directory is now the canonical editable source in this
repo. The temporary `source/` shadow copy has been removed.
