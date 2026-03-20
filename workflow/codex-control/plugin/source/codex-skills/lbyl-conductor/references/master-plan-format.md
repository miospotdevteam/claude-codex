# masterPlan.md Template

`masterPlan.md` is the user-facing proposal document reviewed via Orbit. It
communicates intent, critical decisions, warnings, and risk, not execution
state. Execution state lives in `plan.json`.

**Write-once**: `masterPlan.md` freezes after approval. It is never updated
during execution. All runtime state, progress, results, and deviations live in
`plan.json`.

No checkboxes. No progress tracking. No result fields.

---

```markdown
# Plan: <Descriptive Title>

> **For Codex:** REQUIRED SKILL: Use
> `lbyl-engineering-discipline` for all steps. Also invoke each
> step's `Skill` field when it is not `none`. See the Required Skills section
> for the full list.

## Context

<2-3 sentences: what the user asked for, what project this is, key
constraints. Write this so a fresh context window understands the task without
needing the original conversation.>

## Required Skills

<List any installed skills that should be invoked at specific steps. Use exact
skill identifiers for Codex. Format:

- **Step N**: `lbyl-frontend-design` (full mode)
- **Step M**: `lbyl-writing-plans` (plan generation)

If no external skills are needed, write "None — all work covered by core
disciplines.">

## Applicable Disciplines

<Which discipline checklists apply to this task. Format:

- **testing-checklist.md** — applies at Steps N, M
- **security-checklist.md** — applies at Step K
- **git-checklist.md** — applies at all commit points>

## Discovery Summary

<Structured findings from exploration. Complete all 8 sections.>

### Scope
<What files/directories are in scope. Be explicit about boundaries.>

### Entry Points
<The primary files to modify.>

### Consumers
<Who imports or uses the files you're changing.>

### Existing Patterns
<How similar problems are already solved in this codebase.>

### Test Infrastructure
<Testing framework, test location, how to run tests.>

### Conventions
<Project-specific conventions.>

### Blast Radius
<What could break. Consumer counts, shared types, public API surfaces.>

### Confidence Rating
<Low / Medium / High with justification.>

## Steps

### Step 1: <Title>
- **Skill**: `lbyl-refactoring` | none
- **Simplify**: true/false
- **Sub-plan**: none
- **Files involved**: `src/foo.ts`, `src/bar.ts`
- **Description**: What needs to happen in this step.
- **Acceptance criteria**: How to know this step is done.

### Step 2: <Title>
...

## Blocked Items

<List anything blocked, why, and what is needed to unblock. If nothing is
blocked, write "None.">

## Risk Areas

<Highlight areas where things could go wrong — consumer breakage, security
implications, performance concerns, areas requiring manual verification. If no
notable risks, write "None.">
```

---

## Naming Convention

Plan directories use kebab-case under `.temp/plan-mode/active/`.

When all steps are complete, the plan folder moves to `completed/`.

Parallel workflows are allowed, so multiple active plan directories may exist
at once. Ownership and resume selection are handled by Codex runtime metadata,
not by changing the meaning of `masterPlan.md`.

## Relationship to plan.json

`masterPlan.md` and `plan.json` are written together during planning. They
contain the same planned steps, but:

| Aspect | `plan.json` | `masterPlan.md` |
|---|---|---|
| Audience | Codex sessions | User / reviewer |
| Execution state | Yes | No |
| Updated during execution | Yes | Never |
| Review artifact | No | Yes |
| Parsed by tooling | Yes | Optional fallback only |

After approval, `plan.json` may include non-material follow-through in service
of the same approved objective. If the objective, risk profile, or tradeoffs
change materially, revise the plan instead of stretching the old one.
