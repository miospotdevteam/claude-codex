# Codex Runtime Wrappers

This directory is the future landing zone for Codex runtime wrappers and
control scripts that are specific to Codex usage.

This is distinct from `orchestration/scripts/`, which currently owns the
integration-level worker/verifier wrappers for the combined system.

Runtime wrappers must preserve same-repo parallel workflow support when Codex
claims, resumes, or inspects plans.

Canonical editable source:

- `workflow/codex-control/plugin/source/scripts/`
- `workflow/codex-control/plugin/source/usage-errors/`

The temporary `source/` shadow copy has been removed. Edit the staged
`plugin/source/` tree directly.
