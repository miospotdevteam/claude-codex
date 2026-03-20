# Orchestration

`orchestration/` is the integration layer for the combined Claude Code x Codex
system.

It should hold:

- end-to-end explanations
- smoke tests
- example prompts
- rollout notes
- integration validation
- canonical integration-owned source files such as worker/verifier scripts and
  orchestration agent definitions

It should not be the source of truth for the routing matrix or ownership
contract. Those live in `workflow/core/contracts/`.
