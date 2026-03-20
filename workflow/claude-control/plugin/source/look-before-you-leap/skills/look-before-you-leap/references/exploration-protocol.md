# Exploration Protocol

Answer all 8 questions before writing a plan. If a question does not apply,
write `N/A`; do not skip it. You are not ready to plan until all 8 have
concrete answers and confidence is Medium or higher.

---

## Step 0: Run deps-query First When Configured

Before answering any question below, check the active Claude control layer for
the resolved `deps-query.py` command. If dependency maps are configured, run
the query on every file in scope before reading broadly or grepping. A hook may
enforce this, but you should do it proactively rather than waiting to be
blocked.

Why first:

- it reveals consumers and cross-module dependencies early
- it shapes blast-radius analysis before planning
- it helps avoid spending time on the wrong files

Record the output. You will need it for consumers, blast radius, and the
discovery summary.

If dependency maps are not configured and this is a TypeScript project, suggest
setting them up before large shared-code changes.

## 1. What is the scope?

Which files and directories will this change touch?

How to answer:

- search for likely file patterns
- read the request word by word
- identify every noun that maps to a file or module

Output:

- list of file paths with explicit boundaries

## 2. What are the entry points?

Which files will you directly modify?

How to answer:

- read each candidate file
- note current state, key exports, major responsibilities, and approximate size

Output:

- file path plus brief description for each entry point

## 3. Who are the consumers?

Who imports or uses the files you are changing?

If dependency maps are configured, use the dependency-query helper for every
entry point. Do not substitute ad-hoc grep when a stronger graph source exists.

If dependency maps are not configured:

- grep for import and require usage
- trace important call sites manually when needed

Output:

- list of consumer files with count
- if count is large, provide total plus representative examples
- when dependency maps exist, capture the exact dependency-query output

## 4. What patterns already exist?

How does this codebase solve similar problems?

How to answer:

- read sibling files in the same area
- look for shared utilities and established patterns
- read `CLAUDE.md`, README files, and local guidance

Output:

- naming patterns
- error-handling patterns
- data-flow conventions
- repo-specific implementation expectations

## 5. What test infrastructure exists?

Where do tests live? What framework? Any test utilities?

How to answer:

- search for `*.test.*`, `*.spec.*`, `test/`, and `__tests__/`
- read at least one representative test file
- inspect package or task scripts for the relevant test command

Output:

- framework name
- test location pattern
- how to run the relevant tests

## 6. What are the project conventions?

What style, structure, and tooling constraints apply?

How to answer:

- read repo guidance files
- inspect linter, formatter, and compiler configs
- note naming, file-organization, and import-order expectations

Output:

- key conventions that constrain implementation choices

## 7. What is the blast radius?

What could break if you get this wrong?

How to answer:

- use dependency-query output when available
- otherwise count consumers and identify shared types, utilities, and public APIs

Output:

- list of risk areas with consumer counts and why they matter

## 8. What is your confidence?

Can you write a complete plan right now?

How to answer:

- review questions 1-7
- identify remaining assumptions and unknowns

Output:

- Low / Medium / High with justification

Interpretation:

- Low: stop and explore more
- Medium: proceed, but flag unknowns in the plan
- High: proceed with full confidence
