# SFD Decision Log — tipsy

## Surface Type
CLI (terminal session). Prototype form: scripted session transcript
(`prototype/session-transcript.md`).

## Convergence Status
Converged on 2026-06-12 ("this feels right, freeze it").

## Decisions

- [D-001] 2026-06-12 — Surface is a one-shot CLI; prototype is a scripted session
  transcript. — Per the SFD surface table; user gave no architecture constraints.
- [D-002] 2026-06-12 — Concept direction: flags-only one-shot CLI, stdlib only.
  — User: "the flags-only one, no fancy stuff." Rejected: prompt-first interactive
  variant; pipe-friendly configurable variant (config file, --json).
- [D-003] 2026-06-12 — Tips round to the nearest $0.10, ties rounding UP; totals are
  bill + rounded tip. — User asked for dime rounding; tie direction is my call
  (generous-to-server beats banker's rounding for a tip tool), confirmed via options
  at contract compile. Rejected: round-half-to-even; truncation; rounding the total
  instead of the tip.
- [D-004] 2026-06-12 — "Feels fast" quantified as invocation-to-output p95 < 50ms on
  the reference machine. — Qualitative words don't survive contract compile (Accord
  A6). 50ms recommended over 100ms because the tool is trivially small; confirmed
  via options at contract compile. Rejected: leaving it qualitative; demoting to
  open questions.
- [D-005] 2026-06-12 — Zero and negative bills are rejected (one-line stderr error,
  exit 2). — Nothing to tip on; silent $0 math would mask typos. Rejected: treating
  $0 as a valid bill with $0 tips.
- [D-006] 2026-06-12 — Interactive no-args prompt mode KILLED. No-args prints usage
  to stderr, exit 2; stdin is never read under any invocation. — User: "kill it,
  flags only, I hate interactive prompts." Strong rejection → MUST NOT clause
  (C-006). The round-1 prompt mode is a paid rejection; it must never need
  re-rejecting.
- [D-007] 2026-06-12 — Weird-input policy: accept a single leading "$"; reject
  non-numeric input, >2 decimal places, amounts > $999999.99, multiple positional
  args, and unknown options — all with a single human-readable error line on stderr
  and exit 2, no stack traces. — User: "handle weird inputs sensibly." Rejected:
  silently coercing/rounding malformed input; accepting thousands separators
  (see OQ-1).
- [D-008] 2026-06-12 — Exit-code convention: 0 success, 2 for every usage/validation
  error. — Matches common CLI usage-error convention; exit 1 reserved for future
  internal failures. Rejected: exit 1 for validation errors.

## Derived Contracts

`.contracts/tipsy.contract.yaml` (rev 1) — clauses C-001..C-016, compiled from
`.sfd/clause-log.md`. The contract file is the spec; this log records the why.
(No parallel prose spec — Anti-Pattern 7.)

## Open Questions

- [OQ-1] Thousands separators in input ("1,234.56") are currently rejected as
  non-numeric. Revisit if it annoys in practice.
- [OQ-2] Behavior on system failure (broken pipe / closed stdout) is unspecified —
  deferred state in the inventory; pin it at hardening time.
- [OQ-3] Custom percentages explicitly out of scope per "no fancy stuff"; would be
  a new contract rev, not a quiet addition.
- [OQ-4] (from round-trip residuals) Precedence is unpinned for (a) inputs failing
  multiple validation rules at once (e.g. "-5.123": negative vs decimals) and
  (b) `--help` combined with a positional amount. Both exit-2/exit-0 classes are
  individually pinned; only which message/rule wins is open. Never demonstrated in
  the converged surface — undecided, so logged here rather than invented as clauses.

## Hardening Status

Engagement stopped at Gate 2 by design (handoff bundle is the deliverable;
no Phase 6/7 performed).

- [ ] Persistence (n/a — stateless)
- [ ] Auth (n/a)
- [ ] Domain logic (currently: simulated — transcript only, nothing implemented)
- [ ] Error handling (currently: specified in contract, not implemented)
- [ ] Performance (currently: target set [C-004], not measured)
