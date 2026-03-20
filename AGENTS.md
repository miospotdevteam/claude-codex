# Claude Code x Codex Bootstrap

## Scope

- This repository defines a local Claude Code x Codex orchestration scaffold.
- Keep the implementation focused on repo guidance, Claude subagents, and
  small helper scripts.
- Do not invent application code, CI pipelines, or MCP integrations unless
  the repo grows to require them.

## Commands

- Verify Codex subscription login: `codex login status`
- Start Codex login flow if needed: `codex login`
- Check Claude CLI availability: `claude --help`
- Validate shell scripts: `bash -n scripts/codex-preflight.sh scripts/codex-worker.sh scripts/codex-verifier.sh`

## Conventions

- Prefer ChatGPT subscription sign-in for Codex. Do not require
  `OPENAI_API_KEY` for normal local use.
- Keep `workflow/core/contracts/`, `README.md`, `CLAUDE.md`,
  `orchestration/`, and `scripts/` aligned.
- `workflow/core/contracts/agent-ownership.md` and
  `workflow/core/contracts/routing-matrix.md` are the canonical ownership and
  routing sources of truth.
- `README.md` is the high-level repo map, not the sole source of truth.
- `orchestration/scripts/` are the canonical orchestration-owned sources.
  Root `scripts/` are compatibility wrappers and should stay thin.
- Codex is called directly via shell scripts (`codex-worker.sh`,
  `codex-verifier.sh`), not through agent `.md` wrappers. Claude builds the
  prompt and calls the script via Bash.
- If the repo is not a git repository, Codex wrappers must use
  `--skip-git-repo-check`.
- Use the helper scripts instead of ad hoc `codex exec` commands when the
  standard worker or verifier flow is enough. Prefer the root wrappers for
  convenience and `orchestration/scripts/` when editing the canonical source.

## Safety Rules

- Keep wrapper scripts small and transparent. They should standardize the
  workflow, not hide it.
- Treat API-key auth as an explicit fallback only when subscription auth is
  unavailable or exhausted.
