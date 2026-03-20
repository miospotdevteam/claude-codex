# Claude Control

`workflow/claude-control/` is the future Claude-specific adapter layer.

Its job is to make Claude Code follow the shared ownership contract by default
once the orchestration layer is installed globally.

This layer should own:

- Claude-specific prompts and instruction surfaces
- future hook/runtime integration for always-on orchestration behavior
- mappings from the shared routing contract into Claude execution defaults
- session-aware runtime behavior for parallel same-repo workflows

This layer should not own the canonical routing policy itself. That lives in
`workflow/core/contracts/`.

Key adapter surfaces:

- `prompts/global-orchestration/shared-contract-adapter.md`
- `runtime/hooks/shared-contract-boundary.md`
- `plugin/package/boundary-map.md`
