# Surface State Inventory — mdtodo

Status: complete (Gate 1, 2026-06-12). Classifications: **in-scope** =
demonstrated in the converged transcript and accepted; **deferred** =
acknowledged, not blocking convergence; **n/a** = state cannot occur for this
unit by design.

Surface units:
- `scan-text` — default invocation: `mdtodo <path>...`
- `scan-json` — JSON mode: `mdtodo --json <path>...`
- `usage` — argument parsing, validation, `--help`

Cell naming convention used in clause anchors: `<unit> × <state>`.

## scan-text — `mdtodo <path>...`

| State | Classification | Notes / governing clauses |
|---|---|---|
| empty / zero-data | in-scope | zero TODOs (incl. zero files matched) → single message, exit 0 — C-016, C-021 |
| loading / in-progress | n/a | designed out: no progress output, silent until done; runtime bounded by C-012. Very-large-tree feedback → open question |
| success | in-scope | grouped list + summary footer — C-001, C-003, C-004, C-005, C-006, C-007, C-008, C-009, C-011, C-012 |
| validation failure | n/a | argument validation happens before scanning; owned by `usage` unit |
| system failure | in-scope | I/O error mid-read handled as unreadable file: warn, skip, continue — C-014, C-022 |
| partial failure | in-scope | some files read, some not; readable results still print; exit 1 — C-014, C-022 |
| permission denied | in-scope | unreadable file path of C-014; warning wording governed by C-020 |
| conflict | n/a | no shared mutable state; no writes |
| rate limit / retry | n/a | no network, no quota |
| offline / degraded | n/a | purely local |

## scan-json — `mdtodo --json <path>...`

| State | Classification | Notes / governing clauses |
|---|---|---|
| empty / zero-data | in-scope | `[]` on stdout, exit 0 — C-010, C-017, C-021 |
| loading / in-progress | n/a | as scan-text |
| success | in-scope | single JSON array, fixed field set, same ordering as text — C-010, C-017, C-004 |
| validation failure | n/a | owned by `usage` unit |
| system failure | in-scope | stdout stays pure JSON; diagnostics to stderr — C-017, C-014, C-022 |
| partial failure | in-scope | valid JSON on stdout + warnings on stderr + exit 1 — C-017, C-014, C-022 |
| permission denied | in-scope | C-014 (applies in both modes), C-017 |
| conflict | n/a | as scan-text |
| rate limit / retry | n/a | as scan-text |
| offline / degraded | n/a | as scan-text |

## usage — argument parsing, `--help`

| State | Classification | Notes / governing clauses |
|---|---|---|
| empty / zero-data | n/a | no data state; an empty argument list is a validation failure |
| loading / in-progress | n/a | instantaneous |
| success | in-scope | `--help` → usage text on stdout, exit 0 — C-019 |
| validation failure | in-scope | no paths / unknown flag / nonexistent path → stderr error, nothing scanned, exit 2 — C-018, C-023, C-020 |
| system failure | n/a | no dependencies involved before scanning |
| partial failure | n/a | validation is all-or-nothing |
| permission denied | n/a | not applicable to parsing |
| conflict | n/a | — |
| rate limit / retry | n/a | — |
| offline / degraded | n/a | — |

## Coverage summary

In-scope cells: 12. Every in-scope cell is cited by ≥1 clause anchor in
`.contracts/mdtodo.contract.yaml` (checked at Phase 5 step 2). Deferred cells:
0 (the only candidate — progress feedback on very large trees — was classified
n/a-by-design with an open question logged in the decision log).
