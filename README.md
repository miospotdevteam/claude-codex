# Claude Code x Codex

This repository is now the transition workspace for a globally installed
two-agent orchestration system.

The target model is:

- shared workflow contracts in `workflow/core/`
- Claude-specific runtime/control behavior in `workflow/claude-control/`
- Codex-specific worker/verifier behavior in `workflow/codex-control/`
- integrated end-to-end behavior and examples in `orchestration/`

## Canonical Source Of Truth

The ownership contract does not live only in this root README anymore.

The canonical files are:

- `workflow/core/contracts/agent-ownership.md`
- `workflow/core/contracts/routing-matrix.md`

Those files define:

- who owns which phase
- who owns which task types
- when dual-pass review is justified
- what must stay shared versus tool-specific

`README.md` is now the high-level map for the repo.

## Repository Layout

```text
workflow/
  core/                  shared contracts, schemas, migration inventory
  claude-control/        Claude-specific control/runtime layer
  codex-control/         Codex-specific worker/verifier layer
orchestration/           integration docs, examples, smoke tests, rollout notes
scripts/                 root compatibility wrappers
```

## Current Ownership Model

At a high level:

- Claude owns ambiguity, planning, orchestration, UX, MCP/external-tool work,
  and final user communication.
- Codex owns constrained backend execution, refactors, debugging, adversarial
  review, and verification.

The detailed matrix lives in `workflow/core/contracts/routing-matrix.md`.

## Why This Repo Exists

You currently have two globally installed setup repos on this machine:

- `~/Projects/claude-code-setup`
- `~/Projects/codex-setup`

They overlap conceptually but differ correctly in runtime assumptions.
This repo is the staging area where the shared source of truth gets extracted
without forcing a premature merge of the two global systems.

## Control Layer Split

### `workflow/core/`

Owns shared contracts:

- agent ownership
- routing matrix
- shared migration inventory
- future shared schemas, checklists, and reusable fragments

### `workflow/claude-control/`

Owns Claude-specific behavior:

- always-on orchestration rules
- runtime integration into Claude Code
- future prompts/hooks/settings that make Claude follow the shared contract by default
- future installable plugin/package landing zone under `workflow/claude-control/plugin/`
- current staged copy of the existing Claude setup under `workflow/claude-control/plugin/source/`

### `workflow/codex-control/`

Owns Codex-specific behavior:

- worker/verifier consumption of the shared contract
- Codex-native prompts, wrappers, and install surfaces
- future migration from the current `codex-setup` layout
- future installable plugin/package landing zone under `workflow/codex-control/plugin/`
- current staged copy of the existing Codex setup under `workflow/codex-control/plugin/source/`

### `orchestration/`

Owns integration-level material:

- examples
- smoke tests
- end-to-end behavior notes
- rollout and adoption docs
- canonical orchestration scripts under `orchestration/scripts/`
- canonical orchestration agent definitions under `orchestration/agents/`

It is not the source of truth for ownership policy.

## Current Local Wrappers

The canonical implementations now live under `orchestration/scripts/`.

The root wrappers remain as compatibility entrypoints:

- `scripts/codex-preflight.sh`
- `scripts/codex-worker.sh`
- `scripts/codex-verifier.sh`

These delegate to the orchestration-owned sources so the repo remains directly
usable during the transition.

## Current Agent Definitions

The canonical orchestration agent definitions now live under:

- `orchestration/agents/codex-worker.md`
- `orchestration/agents/codex-verifier.md`

The root `.claude/agents/` files remain as compatibility mirrors for current
runtime discovery.

## Auth Model

Use subscription auth for both tools.

### Claude Code

- Requires an active Claude subscription

### Codex

- Prefer ChatGPT subscription sign-in
- Check status with `codex login status`
- Start login with `codex login`
- Treat `OPENAI_API_KEY` as an optional fallback only

## Quick Checks

These checks are currently expected to pass:

```bash
claude --help
codex login status
bash -n scripts/codex-preflight.sh scripts/codex-worker.sh scripts/codex-verifier.sh
scripts/codex-worker.sh --help
scripts/codex-verifier.sh --help
```
