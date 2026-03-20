# Runtime Defaults

This directory is the future landing zone for Claude-specific default behavior
that must exist at install time but is not itself a shared-core contract.

Examples:

- default orchestration wording
- plugin-install defaults
- Claude-specific config fragments
- parallel-workflow session defaults

Any default placed here must reference shared-core contracts rather than
redefining ownership, routing, or planning semantics.

Canonical editable source:

- `workflow/claude-control/plugin/source/anthropic.md`
- other Claude-default surfaces inside
  `workflow/claude-control/plugin/source/`

The temporary `source/` shadow copy has been removed. Edit the staged
`plugin/source/` tree directly.
