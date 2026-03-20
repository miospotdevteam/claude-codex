# Tool Adapter Rules

`workflow/core/` owns semantics. Control layers own translation.

This file defines what Claude and Codex adapters are allowed to customize when
they consume shared-core contracts.

## Core Owns

These meanings must stay aligned between Claude and Codex:

- agent ownership and routing policy
- the eight-part discovery model
- the `plan.json` schema
- the `masterPlan.md` proposal shape
- the rule that `masterPlan.md` freezes after approval
- the rule that execution state lives in `plan.json`
- the allowance for non-material follow-through only inside the approved
  objective
- dependency-mapping semantics: use the strongest available graph source
  before estimating blast radius
- parallel same-repo workflow behavior

If one of those semantics changes, update `workflow/core/` first.

## Adapters May Customize

Control layers may translate only the runtime-specific parts:

- repo guidance file names such as `CLAUDE.md` vs `AGENTS.md`
- exact skill identifiers such as `look-before-you-leap:*` vs `lbyl-*`
- config file locations such as `.claude/...` vs `.codex/...`
- hook-based vs wrapper-based enforcement
- packaging, manifests, installers, and command surfaces
- user-experience wording that is specific to one tool
- how a session claims or resumes its own plan, as long as the shared
  parallel-workflow semantics stay intact

## Placeholder Policy

Shared-core docs may use generic placeholders when exact names differ by tool.
Adapters are responsible for binding those placeholders to concrete values.

Common examples:

- `<repo-guidance-file>`
- `<core-engineering-skill-id>`
- `<frontend-design-skill-id>`
- `<writing-plans-skill-id>`
- `<dep-query-command>`
- `<dep-config-path>`

## Adapter Constraint

Adapters may clarify, but they must not silently weaken the shared contract.

Examples of allowed adaptation:

- swapping `CLAUDE.md` for `AGENTS.md`
- swapping skill IDs to the local namespace
- swapping hook wording for wrapper wording
- using sidecar lock files instead of an inline ownership field

Examples of forbidden silent drift:

- reducing the required discovery questions from 8 to fewer
- changing `masterPlan.md` from write-once to mutable execution state
- dropping blast-radius analysis when dependency maps are configured
- changing ownership defaults without updating `agent-ownership.md`
- forcing a single active workflow per repo when shared core allows parallel
  workflows
