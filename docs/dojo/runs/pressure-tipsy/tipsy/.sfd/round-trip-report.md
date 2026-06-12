# Round-Trip Report — tipsy (contract rev 1)

mode: subagent
date: 2026-06-12
inputs handed to reconstructor: `.contracts/tipsy.contract.yaml` +
`.sfd/surface-state-inventory.md` ONLY (no prototype, no decision log, no
conversation). Fresh-context general-purpose subagent (id a43bd986f7ec8b547),
instructed to read exactly those two files.

## Rounds

### Round 1

Reconstruction: full scripted session transcript covering all four in-scope
inventory cells, with exact arithmetic (tie case 4.25→4.30, 6.375→6.40,
boundary 999999.99 accepted with dime-rounded six-figure tips) and 12
explicitly declared invented assumptions.

**Leaks found: 0.** Every behavior the converged prototype demonstrates was
reproduced from the YAML + inventory alone: dime rounding ties-up, totals from
rounded tip, $-prefix equivalence (byte-identical output), zero/negative
rejection with empty stdout, no-args → usage to stderr exit 2, piped stdin
never consumed and no prompt invented, non-numeric / >2-decimals / over-cap /
extra-args / unknown-option rejections all exit 2, --help to stdout exit 0,
success exit 0.

**Accepted cosmetic diffs** (layout/wording the contracts legitimately don't
govern):
- Success-line shape: `10%: tip $4.30   total $46.80` vs prototype's
  column-padded `  10%   tip $4.30    total $46.80`; no blank line after the
  bill line; `Bill: $42.50` vs `Bill:  $42.50`.
- All error-message phrasing (e.g. "bill amount must be greater than zero:
  '-5'" vs "bill amount must be a positive number (got: -5)") — C-014 governs
  quality, not wording.
- Usage-block and --help wording/ordering.
- Example bill values chosen ($7.30 / $999999.99 instead of $100).

**Residual ambiguities (not leaks — never demonstrated in the converged
prototype, hence undecided, not unpinned-but-converged):**
- Validation precedence for multi-error inputs and `--help` + amount mixes →
  logged as decision-log OQ-4, per the rule that open questions live in the
  decision log and never ride along as clauses.
- Output thousands-separator format for 6-figure totals (reconstructor assumed
  bare `$1099999.99`, consistent with the input-side rule) → folded into OQ-4
  territory; no converged behavior to contradict.
- Note: the reconstructor under-applied C-015 for `tipsy --json 20` (left it
  out); C-015's plain reading already pins any invocation containing an
  unknown option → exit 2. Reconstructor caution, not a contract leak.

**Fixes applied: none required** (no clause added or tightened; OQ-4 appended
to the decision log).

### Round 2

Not run — round 1 produced zero leaks; protocol allows stopping (max 2 rounds).

## Verdict

Contracts are sufficient: a blind agent rebuilt the surface at
session-transcript fidelity with only cosmetic divergence. Remaining diffs
cosmetic-only — accepted and noted above.

## Self-Admission Walk (Accord A1–A9), contract rev 1

Performed before the round-trip, over `.contracts/tipsy.contract.yaml`.
Mechanical lint (A1/A2/A4/A5/A6/A7/A9: YAML validity, unique ids, required
fields, exactly one acceptance type, one RFC-2119 keyword, no SHOULD, no
qualitative perf words, no shared acceptance targets, risk/evidence pairing)
ran clean; A3/A8 assessed by judgment.

- C-001: admitted · FLAG PENDING-HARNESS (A3: tests/test_output.py absent) ·
  A8 judged atomic (one rendering obligation)
- C-002: admitted · FLAG PENDING-HARNESS (A3)
- C-003: admitted · FLAG PENDING-HARNESS (A3)
- C-004: admitted · FLAG PENDING-HARNESS (A3: scripts/bench_startup.sh absent)
  · A6 pass — "feels fast" was numbered (p95 < 50ms) at compile (D-004); an
  unnumbered version would have been REFUSED A6
- C-005: admitted · FLAG PENDING-HARNESS (A3: tipsy binary absent) · A8 judged
  atomic — one rejection law; stderr/exit-2/empty-stdout are the definition of
  "reject", checked by a single command
- C-006: admitted · FLAG PENDING-HARNESS (A3) · MUST NOT mined from paid
  rejection (D-006)
- C-007: admitted · FLAG PENDING-HARNESS (A3)
- C-008: admitted · FLAG PENDING-HARNESS (A3)
- C-009: admitted · FLAG PENDING-HARNESS (A3)
- C-010: admitted · FLAG PENDING-HARNESS (A3)
- C-011: admitted · FLAG PENDING-HARNESS (A3) · A8 note: boundary acceptance in
  the command is the edge-test of the single cap law, not a second obligation
- C-012: admitted · FLAG PENDING-HARNESS (A3)
- C-013: admitted · FLAG PENDING-HARNESS (A3)
- C-014: admitted · A1: `verdict: human` explicit, no flag
- C-015: admitted · FLAG PENDING-HARNESS (A3)
- C-016: admitted · FLAG PENDING-HARNESS (A3) · born at contract compile
  (coverage gap: success exit code demonstrated in transcript but unpinned)

Refusals: 0 (fixed-at-source count: 1 pre-emptive — C-004 quantification;
1 coverage fix — C-016 added via clause log before the walk).
Flags: 15 × PENDING-HARNESS (A3), recorded per-clause in contract `notes:`.
A5 OVERLAP: none. A9 THIN-EVIDENCE: none (no risk: high clauses).
