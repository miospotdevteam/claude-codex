# LBYL Setup

This repository tracks two related things:

- `codex-skills/`: the Codex port, adapted for Codex CLI and GPT-5.4
- the staged Claude source tree in the monorepo at
  `workflow/claude-control/plugin/source/look-before-you-leap/`

The goal is the same in both environments: make the model behave like a
disciplined engineer instead of a fast but sloppy one. The Codex port keeps
the shared Claude exploration, planning, verification, and blast-radius rules,
but
rewrites Claude-only concepts such as hook enforcement and plan mode into
Codex-native instructions, helper scripts, and Orbit-backed review flow.

## Why this exists

The discipline targets the recurring failure modes that show up in real coding
sessions:

- silent scope cuts
- shared-code changes without consumer checks
- type-safety shortcuts
- missing verification
- shallow exploration
- compaction without a recoverable plan

GPT-5.4 is stronger at following explicit long-horizon instructions than
earlier models, so the Codex version leans on clear contracts: exact skills,
exact plan files, exact acceptance criteria, and concise progress updates.

## Repository layout

```text
codex-skills/           Codex-native skill pack
scripts/                install helpers for Codex
```

## Install the repo skills

```bash
bash workflow/codex-control/plugin/source/scripts/install-codex-skills.sh
```

This installs the full Codex-native pack plus the shared Claude skills from:

- `codex-skills/`
- `workflow/claude-control/plugin/source/look-before-you-leap/skills/`

into `~/.codex/skills/`, except the Claude `frontend-design` skill. That
source stays in the repo for sync, but installed Codex sessions use
`lbyl-frontend-design` as the single standard frontend design skill.
`immersive-frontend` remains available for motion-heavy frontend work, and the
Claude-sourced skills such as `doc-coauthoring`, `mcp-builder`, `svg-art`, and
`webapp-testing` are installed directly from the staged Claude tree. The
`lbyl-*` skills remain the Codex-native defaults for coding work.

If a local Orbit repo is available at `~/Projects/orbit` or `~/projects/orbit`,
the installer also:

- builds the local Orbit MCP server when needed
- packages and installs the local VS Code extension when `code` is available
- registers a global Codex MCP server named `orbit`

That makes Orbit tools available automatically in future Codex sessions at
startup via `~/.codex/config.toml`.

To skip Orbit during a skill install:

```bash
SKIP_ORBIT_INSTALL=1 bash workflow/codex-control/plugin/source/scripts/install-codex-skills.sh
```

To bootstrap Orbit separately or point at a non-default checkout:

```bash
bash workflow/codex-control/plugin/source/scripts/install-orbit-codex-integration.sh
ORBIT_DIR=/absolute/path/to/orbit bash workflow/codex-control/plugin/source/scripts/install-orbit-codex-integration.sh
```

## Install from GitHub

For multi-machine use, treat GitHub as the source of truth and run the
bootstrap wrapper on each machine:

```bash
curl -fsSL https://raw.githubusercontent.com/miospotdevteam/claude-codex/main/workflow/codex-control/plugin/source/scripts/bootstrap-codex-skills-from-github.sh | bash
```

That script:

- clones `https://github.com/miospotdevteam/claude-codex.git` into
  `~/Projects/claude-codex` if it is missing
- otherwise validates the checkout and pulls the latest `main`
- runs `workflow/codex-control/plugin/source/scripts/install-codex-skills.sh`
  from that checkout

You can also run it from any existing checkout:

```bash
bash workflow/codex-control/plugin/source/scripts/bootstrap-codex-skills-from-github.sh
```

Useful overrides:

```bash
CHECKOUT_DIR=~/projects/claude-codex bash workflow/codex-control/plugin/source/scripts/bootstrap-codex-skills-from-github.sh
REPO_URL=https://github.com/<org>/claude-codex.git bash workflow/codex-control/plugin/source/scripts/bootstrap-codex-skills-from-github.sh
BRANCH=main bash workflow/codex-control/plugin/source/scripts/bootstrap-codex-skills-from-github.sh
SKIP_ORBIT_INSTALL=1 bash workflow/codex-control/plugin/source/scripts/bootstrap-codex-skills-from-github.sh
SKIP_PULL=1 bash workflow/codex-control/plugin/source/scripts/bootstrap-codex-skills-from-github.sh
```

This still installs into `~/.codex/skills/`, so future updates are not live.
After pushing changes to GitHub, rerun the bootstrap script on each machine to
pull and reinstall the latest version.

## Use in Codex

Mention the skills explicitly or rely on project `AGENTS.md` defaults.
Typical prompts:

- `Use lbyl-conductor and lbyl-engineering-discipline for this task.`
- `Use lbyl-writing-plans, then execute with lbyl-persistent-plans.`
- `Use lbyl-systematic-debugging for this failure.`
- `Use immersive-frontend for this motion-heavy landing page.`

For coding work, the expected default is:

- explore first
- write `.temp/plan-mode/active/<plan-name>/plan.json` and `masterPlan.md` before source edits
- update the plan every 2-3 file edits
- run relevant verification before declaring done

By default, the Codex skill pack presents new plans through Orbit for review
with `orbit_await_review` before execution starts unless the user explicitly
skips that review.

If a future session discovers that the skill pack itself caused a bad
workflow, missed requirement, or other usage error, log it back here under
`usage-errors/`. Preferred helper:

```bash
bash ~/Projects/codex-setup/scripts/log-usage-error.sh "short title"
```

If this repo lives elsewhere on that machine, set
`LBYL_CODEX_SETUP_REPO=/absolute/path/to/codex-setup` first. See
[`usage-errors/README.md`](/Users/robertobortolaso/Projects/codex-setup/usage-errors/README.md)
for the report format.

## Sync policy

When the Claude repo evolves:

1. sync the shared Claude source in
   `workflow/claude-control/plugin/source/look-before-you-leap/`
2. port the relevant changes into `codex-skills/`
3. adapt for Codex instead of copying Claude-specific runtime assumptions

That adaptation layer is the important part. This repo is intentionally not a
literal mirror.

Current examples of Claude-sourced skills that ship directly from the staged
Claude tree are `doc-coauthoring`, `mcp-builder`, `svg-art`, and
`webapp-testing`.
