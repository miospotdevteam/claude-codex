# Claude Plugin

This directory is the future landing zone for the Claude-global installable
plugin package or package-like source tree.

Current staged source:

- `workflow/claude-control/plugin/source/`

It should eventually consume:

- shared contracts from `workflow/core/`
- Claude-specific runtime logic from `workflow/claude-control/runtime/`
- Claude-specific orchestration prompts from `workflow/claude-control/prompts/`

This is distinct from `orchestration/`, which owns the integrated end-to-end
system examples and compatibility surfaces.

Package-shaping docs now live in:

- `workflow/claude-control/plugin/package/README.md`
- `workflow/claude-control/plugin/package/boundary-map.md`
