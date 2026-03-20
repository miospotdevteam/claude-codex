#!/usr/bin/env python3
"""Query dependency maps for a file's dependencies and dependents.

Usage:
    python3 deps-query.py <project_root> <file_path>
    python3 deps-query.py <project_root> <file_path> --json
    python3 deps-query.py <file_path> --project-root <project_root>
    python3 deps-query.py <file_path> --project-root <project_root> --json

Configuration is read via the Claude hook config reader from
.claude/look-before-you-leap.local.md. The command auto-regenerates stale
module dep maps before querying and scans all dep maps for cross-module
dependents.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import Any

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GENERATE_SCRIPT = os.path.join(SCRIPT_DIR, "deps-generate.py")
READ_CONFIG = os.path.join(SCRIPT_DIR, "..", "..", "..", "hooks", "lib", "read-config.py")
CONFIG_HINT = ".claude/look-before-you-leap.local.md"


def read_config(project_root: str) -> dict[str, Any]:
    try:
        result = subprocess.run(
            [sys.executable, READ_CONFIG, project_root],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
    except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
        pass
    return {}


def module_slug(module_path: str) -> str:
    return module_path.replace("/", "-")


def find_module_for_file(file_path: str, modules: list[str]) -> str | None:
    best = None
    for module in modules:
        if file_path.startswith(module + "/") or file_path == module:
            if best is None or len(module) > len(best):
                best = module
    return best


def regen_if_stale(project_root: str, module_path: str) -> None:
    try:
        subprocess.run(
            [sys.executable, GENERATE_SCRIPT, project_root, "--module", module_path],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass


def get_stale_modules(deps_dir: str) -> set[str]:
    stale_file = os.path.join(deps_dir, ".stale")
    if not os.path.exists(stale_file):
        return set()
    try:
        with open(stale_file, encoding="utf-8") as handle:
            return {line.strip() for line in handle if line.strip()}
    except (FileNotFoundError, PermissionError):
        return set()


def load_all_dep_maps(deps_dir: str) -> dict[str, dict[str, list[str]]]:
    maps: dict[str, dict[str, list[str]]] = {}
    if not os.path.isdir(deps_dir):
        return maps
    for filename in os.listdir(deps_dir):
        if filename.startswith("deps-") and filename.endswith(".json"):
            path = os.path.join(deps_dir, filename)
            try:
                with open(path, encoding="utf-8") as handle:
                    maps[filename] = json.load(handle)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
    return maps


def query_file(file_path: str, all_maps: dict[str, dict[str, list[str]]]) -> dict[str, Any]:
    dependencies: list[str] = []
    dependents: list[str] = []
    found_in_module = None

    for map_name, dep_map in all_maps.items():
        if file_path in dep_map:
            found_in_module = map_name
            dependencies = dep_map[file_path]

        for source, deps in dep_map.items():
            if file_path in deps:
                dependents.append(source)

    return {
        "file": file_path,
        "found_in": found_in_module,
        "dependencies": sorted(set(dependencies)),
        "dependents": sorted(set(dependents)),
    }


def format_human(result: dict[str, Any]) -> str:
    lines = [f"FILE: {result['file']}"]
    if result["found_in"]:
        module = (
            result["found_in"]
            .replace("deps-", "")
            .replace(".json", "")
            .replace("-", "/")
        )
        lines.append(f"MODULE: {module}")
    lines.append("")

    dependencies = result["dependencies"]
    lines.append(f"DEPENDENCIES ({len(dependencies)}):")
    if dependencies:
        lines.extend(f"  {dependency}" for dependency in dependencies)
    else:
        lines.append("  (none)")

    lines.append("")
    dependents = result["dependents"]
    lines.append(f"DEPENDENTS ({len(dependents)}):")
    if dependents:
        by_prefix: dict[str, list[str]] = {}
        for dependent in dependents:
            segments = dependent.split("/")
            prefix = "/".join(segments[:2]) if len(segments) > 1 else dependent
            by_prefix.setdefault(prefix, []).append(dependent)
        for prefix in sorted(by_prefix):
            lines.extend(f"  {dependent}" for dependent in by_prefix[prefix])
    else:
        lines.append("  (none)")

    lines.append("")
    lines.append(f"BLAST RADIUS: {len(dependents)} direct consumer(s)")
    if dependents:
        top_modules = {"/".join(path.split("/")[:2]) for path in dependents}
        lines.append(f"  Across {len(top_modules)} module(s): {', '.join(sorted(top_modules))}")

    return "\n".join(lines)


def parse_args(argv: list[str]) -> tuple[str, str, bool]:
    """Support both positional and --project-root invocation forms."""
    if len(argv) < 3:
        raise ValueError(
            "Usage: deps-query.py <project_root> <file_path> [--json] "
            "or deps-query.py <file_path> --project-root <project_root> [--json]"
        )

    args = argv[1:]
    json_mode = False
    filtered: list[str] = []
    i = 0
    while i < len(args):
        if args[i] == "--json":
            json_mode = True
            i += 1
            continue
        filtered.append(args[i])
        i += 1

    if "--project-root" in filtered:
        idx = filtered.index("--project-root")
        if idx == 0 or idx == len(filtered) - 1:
            raise ValueError("Error: --project-root requires both a file path and a project root")
        if len(filtered) != 3:
            raise ValueError("Error: expected exactly one file path plus --project-root <root>")
        file_path = filtered[0]
        project_root = filtered[idx + 1]
        return os.path.abspath(project_root), file_path, json_mode

    if len(filtered) != 2:
        raise ValueError(
            "Usage: deps-query.py <project_root> <file_path> [--json] "
            "or deps-query.py <file_path> --project-root <project_root> [--json]"
        )

    project_root = filtered[0]
    file_path = filtered[1]
    return os.path.abspath(project_root), file_path, json_mode


def main() -> None:
    try:
        project_root, raw_file_path, json_mode = parse_args(sys.argv)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)

    if os.path.isabs(raw_file_path):
        file_path = os.path.relpath(raw_file_path, project_root)
    else:
        file_path = raw_file_path

    config = read_config(project_root)
    dep_maps_config = config.get("dep_maps", {})
    modules = dep_maps_config.get("modules", [])

    if not modules:
        config_file = os.path.join(project_root, CONFIG_HINT)
        print(
            "Error: No dep_maps.modules configured. "
            f"Expected dep-map config at {config_file}",
            file=sys.stderr,
        )
        sys.exit(1)

    deps_dir_rel = dep_maps_config.get("dir", ".claude/deps")
    deps_dir = os.path.join(project_root, deps_dir_rel)

    stale_slugs = get_stale_modules(deps_dir)
    file_module = find_module_for_file(file_path, modules)

    if file_module:
        slug = module_slug(file_module)
        dep_file = os.path.join(deps_dir, f"deps-{slug}.json")
        if slug in stale_slugs or not os.path.exists(dep_file):
            print(f"Regenerating stale dep map for {file_module}...", file=sys.stderr)
            regen_if_stale(project_root, file_module)

    for module in modules:
        slug = module_slug(module)
        if slug in stale_slugs and module != file_module:
            print(f"Regenerating stale dep map for {module}...", file=sys.stderr)
            regen_if_stale(project_root, module)

    all_maps = load_all_dep_maps(deps_dir)
    if not all_maps:
        print("Error: No dep maps found. Run deps-generate.py --all first.", file=sys.stderr)
        sys.exit(1)

    result = query_file(file_path, all_maps)

    if json_mode:
        json.dump(result, sys.stdout, indent=2)
        print()
    else:
        print(format_human(result))


if __name__ == "__main__":
    main()
