#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
WORKER_SCRIPT="${SCRIPT_DIR}/codex-worker.sh"

usage() {
  cat <<'EOF'
Usage:
  orchestration/scripts/codex-verifier.sh --requirements-file FILE [--output FILE] [--model MODEL]

Options:
  --requirements-file FILE   Path to a file containing the original requirements
  --output FILE              Write Codex's final verifier message to a file
  --model MODEL              Override the default Codex model
  -h, --help                 Show this help
EOF
}

requirements_file=""
output_file=""
model=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --requirements-file)
      requirements_file="${2:-}"
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

if [[ -z "$requirements_file" ]]; then
  printf '--requirements-file is required.\n\n' >&2
  usage >&2
  exit 1
fi

if [[ ! -f "$requirements_file" ]]; then
  printf 'Requirements file not found: %s\n' "$requirements_file" >&2
  exit 1
fi

requirements="$(cat "$requirements_file")"
prompt_file="$(mktemp "${TMPDIR:-/tmp}/codex-verify.XXXXXX.txt")"
trap 'rm -f "$prompt_file"' EXIT

cat >"$prompt_file" <<EOF
You are a QA verifier.

Check the current state of the repository against these requirements:

$requirements

Verification steps:
1. Read the relevant source files and inspect the current working tree.
2. If tests exist, run the appropriate test commands and report failures.
3. Check for obvious regressions such as broken imports, missing exports, or requirement drift.
4. If this repository is in git, use git context when helpful. If it is not, continue without assuming git history exists.
5. Report missing edge cases or follow-up risks that would block sign-off.

Report format:
VERDICT: PASS | FAIL
ISSUES:
- <issue with file path and reason>
SUGGESTIONS:
- <optional non-blocking improvement>
EOF

args=(--prompt-file "$prompt_file")

if [[ -n "$output_file" ]]; then
  args+=(--output "$output_file")
fi

if [[ -n "$model" ]]; then
  args+=(--model "$model")
fi

"$WORKER_SCRIPT" "${args[@]}"
