# Claude Package Boundary

This directory defines the future installable Claude package boundary.

Intended contents:

- package-facing metadata derived from the Claude plugin
- packaged runtime assets that belong in the installed plugin
- references to Claude runtime defaults and orchestration prompts

Source of provenance:

- `workflow/claude-control/plugin/source/`

Rule:

- the original external repo stays untouched
- `source/` is the editable staged plugin tree in this repo
- this package boundary should eventually be derived from that staged tree
