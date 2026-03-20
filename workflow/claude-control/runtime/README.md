# Runtime

This directory is the future landing zone for Claude-specific runtime and
installation surfaces.

Examples:

- hook wiring
- plugin manifests
- Claude-specific orchestration runtime defaults
- session-aware plan routing for parallel workflows

The runtime must enforce shared-core contracts without redefining them.

See:

- `workflow/claude-control/runtime/hooks/shared-contract-boundary.md`
- `workflow/claude-control/runtime/defaults/README.md`
