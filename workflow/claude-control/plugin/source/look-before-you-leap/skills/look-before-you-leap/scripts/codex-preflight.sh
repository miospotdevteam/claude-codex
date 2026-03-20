#!/usr/bin/env bash
set -euo pipefail

resolve_repo_root() {
  if git rev-parse --show-toplevel >/dev/null 2>&1; then
    git rev-parse --show-toplevel
  else
    pwd -P
  fi
}

is_git_repo() {
  git rev-parse --show-toplevel >/dev/null 2>&1
}

require_command() {
  local name="$1"
  if ! command -v "$name" >/dev/null 2>&1; then
    printf 'Missing required command: %s\n' "$name" >&2
    exit 1
  fi
}

require_codex_auth() {
  if codex login status >/dev/null 2>&1; then
    return 0
  fi

  if [[ -n "${OPENAI_API_KEY:-}" ]]; then
    printf 'Codex subscription login is not active. OPENAI_API_KEY is set, so API-key fallback is available if you explicitly want it.\n' >&2
    return 0
  fi

  printf 'Codex is not authenticated.\n' >&2
  printf 'Run `codex login` and sign in with ChatGPT, then retry.\n' >&2
  exit 1
}

print_preflight_summary() {
  local repo_root="$1"
  if is_git_repo; then
    printf 'repo_root=%s\ngit_repo=yes\n' "$repo_root"
  else
    printf 'repo_root=%s\ngit_repo=no\n' "$repo_root"
  fi
}

main() {
  require_command codex
  require_codex_auth
  local repo_root
  repo_root="$(resolve_repo_root)"
  print_preflight_summary "$repo_root"
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  main "$@"
fi
