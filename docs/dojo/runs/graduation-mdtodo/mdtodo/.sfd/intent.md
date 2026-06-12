# Intent — mdtodo

Created: 2026-06-12 (Phase 1). Updated during iteration where noted.

## Problem statement

TODO items accumulate inside markdown files — notes, docs, READMEs — where no task
tooling can see them. mdtodo is a small CLI that scans markdown files and extracts
TODO items into a single list, so scattered TODOs become reviewable in one place,
in one command.

## Target users

- Developers and note-takers whose projects and notes are markdown-heavy.
- Primary persona: the requesting user — runs it ad hoc in a terminal against a
  repo or a notes directory; sometimes pipes the output into scripts.

## Constraints

- CLI tool; the interaction surface is the terminal session.
- Small: one command, no service component, no install-time ceremony.
- Output must serve humans (readable text) and scripts (JSON — added in iteration
  round 1 at the user's request).

## Non-negotiables

- One-shot execution: no daemon, no file watching. (User, direction lock.)
- No configuration file, ever — flags only. (User, iteration round 2, verbatim:
  "drop it, no config file ever, flags only".)
- Must not choke on big files. (User, iteration round 1.)
- Unreadable files must not kill the whole run. (User, iteration round 2.)

## Known unknowns

- Which TODO syntaxes count as "the usual formats" — resolved in iteration round 1
  (unchecked task items + TODO:/FIXME: markers; see decision log D-004).
- Symlink traversal policy — open question (decision log, open questions).
- Feedback on very large trees (progress output) — deferred (state inventory).
- Non-UTF-8 / binary-ish .md files — open question (decision log).
