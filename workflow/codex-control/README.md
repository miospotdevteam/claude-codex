# Codex Control

`workflow/codex-control/` is the future Codex-specific adapter layer.

Its job is to consume the shared ownership contract as Codex-native worker and
verifier behavior without inheriting Claude-only runtime assumptions.

This layer should own:

- Codex-specific prompts
- worker/verifier control surfaces
- install surfaces and wrapper assumptions
- future mapping from the shared routing contract into Codex-native guidance
- session-aware plan ownership and resume behavior for parallel same-repo
  workflows

The canonical contract still lives in `workflow/core/contracts/`.

Key adapter surfaces:

- `skills/pack/shared-contract-adapter.md`
- `wrappers/runtime/shared-contract-boundary.md`
- `plugin/package/boundary-map.md`
