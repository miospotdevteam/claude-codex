# Parallel Workflows

The workflow system must support multiple concurrent workflows inside the same
repository.

This is a shared-core requirement, not a Claude-only feature.

## Core Rules

- Multiple active plan directories may coexist under `.temp/plan-mode/active/`.
- One workflow session owns one active plan at a time.
- A workflow should resume its own claimed plan before looking at unrelated
  active plans.
- Different workflows may explore in parallel, but they must not both own the
  same implementation slice at the same time.
- Read-only cross-session context sharing is allowed.
- Write ownership must stay explicit enough to avoid accidental plan or code
  stomping.

## Ownership Model

Plan ownership may be implemented with runtime sidecars such as lock files,
session claims, or another equivalent mechanism.

Shared-core requirements:

- ownership must be discoverable by the active runtime
- stale ownership must be recoverable
- unclaimed active plans must remain resumable
- one session must be able to read another session's discovery context without
  hijacking that session's plan

The exact mechanism is adapter-specific.

## Resume Semantics

Resume behavior should prefer:

1. the current session's claimed active plan
2. an explicitly targeted foreign plan for tangent or review work
3. an unclaimed active plan when the current session has none

It should not default to silently attaching one session to another session's
active plan unless the user or runtime explicitly asked for that.

## Parallel Safety Rules

- Separate workflows need separate plan directories.
- Shared-core artifacts must be immutable or append-only during execution.
- Runtime helpers may update `plan.json`, but only for the plan they own unless
  they are in an explicit cross-session read or admin flow.
- Cross-session context loading should be read-only by default.
- If two workflows need to edit the same code slice, orchestration must merge
  them into one owner or split the slice more cleanly.

## Why This Lives In Core

Claude already supports same-repo parallel workflows through session-aware plan
routing. Codex migration must preserve that capability rather than falling back
to a single active plan model.
