# Codex Package Boundary

This directory defines the future installable Codex package boundary.

Intended contents:

- package-facing metadata for Codex distribution
- references to the Codex skill pack
- references to installers and runtime wrappers

Source of provenance:

- `workflow/codex-control/plugin/source/`

Rule:

- the original external repo stays untouched
- `source/` is the editable staged plugin tree in this repo
- this package boundary should eventually be derived from that staged tree
