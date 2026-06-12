# CLAUDE.md — docket

Docket is the repo's courtroom: contracts (obligations) + evidence +
verdicts, file-native, deliberately boring. Concept phase — no code yet.

## Orient

1. Read `memory/boot/context.md` — project state, founding decisions, next
   steps.
2. The four concept docs in `docs/concepts/` (numbered reading order) are
   the design. They were converged conversationally on 2026-06-12 and are
   the authority until amended.

## Rules of this repo

- **No second spec reality.** The concept docs define behavior via concrete
  artifacts (schemas by example, terminal sessions). Never add a parallel
  prose-requirements layer. Extend the docs' example artifacts instead.
- **Boundary discipline.** Docket integrates with nothing: no
  producer-specific (SFD) or consumer-specific (loop runner) code paths.
  If a change requires knowing who produced or consumes a contract, the
  change is wrong.
- **State is derived, never stored.** If you find yourself persisting a
  status field, stop.
- **v0 builds against `docs/concepts/03`** — the recursive fixture
  (docket's own requirements as a docket contract) gates shipping.
- Git identity: pyros-projects (`pyros.sd.models@gmail.com`) — already set
  locally. Never use the whiteduck identity here; never mention
  work-context names in this repo's content.

## Memory

`memory/` is the codies-memory-style vault (boot/, decisions/, inbox/,
lessons/, sessions/, threads/). Keep decisions in `memory/decisions/`,
session summaries in `memory/sessions/`. The founding decisions are
DC-0001.
