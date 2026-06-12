# Round-Trip Report — mdtodo

mode: subagent
date: 2026-06-12
inputs handed to blind agent: `.contracts/mdtodo.contract.yaml` +
`.sfd/surface-state-inventory.md` ONLY (not the prototype, not the decision
log, not the conversation). Fresh-context subagent per round; round 2 used a
new agent, not the round-1 context.
rounds: 2 (protocol max 2)
result: PASS — round 2 divergences cosmetic-only; 0 behavioral leaks remain.

## Round 1

Blind reconstruction covered all 12 in-scope inventory cells. Diff against
`prototype/session-transcript.md`:

**Leaks (behavior the contracts failed to pin) — 3, all fixed:**

1. Summary footer template. Reconstruction: `Found 8 TODOs in 3 files (4 files
   scanned).` Converged: `5 TODOs in 3 files (4 files scanned)`. C-003 named
   the three counts but not the template.
   → Fix: C-003 tightened with the exact footer form.
2. Partial-failure footer accounting. Reconstruction silently excluded
   unreadable files from the count (`(3 files scanned)`); converged surface
   reports them (`(3 of 4 files scanned, 1 unreadable)`).
   → Fix: new clause C-024 (via clause log).
3. Usage synopsis after validation errors. Reconstruction printed only the
   error line; converged surface follows every usage error with
   `usage: mdtodo [--json] <path>...`.
   → Fix: new clause C-025 (via clause log).

**Lucky guess, pinned proactively:** directory-discovered path rendering
(`<given-dir>/<relpath>`) was flagged INVENTED by the blind agent but happened
to match the prototype. Pinned in the C-003 tightening rather than left to
luck.

**Cosmetic (accepted, not contract-governed) — 4:** warning/error wording and
prefixes (style governed by C-020 only); help body text beyond the pinned
first line (C-019); line-number padding/alignment; JSON pretty-printing,
indent, and key order.

## Round 2

Fresh blind agent, updated contract. Diff against the converged prototype:

**Leaks: 0.** All round-1 fixes reproduced exactly: footer template,
`(5 of 6 files scanned, 1 unreadable)` accounting with R = K − U, usage
synopsis on all three validation-failure variants, exit codes 0/1/2, format
rules including checked-item exclusion, code-block scanning, HTML-comment
`-->` stripping, ordering, JSON field set, stream purity.

**Cosmetic (accepted):** diagnostic message templates (`mdtodo: error:` /
`mdtodo: warning:` prefixes vs the prototype's bare `error:` / `warning:`);
help body; line-number padding; JSON serialization layout; stderr/stdout
interleaving position of the warning (buffering-dependent, not governable).

**Residuals surfaced by the blind agent, dispositioned:**

- C-016's literal `files` vs C-003's "pluralized naturally" — latent template
  inconsistency. → C-016 obligation amended (wording-consistency fix, no new
  behavior), recorded in clause log and contract notes.
- C-016 × C-024 interaction (zero TODOs AND unreadable files in one run) —
  never demonstrated to the user, so it cannot become a clause claiming
  acceptance. → logged as an open question in the decision log.

## Self-Admission Walk (the Accord, A1–A9)

Walked over the compiled draft (22 clauses: C-001..C-015, C-016..C-020) before
the round-trip; re-walked every clause added or changed afterward (C-021..C-025,
C-003, C-016).

Per-clause record:

- C-001: admitted · FLAG PENDING-HARNESS (A3: tests/test_scan_set.py does not exist yet)
- C-002: admitted · FLAG PENDING-HARNESS (A3: command targets the not-yet-built binary)
- C-003: admitted · FLAG PENDING-HARNESS (A3) · tightened at round-trip r1, re-walked, admitted
- C-004: admitted · FLAG PENDING-HARNESS (A3)
- C-005: admitted · FLAG PENDING-HARNESS (A3)
- C-006: admitted · FLAG PENDING-HARNESS (A3)
- C-007: admitted · FLAG PENDING-HARNESS (A3)
- C-008: admitted · FLAG PENDING-HARNESS (A3)
- C-009: admitted · FLAG PENDING-HARNESS (A3)
- C-010: admitted · FLAG PENDING-HARNESS (A3) · A8 judgment call: "zero items yields []" kept — degenerate case of the same array law, not a second obligation
- C-011: admitted · FLAG PENDING-HARNESS (A3: bench script absent) · FLAG OVERLAP (A5: shares scripts/bench_bigfile.sh with C-012) → resolved by scoping: bench emits two metrics, C-011 binds memory only — recorded in contract `notes:`
- C-012: admitted · FLAG PENDING-HARNESS (A3) · A5 OVERLAP resolved by scoping (binds time only) — recorded in `notes:`
- C-013: admitted · FLAG PENDING-HARNESS (A3)
- C-014: admitted · FLAG PENDING-HARNESS (A3) · A8 judgment call: warn/skip/continue/report kept as one clause — a single graceful-degradation law with one acceptance test
- C-015: **REFUSED A8** — "two laws in one clause — split them" (in fact three: exit 0, exit 1, exit 2 in one mapping) → split into C-021, C-022, C-023; C-015 superseded in the clause log and absent from the contract file
- C-016: admitted · FLAG PENDING-HARNESS (A3) · amended at round-trip r2 (pluralization consistency), re-walked, admitted; undemonstrated C-024 interaction recorded in `notes:` + open questions
- C-017: admitted · FLAG PENDING-HARNESS (A3)
- C-018: admitted · FLAG PENDING-HARNESS (A3)
- C-019: admitted · FLAG PENDING-HARNESS (A3: command targets the not-yet-built binary)
- C-020: admitted · acceptance `verdict: human` — legal and explicit (A1)
- C-021: admitted (born from C-015 split) · FLAG PENDING-HARNESS (A3)
- C-022: admitted (born from C-015 split) · FLAG PENDING-HARNESS (A3)
- C-023: admitted (born from C-015 split) · FLAG PENDING-HARNESS (A3)
- C-024: admitted (born round-trip r1) · FLAG PENDING-HARNESS (A3)
- C-025: admitted (born round-trip r1) · FLAG PENDING-HARNESS (A3)

Check-level summary:

- A1: pass — every clause has exactly one typed acceptance; the one human
  verdict (C-020) is explicit.
- A2: pass — every clause has ≥1 typed anchor; pure-negative clauses C-002 and
  C-013 anchor to decisions D-002 / D-008.
- A3: 24/24 FLAG PENDING-HARNESS — pre-implementation handoff; no test files,
  bench script, or binary exist yet. Normal and recorded.
- A4: pass — exactly one MUST or MUST NOT per obligation; zero SHOULDs.
- A5: one OVERLAP (C-011/C-012 shared bench target) — resolved by metric
  scoping before signing; recorded in both clauses' `notes:`.
- A6: pass — the born-qualitative "shouldn't choke on big files" was numbered
  at compile time (100 MB / <5 s / <64 MB RSS, confirmed via options, D-012);
  no unnumbered qualitative performance words remain in any obligation.
- A7: pass — mechanically validated (valid YAML, required fields, unique ids,
  one acceptance type each).
- A8: one REFUSE (C-015) — fixed at source by splitting; judgment calls on
  C-010 and C-014 recorded above.
- A9: vacuous pass — no `risk: high` clauses (C-011, C-014 are `medium`), so
  no `evidence_required` obligations triggered.

Refusals fixed at source: 1 (C-015 → C-021/C-022/C-023).
Flags recorded: 24× PENDING-HARNESS, 1× OVERLAP (resolved).
