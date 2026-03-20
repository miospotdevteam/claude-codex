# Claude Code Orchestrator Notes

## Role

- Claude Code is the default orchestrator in this repository.
- Claude handles planning, task routing, user communication, and integration.
- Codex is used as a delegated worker for well-scoped coding tasks and as the
  independent verification layer.

## Routing

- Keep planning, architecture, UI work, and MCP-dependent work in Claude.
- Delegate large refactors, code generation from a clear spec, bug
  investigation, and verification passes to Codex.
- When a task is mixed or ambiguous, Claude owns the integration and may
  delegate only the narrow backend or verification slice.

## Default Execution Flow

1. Clarify the task and collect the exact requirement text.
2. Build a self-contained prompt and call `scripts/codex-worker.sh` directly
   via Bash for implementation tasks that fit Codex. Write long prompts to a
   temp file and use `--prompt-file`. Always use `--output` for analysis tasks.
   The canonical implementation lives in `orchestration/scripts/codex-worker.sh`.
3. Review the resulting changes before integrating them.
4. Run `scripts/codex-verifier.sh --requirements-file <path>` before reporting
   completion on any significant work. The canonical implementation lives in
   `orchestration/scripts/codex-verifier.sh`.
5. If verification fails, fix the issues and re-run verification.

## Auth

- Prefer subscription auth for both tools.
- For Codex, use `codex login` and confirm with `codex login status`.
- Do not assume `OPENAI_API_KEY` is present.

## Repo Notes

- This repo may be used before `git init`; the Codex wrappers handle that by
  adding `--skip-git-repo-check` automatically.
- `workflow/core/contracts/agent-ownership.md` and
  `workflow/core/contracts/routing-matrix.md` are the canonical routing and
  ownership contracts.
- `README.md` is the high-level map for this repository. Keep it aligned with
  `AGENTS.md`, `workflow/`, `orchestration/`, and the helper scripts.
- `orchestration/scripts/` are the canonical orchestration-owned sources;
  root `scripts/` exist as compatibility wrappers.
