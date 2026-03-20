#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
# shellcheck source=./codex-preflight.sh
source "${SCRIPT_DIR}/codex-preflight.sh"

usage() {
  cat <<'EOF'
Usage:
  orchestration/scripts/codex-worker.sh --prompt "..." [--output FILE] [--model MODEL] [--json] [--ephemeral]
  orchestration/scripts/codex-worker.sh --prompt-file FILE [--output FILE] [--model MODEL] [--json] [--ephemeral]

Options:
  --prompt TEXT        Inline prompt for Codex
  --prompt-file FILE   Read the prompt from a file
  --output FILE        Write Codex's final message to a file
  --model MODEL        Override the default Codex model
  --json               Print JSONL events to stdout
  --ephemeral          Do not persist the Codex session
  -h, --help           Show this help
EOF
}

prompt=""
prompt_file=""
output_file=""
model=""
json_mode=0
ephemeral=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --prompt)
      prompt="${2:-}"
      shift 2
      ;;
    --prompt-file)
      prompt_file="${2:-}"
      shift 2
      ;;
    --output)
      output_file="${2:-}"
      shift 2
      ;;
    --model)
      model="${2:-}"
      shift 2
      ;;
    --json)
      json_mode=1
      shift
      ;;
    --ephemeral)
      ephemeral=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown argument: %s\n\n' "$1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -n "$prompt" && -n "$prompt_file" ]]; then
  printf 'Use either --prompt or --prompt-file, not both.\n' >&2
  exit 1
fi

if [[ -z "$prompt" && -z "$prompt_file" ]]; then
  printf 'A prompt is required.\n\n' >&2
  usage >&2
  exit 1
fi

if [[ -n "$prompt_file" && ! -f "$prompt_file" ]]; then
  printf 'Prompt file not found: %s\n' "$prompt_file" >&2
  exit 1
fi

require_command codex
require_codex_auth

repo_root="$(resolve_repo_root)"
args=(exec --full-auto --cd "$repo_root")

if ! is_git_repo; then
  args+=(--skip-git-repo-check)
fi

if [[ -n "$output_file" ]]; then
  args+=(-o "$output_file")
fi

if [[ -n "$model" ]]; then
  args+=(--model "$model")
fi

if [[ "$json_mode" -eq 1 ]]; then
  args+=(--json)
fi

if [[ "$ephemeral" -eq 1 ]]; then
  args+=(--ephemeral)
fi

if [[ -n "$prompt_file" ]]; then
  codex "${args[@]}" - <"$prompt_file"
else
  codex "${args[@]}" "$prompt"
fi
