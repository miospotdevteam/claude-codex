#!/usr/bin/env python3
"""Resolve template references from workflow/core/ into tool-specific output directories.

Usage:
    python3 workflow/scripts/resolve-refs.py          # resolve both
    python3 workflow/scripts/resolve-refs.py claude    # resolve claude only
    python3 workflow/scripts/resolve-refs.py codex     # resolve codex only
    python3 workflow/scripts/resolve-refs.py --check   # verify outputs match (for CI/pre-commit)
"""

import json
import os
import re
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CORE_DIR = REPO_ROOT / "workflow" / "core"
VARS_FILE = CORE_DIR / "resolve-vars.json"

# Source directories inside workflow/core/ that contain templates
SOURCE_DIRS = [
    CORE_DIR / "references",
    CORE_DIR / "checklists",
    CORE_DIR / "schemas",
]

OVERRIDES_DIR = CORE_DIR / "overrides"

# Output directories for each target
OUTPUT_DIRS = {
    "claude": REPO_ROOT / "workflow" / "claude-control" / "plugin" / "source"
              / "look-before-you-leap" / "skills" / "look-before-you-leap" / "references",
    "codex": REPO_ROOT / "workflow" / "codex-control" / "plugin" / "source"
             / "codex-skills" / "lbyl-conductor" / "references",
}

# ---------------------------------------------------------------------------
# Template resolution
# ---------------------------------------------------------------------------

def load_vars() -> dict:
    """Load the variable definitions from resolve-vars.json."""
    with open(VARS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve_conditionals(text: str, target: str) -> str:
    """Process conditional blocks: {{#target}}...{{/target}}.

    Keeps content for the matching target, strips it (including markers) for
    non-matching targets.
    """
    all_targets = ["claude", "codex"]
    for t in all_targets:
        pattern = re.compile(
            r"\{\{#" + re.escape(t) + r"\}\}\n?(.*?)\{\{/" + re.escape(t) + r"\}\}\n?",
            re.DOTALL,
        )
        if t == target:
            # Keep the inner content, remove the markers
            text = pattern.sub(r"\1", text)
        else:
            # Remove the entire block
            text = pattern.sub("", text)
    return text


def resolve_placeholders(text: str, variables: dict) -> str:
    """Replace {{VAR_NAME}} placeholders with their values."""
    def replacer(match):
        var_name = match.group(1)
        if var_name in variables:
            return variables[var_name]
        # Leave unrecognised placeholders intact (they may be literal template
        # examples in the document itself, e.g. inside code blocks)
        return match.group(0)

    return re.compile(r"\{\{([A-Z_]+)\}\}").sub(replacer, text)


def resolve_template(text: str, target: str, variables: dict) -> str:
    """Full template resolution: conditionals first, then placeholders."""
    text = resolve_conditionals(text, target)
    text = resolve_placeholders(text, variables)
    return text


# ---------------------------------------------------------------------------
# File operations
# ---------------------------------------------------------------------------

def collect_source_files() -> list[Path]:
    """Collect all .md files from the source directories (excluding READMEs)."""
    files = []
    for src_dir in SOURCE_DIRS:
        if not src_dir.is_dir():
            continue
        for p in sorted(src_dir.glob("*.md")):
            if p.name.lower() == "readme.md":
                continue
            files.append(p)
    return files


def collect_override_files(target: str) -> list[Path]:
    """Collect override files for a specific target."""
    override_dir = OVERRIDES_DIR / target
    if not override_dir.is_dir():
        return []
    return sorted(override_dir.glob("*.md"))


def write_if_changed(dest: Path, content: str) -> bool:
    """Write content to dest only if it differs from the current file.

    Returns True if the file was written (changed or new).
    """
    if dest.exists():
        existing = dest.read_text(encoding="utf-8")
        if existing == content:
            return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")
    return True


def copy_if_changed(src: Path, dest: Path) -> bool:
    """Copy src to dest only if they differ. Returns True if copied."""
    src_content = src.read_text(encoding="utf-8")
    return write_if_changed(dest, src_content)


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------

def resolve_target(target: str, variables: dict, check_only: bool = False) -> tuple[int, int, list[str]]:
    """Resolve all templates and overrides for a single target.

    Returns (updated_count, total_count, stale_files).
    """
    out_dir = OUTPUT_DIRS[target]
    updated = 0
    total = 0
    stale = []

    # 1. Process template files from source dirs
    for src_file in collect_source_files():
        total += 1
        template = src_file.read_text(encoding="utf-8")
        resolved = resolve_template(template, target, variables)
        dest = out_dir / src_file.name

        if check_only:
            if not dest.exists():
                stale.append(str(dest.relative_to(REPO_ROOT)))
            elif dest.read_text(encoding="utf-8") != resolved:
                stale.append(str(dest.relative_to(REPO_ROOT)))
        else:
            if write_if_changed(dest, resolved):
                updated += 1
                print(f"  updated: {dest.relative_to(REPO_ROOT)}")

    # 2. Copy override files
    for override_file in collect_override_files(target):
        total += 1
        dest = out_dir / override_file.name

        if check_only:
            override_content = override_file.read_text(encoding="utf-8")
            if not dest.exists():
                stale.append(str(dest.relative_to(REPO_ROOT)))
            elif dest.read_text(encoding="utf-8") != override_content:
                stale.append(str(dest.relative_to(REPO_ROOT)))
        else:
            if copy_if_changed(override_file, dest):
                updated += 1
                print(f"  updated: {dest.relative_to(REPO_ROOT)}")

    return updated, total, stale


def main():
    args = sys.argv[1:]

    check_only = "--check" in args
    args = [a for a in args if a != "--check"]

    if len(args) == 0:
        targets = ["claude", "codex"]
    elif len(args) == 1 and args[0] in ("claude", "codex"):
        targets = [args[0]]
    else:
        print(f"Usage: {sys.argv[0]} [claude|codex] [--check]", file=sys.stderr)
        sys.exit(2)

    all_vars = load_vars()
    all_stale = []
    total_updated = 0
    total_files = 0

    for target in targets:
        variables = all_vars[target]
        if not check_only:
            print(f"Resolving for {target}...")
        updated, total, stale = resolve_target(target, variables, check_only=check_only)
        total_updated += updated
        total_files += total
        all_stale.extend(stale)

    if check_only:
        if all_stale:
            print("Stale resolved references detected:")
            for f in all_stale:
                print(f"  {f}")
            print(f"\nRun 'make sync-refs' to update {len(all_stale)} file(s).")
            sys.exit(1)
        else:
            print(f"All {total_files} resolved references are up to date.")
            sys.exit(0)
    else:
        print(f"\nDone. {total_updated}/{total_files} file(s) updated.")


if __name__ == "__main__":
    main()
