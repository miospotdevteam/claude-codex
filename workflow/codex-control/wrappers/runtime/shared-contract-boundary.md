# Codex Wrapper Boundary

Codex wrappers are execution and installation surfaces. They are not the
source of truth for ownership, routing, or planning semantics.

## Wrappers May Do

- install or update Codex skills
- expose worker and verifier entrypoints
- call helper utilities that read and update `plan.json`
- set up Codex-specific auth, model, or CLI defaults
- surface verification or usage-error reporting
- manage session-aware claim and resume behavior for parallel workflows

## Wrappers Must Not Do

- redefine the ownership matrix locally
- change the discovery model independently of shared core
- treat `masterPlan.md` as mutable execution state
- drift from the shared meaning of `plan.json`
- force a single active workflow per repo if the runtime can support better

## Upstream Provenance

Source material will be copied from:

- `workflow/codex-control/plugin/source/scripts/`
- `workflow/codex-control/plugin/source/usage-errors/`

The staged upstream directory is now the canonical editable source in this
repo. The temporary `source/` shadow copy has been removed.
