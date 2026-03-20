# Smoke Tests

These are the first integration checks the orchestration layer should support.

## Package-Layer Smoke Test

After the staged plugin/package boundaries are shaped:

- Claude package surfaces under `workflow/claude-control/plugin/`
- Codex package surfaces under `workflow/codex-control/plugin/`

Expected result:

- both package layers can be reasoned about and validated without depending on
  the old global repos as hidden source-of-truth

## Routing Smoke Test

Give Claude a task that should clearly stay local:

- vague planning request
- frontend/UI request
- MCP/external-tool request

Expected result:

- Claude keeps ownership and does not delegate the wrong slice to Codex

## Worker Smoke Test

Give Claude a bounded backend or file-creation task with explicit requirements.

Expected result:

- Claude delegates through the Codex worker flow
- Codex performs the implementation
- Claude reports the worker result clearly

## Verifier Smoke Test

After meaningful work, require a Codex verification pass.

Expected result:

- Claude triggers the verifier automatically
- Codex reports `PASS` or `FAIL`
- Claude uses the result rather than ignoring it

## High-Risk Dual-Pass Smoke Test

Use a security-sensitive or high-blast-radius planning task.

Expected result:

- Claude performs primary discovery and synthesis
- Codex performs an adversarial challenge pass
- Claude writes the canonical final plan
