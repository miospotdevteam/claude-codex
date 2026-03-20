#!/usr/bin/env python3
"""Generate normalized dependency maps via madge + dynamic import scanning.

Usage:
    python3 deps-generate.py <project_root> --module apps/api
    python3 deps-generate.py <project_root> --all
    python3 deps-generate.py <project_root> --stale-only

Configuration lives in .codex/lbyl-deps.json:
{
  "dep_maps": {
    "dir": ".codex/deps",
    "tool_cmd": "madge --json --extensions ts,tsx",
    "modules": ["apps/api", "packages/shared"]
  }
}

Runs madge per module for static imports, then scans for dynamic imports
(import(), React.lazy, next/dynamic, etc.), normalizes all paths to
repo-relative, and writes to .codex/deps/deps-{slug}.json.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from typing import Any

CONFIG_PATH = os.path.join(".codex", "lbyl-deps.json")


def read_config(project_root: str) -> dict[str, Any]:
    config_file = os.path.join(project_root, CONFIG_PATH)
    try:
        with open(config_file, encoding="utf-8") as handle:
            return json.load(handle)
    except (FileNotFoundError, PermissionError, json.JSONDecodeError):
        return {}


def module_slug(module_path: str) -> str:
    return module_path.replace("/", "-")


def get_deps_dir(project_root: str, config: dict[str, Any]) -> str:
    dep_maps = config.get("dep_maps", {})
    rel_dir = dep_maps.get("dir", ".codex/deps")
    return os.path.join(project_root, rel_dir)


def get_stale_modules(deps_dir: str) -> set[str]:
    stale_file = os.path.join(deps_dir, ".stale")
    if not os.path.exists(stale_file):
        return set()
    try:
        with open(stale_file, encoding="utf-8") as handle:
            return {line.strip() for line in handle if line.strip()}
    except (FileNotFoundError, PermissionError):
        return set()


def clear_stale(deps_dir: str, slug: str) -> None:
    stale_file = os.path.join(deps_dir, ".stale")
    if not os.path.exists(stale_file):
        return
    try:
        with open(stale_file, encoding="utf-8") as handle:
            lines = [line.strip() for line in handle if line.strip()]
        remaining = [line for line in lines if line != slug]
        with open(stale_file, "w", encoding="utf-8") as handle:
            handle.write("\n".join(remaining) + ("\n" if remaining else ""))
    except (FileNotFoundError, PermissionError):
        pass


def is_stale_by_mtime(project_root: str, deps_dir: str, module_path: str) -> bool:
    slug = module_slug(module_path)
    dep_file = os.path.join(deps_dir, f"deps-{slug}.json")
    if not os.path.exists(dep_file):
        return True

    dep_mtime = os.path.getmtime(dep_file)
    src_dir = os.path.join(project_root, module_path, "src")
    if not os.path.isdir(src_dir):
        src_dir = os.path.join(project_root, module_path)

    for root, _dirs, files in os.walk(src_dir):
        if "node_modules" in root:
            continue
        for filename in files:
            if filename.endswith((".ts", ".tsx")) and not filename.endswith(
                (".test.ts", ".test.tsx", ".spec.ts", ".spec.tsx")
            ):
                file_path = os.path.join(root, filename)
                if os.path.getmtime(file_path) > dep_mtime:
                    return True
    return False


def run_madge(project_root: str, module_path: str, tool_cmd: str) -> dict[str, list[str]] | None:
    module_abs = os.path.join(project_root, module_path)
    src_dir = os.path.join(module_abs, "src")
    if not os.path.isdir(src_dir):
        src_dir = module_abs

    tsconfig = os.path.join(module_abs, "tsconfig.json")

    cmd = tool_cmd.split()
    if os.path.exists(tsconfig):
        cmd.extend(["--ts-config", tsconfig])
    cmd.append(src_dir)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=project_root,
            timeout=120,
            check=False,
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
        pass

    npx_cmd = ["npx", "--yes"] + cmd
    try:
        result = subprocess.run(
            npx_cmd,
            capture_output=True,
            text=True,
            cwd=project_root,
            timeout=180,
            check=False,
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        print(f"  madge stderr: {result.stderr[:500]}", file=sys.stderr)
        return None
    except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        print(f"  madge failed: {exc}", file=sys.stderr)
        return None


def normalize_paths(
    raw_deps: dict[str, list[str]],
    project_root: str,
    module_path: str,
) -> dict[str, list[str]]:
    module_abs = os.path.join(project_root, module_path)
    src_dir = os.path.join(module_abs, "src")
    if not os.path.isdir(src_dir):
        src_dir = module_abs

    normalized: dict[str, list[str]] = {}
    for file_key, deps in raw_deps.items():
        abs_key = os.path.normpath(os.path.join(src_dir, file_key))
        repo_key = os.path.relpath(abs_key, project_root)

        repo_deps = []
        for dep in deps:
            abs_dep = os.path.normpath(os.path.join(src_dir, dep))
            repo_dep = os.path.relpath(abs_dep, project_root)
            if not repo_dep.startswith(".."):
                repo_deps.append(repo_dep)

        normalized[repo_key] = repo_deps

    return normalized


def read_tsconfig_paths(project_root: str, module_path: str) -> tuple[dict[str, list[str]], str | None]:
    """Read compilerOptions.paths and baseUrl from tsconfig.json."""
    module_abs = os.path.join(project_root, module_path)
    tsconfig_path = os.path.join(module_abs, "tsconfig.json")
    if not os.path.exists(tsconfig_path):
        return {}, None

    try:
        with open(tsconfig_path, encoding="utf-8") as handle:
            content = handle.read()
    except (FileNotFoundError, PermissionError):
        return {}, None

    content = re.sub(r"//.*?$", "", content, flags=re.MULTILINE)
    content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)
    try:
        tsconfig = json.loads(content)
    except json.JSONDecodeError:
        return {}, None

    compiler_opts = tsconfig.get("compilerOptions", {})
    paths = compiler_opts.get("paths", {})
    base_url = compiler_opts.get("baseUrl")

    if not paths and "extends" in tsconfig:
        extends_path = tsconfig["extends"]
        if not os.path.isabs(extends_path):
            extends_path = os.path.normpath(os.path.join(module_abs, extends_path))
        if not extends_path.endswith(".json"):
            extends_path += ".json"
        if os.path.exists(extends_path):
            try:
                with open(extends_path, encoding="utf-8") as handle:
                    content = handle.read()
            except (FileNotFoundError, PermissionError):
                content = ""
            if content:
                content = re.sub(r"//.*?$", "", content, flags=re.MULTILINE)
                content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)
                try:
                    base_config = json.loads(content)
                except json.JSONDecodeError:
                    base_config = {}
                base_opts = base_config.get("compilerOptions", {})
                paths = paths or base_opts.get("paths", {})
                base_url = base_url or base_opts.get("baseUrl")

    normalized_paths: dict[str, list[str]] = {}
    if isinstance(paths, dict):
        for pattern, targets in paths.items():
            if isinstance(pattern, str) and isinstance(targets, list):
                normalized_paths[pattern] = [target for target in targets if isinstance(target, str)]

    return normalized_paths, base_url if isinstance(base_url, str) else None


_EXTENSIONS = [".ts", ".tsx", ".js", ".jsx"]
_INDEX_FILES = ["/index.ts", "/index.tsx", "/index.js", "/index.jsx"]


def _probe_path(candidate: str) -> str | None:
    candidate = os.path.normpath(candidate)

    if os.path.isfile(candidate):
        return candidate

    for extension in _EXTENSIONS:
        path = candidate + extension
        if os.path.isfile(path):
            return path

    for index_file in _INDEX_FILES:
        path = candidate + index_file
        if os.path.isfile(path):
            return path

    return None


def _resolve_alias(
    specifier: str,
    tsconfig_paths: dict[str, list[str]],
    module_abs: str,
    base_url: str | None,
) -> str | None:
    base_dir = module_abs
    if base_url:
        base_dir = os.path.normpath(os.path.join(module_abs, base_url))

    for pattern, targets in tsconfig_paths.items():
        if not targets:
            continue

        if pattern.endswith("/*"):
            prefix = pattern[:-2]
            if specifier.startswith(prefix + "/"):
                remainder = specifier[len(prefix) + 1:]
                for target in targets:
                    if target.endswith("/*"):
                        target_base = target[:-2]
                        abs_target = os.path.normpath(os.path.join(base_dir, target_base, remainder))
                        result = _probe_path(abs_target)
                        if result:
                            return result
        elif pattern == specifier:
            for target in targets:
                abs_target = os.path.normpath(os.path.join(base_dir, target))
                result = _probe_path(abs_target)
                if result:
                    return result

    return None


def resolve_import_path(
    specifier: str,
    importing_file: str,
    project_root: str,
    module_path: str,
    tsconfig_paths: dict[str, list[str]],
    base_url: str | None,
) -> str | None:
    """Resolve a dynamic import specifier to a repo-relative path."""
    module_abs = os.path.join(project_root, module_path)
    importing_abs = os.path.join(project_root, importing_file)
    importing_dir = os.path.dirname(importing_abs)

    resolved_abs = None

    if specifier.startswith("."):
        resolved_abs = _probe_path(os.path.join(importing_dir, specifier))
    elif tsconfig_paths:
        resolved_abs = _resolve_alias(specifier, tsconfig_paths, module_abs, base_url)
        if resolved_abs is None and base_url:
            base_abs = os.path.normpath(os.path.join(module_abs, base_url))
            resolved_abs = _probe_path(os.path.join(base_abs, specifier))
    elif base_url:
        base_abs = os.path.normpath(os.path.join(module_abs, base_url))
        resolved_abs = _probe_path(os.path.join(base_abs, specifier))

    if resolved_abs is None:
        return None

    repo_rel = os.path.relpath(resolved_abs, project_root)
    if repo_rel.startswith(".."):
        return None
    return repo_rel


_DYNAMIC_IMPORT_RE = re.compile(r"""import\s*\(\s*['"]([^'"]+)['"]\s*\)""")


def scan_dynamic_imports(
    project_root: str,
    module_path: str,
    existing_deps: dict[str, list[str]],
) -> dict[str, list[str]]:
    """Scan source files for dynamic import() patterns."""
    module_abs = os.path.join(project_root, module_path)
    src_dir = os.path.join(module_abs, "src")
    if not os.path.isdir(src_dir):
        src_dir = module_abs

    tsconfig_paths, base_url = read_tsconfig_paths(project_root, module_path)
    additional: dict[str, list[str]] = {}
    dynamic_count = 0

    for root, _dirs, files in os.walk(src_dir):
        if "node_modules" in root:
            continue
        for filename in files:
            if not filename.endswith((".ts", ".tsx")):
                continue
            if filename.endswith((".test.ts", ".test.tsx", ".spec.ts", ".spec.tsx")):
                continue

            file_path = os.path.join(root, filename)
            repo_rel = os.path.relpath(file_path, project_root)

            try:
                with open(file_path, encoding="utf-8") as handle:
                    content = handle.read()
            except (FileNotFoundError, PermissionError, UnicodeDecodeError):
                continue

            matches = _DYNAMIC_IMPORT_RE.findall(content)
            if not matches:
                continue

            existing_for_file = set(existing_deps.get(repo_rel, []))
            new_deps: list[str] = []

            for specifier in matches:
                resolved = resolve_import_path(
                    specifier,
                    repo_rel,
                    project_root,
                    module_path,
                    tsconfig_paths,
                    base_url,
                )
                if resolved and resolved != repo_rel and resolved not in existing_for_file:
                    new_deps.append(resolved)
                    existing_for_file.add(resolved)

            if new_deps:
                additional[repo_rel] = new_deps
                dynamic_count += len(new_deps)

    if dynamic_count:
        print(f"  dynamic imports: found {dynamic_count} additional edge(s)", file=sys.stderr)

    return additional


def generate_module(project_root: str, module_path: str, config: dict[str, Any]) -> bool:
    dep_maps = config.get("dep_maps", {})
    tool_cmd = dep_maps.get("tool_cmd", "madge --json --extensions ts,tsx")
    deps_dir = get_deps_dir(project_root, config)
    slug = module_slug(module_path)

    os.makedirs(deps_dir, exist_ok=True)

    print(f"Generating deps for {module_path}...", file=sys.stderr)
    raw = run_madge(project_root, module_path, tool_cmd)
    if raw is None:
        print(f"  FAILED: could not run madge for {module_path}", file=sys.stderr)
        return False

    normalized = normalize_paths(raw, project_root, module_path)
    dynamic_edges = scan_dynamic_imports(project_root, module_path, normalized)
    for file_key, new_deps in dynamic_edges.items():
        if file_key in normalized:
            existing = set(normalized[file_key])
            normalized[file_key] = sorted(existing | set(new_deps))
        else:
            normalized[file_key] = sorted(new_deps)

    out_path = os.path.join(deps_dir, f"deps-{slug}.json")
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(normalized, handle, indent=2, sort_keys=True)

    clear_stale(deps_dir, slug)
    print(f"  OK: {len(normalized)} files -> {out_path}", file=sys.stderr)
    return True


def main() -> None:
    if len(sys.argv) < 3:
        print(
            "Usage: deps-generate.py <project_root> (--module <path> | --all | --stale-only)",
            file=sys.stderr,
        )
        sys.exit(1)

    project_root = os.path.abspath(sys.argv[1])
    config = read_config(project_root)
    dep_maps = config.get("dep_maps", {})
    modules = dep_maps.get("modules", [])

    if not modules:
        print(f"No dep_maps.modules configured in {CONFIG_PATH}", file=sys.stderr)
        sys.exit(1)

    mode = sys.argv[2]

    if mode == "--module":
        if len(sys.argv) < 4:
            print("--module requires a module path", file=sys.stderr)
            sys.exit(1)
        target = sys.argv[3]
        if target not in modules:
            print(f"Module '{target}' not in configured modules: {modules}", file=sys.stderr)
            sys.exit(1)
        success = generate_module(project_root, target, config)
        sys.exit(0 if success else 1)

    if mode == "--all":
        failed = [module for module in modules if not generate_module(project_root, module, config)]
        if failed:
            print(f"\nFailed modules: {failed}", file=sys.stderr)
            sys.exit(1)
        print(f"\nAll {len(modules)} modules generated successfully.", file=sys.stderr)
        return

    if mode == "--stale-only":
        deps_dir = get_deps_dir(project_root, config)
        stale_slugs = get_stale_modules(deps_dir)
        generated = 0
        for module in modules:
            slug = module_slug(module)
            if slug in stale_slugs or is_stale_by_mtime(project_root, deps_dir, module):
                generate_module(project_root, module, config)
                generated += 1
        if generated == 0:
            print("All dep maps are up to date.", file=sys.stderr)
        else:
            print(f"Regenerated {generated} stale module(s).", file=sys.stderr)
        return

    print(f"Unknown mode: {mode}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
