# plan.json Schema

The execution source of truth for every plan. Claude and its runtime hooks read
and update this file to track progress. `masterPlan.md` is the human-facing
proposal document and does not contain execution state.

## Location

```text
.temp/plan-mode/active/<plan-name>/plan.json
```

Parallel same-repo workflows are supported. Session ownership should be tracked
by Claude runtime metadata such as lock files or equivalent sidecars, not by
changing the meaning of `plan.json`.

## Full Schema

```json
{
  "name": "plan-name-kebab-case",
  "title": "Descriptive Title",
  "context": "What the user asked for — enough for a fresh context window to understand the task without the original conversation.",
  "status": "active",
  "requiredSkills": ["look-before-you-leap:frontend-design"],
  "disciplines": ["testing-checklist.md", "security-checklist.md"],
  "discovery": {
    "scope": "Files/directories in scope. Be explicit about boundaries.",
    "entryPoints": "Primary files to modify and their current state.",
    "consumers": "Who imports/uses the files you're changing. Include file paths.",
    "existingPatterns": "How similar problems are already solved in this codebase.",
    "testInfrastructure": "Test framework, where tests live, how to run them.",
    "conventions": "Project-specific conventions from CLAUDE.md or observed patterns.",
    "blastRadius": "What could break if you get this wrong.",
    "confidence": "high"
  },
  "steps": [
    {
      "id": 1,
      "title": "Step title",
      "status": "pending",
      "agent": "claude",
      "skill": "none",
      "simplify": false,
      "qa": false,
      "files": ["src/foo.ts", "src/bar.ts"],
      "description": "What needs to happen. Specific enough for a fresh context window.",
      "acceptanceCriteria": "Concrete, verifiable conditions (for example, 'tsc --noEmit passes').",
      "progress": [
        {"task": "Sub-task description", "status": "pending", "files": ["src/foo.ts"]},
        {"task": "Another sub-task", "status": "pending", "files": ["src/bar.ts"]}
      ],
      "subPlan": null,
      "result": null
    }
  ],
  "blocked": [],
  "completedSummary": [],
  "deviations": []
}
```

## Field Reference

### Top-level fields

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | yes | kebab-case plan name matching the directory name |
| `title` | string | yes | Human-readable title |
| `context` | string | yes | Request context that survives compaction |
| `status` | string | yes | `"active"` or `"completed"` |
| `requiredSkills` | string[] | yes | Exact skill identifiers for Claude |
| `disciplines` | string[] | yes | Checklist filenames that apply |
| `discovery` | object | yes | All 8 exploration sections |
| `steps` | Step[] | yes | Ordered list of execution steps |
| `blocked` | string[] | yes | Blocked step descriptions |
| `completedSummary` | string[] | yes | Running log of completed steps |
| `deviations` | string[] | yes | Where execution diverged from the approved baseline in `masterPlan.md` |

### Step fields

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | number | yes | Sequential step number (1-based) |
| `title` | string | yes | Step title |
| `status` | string | yes | One of: `pending`, `in_progress`, `done`, `blocked` |
| `agent` | string | yes | Who executes: `"claude"`, `"codex-worker"`, or `"codex-verifier"` |
| `skill` | string | yes | Skill to invoke, or `"none"` |
| `simplify` | boolean | yes | Whether to run simplification after the step |
| `qa` | boolean | no | Whether to run an extra fresh-eyes verification pass after the step |
| `files` | string[] | yes | Files involved in the step |
| `description` | string | yes | Self-contained execution description |
| `acceptanceCriteria` | string | yes | How to know the step is complete |
| `progress` | Progress[] | yes | Sub-task checklist |
| `subPlan` | SubPlan? | no | Inline sub-plan for large steps |
| `result` | string? | no | Filled after completion |

### Progress item fields

| Field | Type | Required | Description |
|---|---|---|---|
| `task` | string | yes | Sub-task description |
| `status` | string | yes | One of: `pending`, `in_progress`, `done` |
| `files` | string[] | no | Files involved in this sub-task |

### SubPlan fields

| Field | Type | Required | Description |
|---|---|---|---|
| `groups` | Group[] | yes | Ordered list of file groups |

### Group fields

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | yes | Logical cluster name |
| `files` | string[] | yes | Files in the group |
| `status` | string | yes | One of: `pending`, `in_progress`, `done` |
| `notes` | string? | no | Execution notes |

## Agent Values

Each step declares which model executes it. This makes routing explicit in
the plan so reviewers know what runs where:

| Value | When to use |
|---|---|
| `"claude"` | Planning, architecture, UI/frontend work, MCP-dependent tasks, ambiguous scope, integration. Default for most steps. |
| `"codex-worker"` | Large refactors, code generation from a clear spec, isolated bug fixes, repetitive sweeps, well-scoped backend work. Requires a self-contained description — Codex has no conversation context. |
| `"codex-verifier"` | Independent verification after significant work, bug root cause analysis. Reports findings only — does not implement fixes. |

**Routing rules:**
- Steps with `skill` values (TDD, frontend-design, etc.) should almost always be `"claude"` — skills require conversation context.
- Steps that are pure implementation with a clear spec → `"codex-worker"`.
- The final verification step of any plan → `"codex-verifier"`.
- When unsure, default to `"claude"`.

## Status Values

Steps, progress items, and groups all use the same status values:

| Value | Meaning |
|---|---|
| `pending` | Not yet started |
| `in_progress` | Currently being worked on |
| `done` | Complete and verified |
| `blocked` | Cannot proceed (steps only) |

## Updating plan.json

Claude may use hooks, helper utilities, or Bash-driven `python3` calls into
`plan_utils.py` to update `plan.json`. The mechanism can vary, but the
semantics do not:

- one execution source of truth
- deterministic status updates
- completed summaries appended as work finishes
- deviations recorded when execution leaves the approved baseline
- session ownership tracked outside `plan.json` when parallel workflows are in play

Example commands:

```bash
python3 /path/to/plan_utils.py update-step /path/to/plan.json 3 in_progress
python3 /path/to/plan_utils.py update-progress /path/to/plan.json 3 0 done
python3 /path/to/plan_utils.py add-summary /path/to/plan.json "Step 3: Migrated all hooks to JSON parsing"
python3 /path/to/plan_utils.py status /path/to/plan.json
python3 /path/to/plan_utils.py next-step /path/to/plan.json
```

## masterPlan.md Companion Rules

`masterPlan.md` lives alongside `plan.json` in the same directory.

Its purpose:

- present the plan for review
- summarize intent, critical decisions, warnings, and risks
- freeze the approved baseline for later comparison

All runtime state lives exclusively in `plan.json`.

After approval, `plan.json` may absorb non-material follow-through that stays
within the same approved objective. Examples include mirrored fixes, adjacent
consistency updates, extra verification, and small cleanup/docs/tests needed to
finish the approved work correctly. If scope, risk, or tradeoffs change
materially, revise the plan and get fresh approval.
