# SFD Decision Log — mdtodo

## Surface Type
CLI (terminal session). Prototype form: scripted session transcript
(`prototype/session-transcript.md`).

## Convergence Status
Converged on 2026-06-12 (user: "this feels right, freeze it").

## Decisions

- [D-001] 2026-06-12 — Surface identified as CLI terminal session; prototype is a
  scripted session transcript. — Unambiguous from the request ("a small CLI").
- [D-002] 2026-06-12 — Direction locked: one-shot scanner ("point it at files or a
  directory, get a list out"). — Rejected: watch-mode TODO dashboard (daemon + live
  TUI) and TODO-board generator (writes TODO.md / syncs issues). User explicitly
  rejected daemon/watch behavior → C-002. Research was offered and skipped by the
  user.
- [D-003] 2026-06-12 — v1 baseline (my opinionated defaults, accepted in round 1):
  positional file/dir paths, recursive `*.md`/`*.markdown` discovery, text output
  grouped by file with summary footer, deterministic ordering (lexicographic
  files, ascending lines). → C-001, C-003, C-004.
- [D-004] 2026-06-12 — Round 1: "the usual todo formats" defined as (a) unchecked
  GFM task list items (`-`/`*`/`+` bullets), (b) `TODO:` and `FIXME:` markers,
  uppercase with colon, anywhere in a line. HTML comments need no special case —
  the marker rule covers `<!-- TODO: ... -->` (trailing `-->` stripped from
  captured text). Checked items excluded. Lowercase `todo:` excluded — too noisy
  in prose (case policy confirmed via options at Phase 5, D-012). Fenced code
  blocks ARE scanned — a TODO in a code sample is still a TODO (simpler and
  predictable; rejected alternative: markdown-aware code-block exclusion).
  → C-005..C-009.
- [D-005] 2026-06-12 — Round 1: big-file strategy is line-streaming, never
  whole-file buffering; concrete numbers attached at contract time (D-012).
  → C-011, C-012.
- [D-006] 2026-06-12 — Round 1: `--json` flag emits a JSON array of
  `{file, line, text, kind}`. Rejected alternative: separate `mdtodo export`
  subcommand (overkill for one alternate format). → C-010.
- [D-007] 2026-06-12 — Round 1 (v2): sketched a `.mdtodorc` config file for custom
  TODO patterns, as a proposal.
- [D-008] 2026-06-12 — Round 2: `.mdtodorc` REJECTED by user — "drop it, no config
  file ever, flags only." Strong rejection → MUST NOT clause C-013. Custom
  patterns, if ever wanted, would arrive as a flag, not a file.
- [D-009] 2026-06-12 — Round 2: unreadable files degrade gracefully — one warning
  line to stderr, skip, continue, readable results still print; diagnostics are
  single-line plain language. Rejected alternative: abort on first error.
  → C-014, C-020, C-017.
- [D-010] 2026-06-12 — Round 2: exit-code mapping 0/1/2 (clean / partial /
  usage), empty result is success not error, `--help` on stdout exits 0,
  invalid invocations rejected before scanning. Rejected alternative:
  grep-style "exit 1 when nothing found" (confirmed via options, D-012).
  → C-015 (later split: C-021..C-023), C-016, C-018, C-019.
- [D-011] 2026-06-12 — Convergence declared after round 2; user froze the surface
  ("this feels right, freeze it"). Gate 1 checklist passed.
- [D-012] 2026-06-12 — Contested clauses confirmed via Propose-Choose-Proceed at
  Phase 5; user took the recommended option in each case:
  (1) big-file thresholds: 100 MB input, < 5 s wall, < 64 MB peak RSS
      [recommended] over 1 GB/30 s/256 MB and over "memory bound only";
  (2) exit 0 when no TODOs found [recommended] over grep-style exit 1;
  (3) uppercase-only `TODO:`/`FIXME:` markers [recommended] over
      case-insensitive matching.
- [D-013] 2026-06-12 — Round-trip round 1 (subagent mode) produced 3 leaks:
  summary-footer template, partial-failure footer accounting, usage synopsis
  on validation errors. Fixed by tightening C-003 and adding C-024, C-025
  (plus proactively pinning directory-path rendering, which the blind agent
  flagged as invented but guessed correctly). 4 divergences classified
  cosmetic (diagnostic wording, help body, line-number padding, JSON
  whitespace). See `.sfd/round-trip-report.md`. Round 2 results recorded
  there. Contract remains rev 1 (pre-signing).

## Open Questions (not clauses — undecided)

- Symlinked directories during recursion: follow or not? (Recommend: do not
  follow; undecided, not pinned.)
- Feedback on very large trees (thousands of files): currently silent until
  done. Acceptable for v1?
- Non-UTF-8 or binary-ish `.md` files: treat as unreadable (warn + skip) or
  scan bytewise? Currently unspecified.
- Duplicate/overlapping inputs (`mdtodo docs docs/roadmap.md`): dedupe or
  report twice? Currently unspecified.
- Zero TODOs combined with unreadable files in one run: what does the single
  C-016 line look like, and does C-024's parenthetical apply to it? Never
  demonstrated to the user (surfaced by round-trip round 2); decide before
  implementing the empty-state path.

## Derived Contracts
See `.contracts/mdtodo.contract.yaml` (rev 1) — 24 active clauses compiled from
`.sfd/clause-log.md`. The contract file plus this log ARE the spec; no parallel
requirements document exists (Anti-Pattern 7).

## Hardening Status
Pre-implementation — handoff bundle only (engagement stopped at Gate 2 by design).
- [ ] Persistence (n/a — stateless tool)
- [ ] Auth (n/a)
- [ ] Domain logic (currently: simulated transcript)
- [ ] Error handling (currently: specified, not implemented)
- [ ] Performance (currently: targets set in C-011/C-012, unverified)
