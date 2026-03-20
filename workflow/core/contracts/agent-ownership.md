# Agent Ownership Contract

This file is the canonical ownership contract for the Claude Code x Codex
system.

## Principle

- Claude owns ambiguity.
- Codex owns constrained execution.
- Claude synthesizes.
- Codex attacks and verifies.
- One implementation slice gets one builder at a time.

## Phase Ownership

- Intent capture and context = 0: Claude
- Brainstorming and option comparison: Claude
- Initial scoping: Claude
- Standard discovery: Claude
- High-risk discovery challenge pass: Codex
- Discovery write-up: Claude
- Plan writing: Claude
- Plan review and adversarial critique: Codex
- Final go/no-go before execution: Claude
- Final user-facing summary: Claude

## Execution Ownership

- Frontend UI, visual design, interaction polish: Claude
- Product copy in UI: Claude
- Backend implementation from a clear spec: Codex
- API/service implementation with no external-tool dependency: Codex
- Large refactors and migrations: Codex
- Bug investigation and CI failure diagnosis: Codex
- Security review and adversarial check: Codex
- Security-sensitive design: Claude with Codex challenge pass
- MCP, DB, API, and external-tool-driven work: Claude
- Cross-domain integration: Claude
- Final verification after meaningful work: Codex

## Dual-Pass Triggers

Run both agents independently only when the cost is justified:

- security-sensitive change
- high-blast-radius refactor
- migration touching shared systems
- unclear production bug
- expensive-to-reverse architecture decision
- major plan review before execution

Default pattern:

1. Claude explores and frames
2. Codex independently challenges or verifies
3. Claude writes the canonical artifact
4. Codex reviews only when justified by risk
5. Claude decides and orchestrates execution

## Hard Boundaries

- Codex does not own user-facing ambiguity resolution.
- Claude should not be the only verifier of significant implementation.
- Claude and Codex should not edit the same implementation slice concurrently.
- Mixed tasks belong to Claude at the top level, with Codex receiving bounded sub-slices.

## Consumption Rules

- `workflow/claude-control/` must turn this contract into default Claude
  orchestration behavior.
- `workflow/codex-control/` must consume the same contract as guidance for
  worker/verifier behavior without inheriting Claude-only runtime assumptions.
- `orchestration/` may explain and exercise this contract, but must not become
  the source of truth for it.
