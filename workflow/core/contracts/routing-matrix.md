# Routing Matrix

This file is the canonical task-type routing table for the Claude Code x Codex
system.

| Task Type | Primary Owner | Secondary Reviewer | Default Trigger | Notes / Exceptions |
|---|---|---|---|---|
| Intent capture / vague ask / context = 0 | Claude | None | User goal is underspecified or ambiguous | Claude clarifies and shapes the task before any delegation |
| Brainstorming / option comparison | Claude | Codex for high-risk technical critique | Multiple plausible approaches with meaningful tradeoffs | Claude owns the final recommendation |
| Initial scoping | Claude | None | Need to translate user intent into concrete work areas | Keep this in Claude unless the codebase is highly unfamiliar |
| Discovery, standard | Claude | None | Normal feature, bug, or implementation prep | Do not dual-run by default |
| Discovery, high-risk | Claude | Codex | Security-sensitive, migration, large refactor, unclear production issue | Claude explores broadly; Codex does an adversarial challenge pass |
| Discovery write-up | Claude | Codex optional | Findings must become a durable artifact | Claude writes the canonical doc |
| Plan writing | Claude | Codex | Work is ready to be sequenced | Claude owns the canonical plan artifacts |
| Plan review / attack pass | Codex | Claude finalizes | Major execution is about to start | Codex looks for missing blast radius, weak assumptions, and hidden regressions |
| Frontend UI implementation | Claude | Codex verifier after completion | Visual components, layout, motion, UX polish | Default Claude territory |
| Product copy in UI | Claude | None | UX text, CTA wording, tone | Codex may review consistency only |
| Backend implementation from clear spec | Codex | Claude integrates | Bounded backend slice with clear requirements | Strong Codex default |
| API route / service implementation | Codex | Claude if external-tool reasoning is needed | Standard backend task | Claude may need to own when live service reasoning is central |
| Refactor across many files | Codex | Claude reviews integration impact | Multi-file rename, API migration, extraction, restructuring | Strong Codex default |
| Framework / library migration | Codex | Claude reviews architecture fit | Clear migration target with broad mechanical changes | Split ownership if UX decisions are involved |
| Bug investigation / root cause analysis | Codex | Claude if external tools or product context are needed | Failing tests, runtime errors, unclear regressions | Codex is first responder |
| CI failure diagnosis | Codex | Claude if fix crosses into design/UI/external systems | Failing checks with concrete evidence | Good Codex default |
| Security review / adversarial check | Codex | Claude synthesizes severity and action plan | Auth, secrets, trust boundaries, validation, risky changes | Dual-pass is justified |
| Security-sensitive design | Claude | Codex challenge pass | Auth architecture, permission model, data exposure | Claude owns the design decision |
| MCP / DB / API / external integration work | Claude | Codex verifier after | Needs external tools, live inspection, or service-specific reasoning | Keep with Claude |
| Integration across frontend + backend + tools | Claude | Codex verifier after | Mixed-domain work spanning multiple surfaces | Claude owns overall orchestration |
| Code review / PR review | Codex | Claude summarizes for user if needed | User asks for review or post-change audit | Codex should be adversarial |
| Verification after significant work | Codex | Claude fixes and reruns if needed | Any meaningful feature, refactor, migration, or bug fix | Standard default |
| Final user-facing summary | Claude | None | Need to report outcome, tradeoffs, or next steps | Always Claude |

## Default Rules

- If the task needs ambiguity handling, product judgment, UX taste, or external-tool reasoning, default to Claude.
- If the task needs precise execution, refactoring, debugging from evidence, or adversarial verification, default to Codex.
- One implementation slice gets one builder.
- Significant work should get a Codex verification pass before sign-off.
- Claude owns final user communication.
