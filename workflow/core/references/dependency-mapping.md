# Dependency Mapping

Instant dependency and consumer analysis using pre-generated module graphs.
This replaces ad-hoc grep for TypeScript import and consumer discovery when a
configured graph source exists.

---

## Core Rule

If dependency maps are configured for {{TOOL_NAME}}, use `deps-query.py` before
estimating consumer count or blast radius.

## Quick Start

```bash
# Query a file's dependencies and dependents (auto-regens if stale)
python3 {{SCRIPTS_PATH}}/deps-query.py <project_root> <file_path>

# Same, JSON output
python3 {{SCRIPTS_PATH}}/deps-query.py <project_root> <file_path> --json
```

The output should report:

- `DEPENDENCIES`: files the target imports
- `DEPENDENTS`: files that import or otherwise depend on the target
- `BLAST RADIUS`: count of direct consumers and the modules they live in

## Generation Commands

```bash
python3 {{SCRIPTS_PATH}}/deps-generate.py <project_root> --module apps/api
python3 {{SCRIPTS_PATH}}/deps-generate.py <project_root> --all
python3 {{SCRIPTS_PATH}}/deps-generate.py <project_root> --stale-only
```

## Configuration

{{#claude}}
In `{{LOCAL_CONFIG}}` {{LOCAL_CONFIG_FORMAT}}:

```yaml
dep_maps:
  dir: .claude/deps
  tool_cmd: "madge --json --extensions ts,tsx"
  modules:
    - apps/api
    - apps/web-consumer
    - packages/shared
```
{{/claude}}
{{#codex}}
In `{{LOCAL_CONFIG}}`:

```json
{
  "dep_maps": {
    "dir": ".codex/deps",
    "tool_cmd": "madge --json --extensions ts,tsx",
    "modules": [
      "apps/api",
      "apps/web-consumer",
      "packages/shared"
    ]
  }
}
```
{{/codex}}

Each tracked module should produce a module-specific dep-map file.

## Freshness Model

{{#claude}}
Claude normally keeps dep maps fresh through:

- hook-based stale marking after relevant edits
- mtime-based stale detection during generation or query
{{/claude}}
{{#codex}}
Codex currently keeps dep maps fresh through:

- manual stale marking when the operator knows a map is outdated
- mtime-based stale detection during generation or query
{{/codex}}

When `deps-query.py` runs, it should refresh stale data before returning
results when practical.

## When to Use

| Situation | Use dependency maps? |
|---|---|
| Finding consumers of a `.ts` or `.tsx` file | Yes |
| Checking blast radius before modifying shared code | Yes |
| Finding what a file depends on | Yes |
| Cross-module consumer analysis | Yes |
| Searching for string references or config keys | No |
| Non-TypeScript files | No |
| Projects without configured dependency maps | No |

## Limitations

- TypeScript-focused static analysis does not capture every dynamic runtime edge
- dynamic imports with variables are usually not fully resolvable
- re-export chains may surface the barrel file rather than the deepest consumer
- generated files only appear after they exist on disk

## Expected Output Shape

Human-readable output should include:

```text
FILE: packages/shared/src/types.ts
MODULE: packages/shared

DEPENDENCIES (3):
  packages/shared/src/constants.ts
  packages/shared/src/utils.ts
  packages/shared/src/validators.ts

DEPENDENTS (12):
  apps/api/src/routes/booking.ts
  apps/api/src/routes/merchant.ts
  apps/web-consumer/src/lib/api.ts
  ...

BLAST RADIUS: 12 direct consumer(s)
  Across 4 module(s): apps/api, apps/web-consumer, apps/web-merchant, packages/booking-logic
```

JSON output should provide at least:

```json
{
  "file": "packages/shared/src/types.ts",
  "found_in": "deps-packages-shared.json",
  "dependencies": ["packages/shared/src/constants.ts"],
  "dependents": ["apps/api/src/routes/booking.ts"]
}
```
