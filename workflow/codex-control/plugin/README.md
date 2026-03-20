# Codex Plugin

This directory is the future landing zone for the Codex-global installable
package, skill bundle, or distribution tree.

Current staged source:

- `workflow/codex-control/plugin/source/`

It should eventually consume:

- shared contracts from `workflow/core/`
- Codex-specific skills from `workflow/codex-control/skills/`
- Codex-specific wrappers from `workflow/codex-control/wrappers/`

This is distinct from `orchestration/`, which owns the integrated end-to-end
system examples and compatibility surfaces.

Package-shaping docs now live in:

- `workflow/codex-control/plugin/package/README.md`
- `workflow/codex-control/plugin/package/boundary-map.md`
