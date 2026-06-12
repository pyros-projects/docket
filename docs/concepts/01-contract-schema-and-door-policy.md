# Docket — Contract Schema and Door Policy

**Status:** converged via an SFD pass (Pyro + Claude, 2026-06-12); schema by
example, then the door. Read `00-docket-why-and-what.md` first.

---

## Design stance

Three principles govern everything below:

1. **State is derived, never stored.** Docket stores law (clauses) and
   history (evidence bundles, signatures, amendments). Green/red/holding is
   *computed* from those at runtime. There is no status field to rot, no
   lock file to drift.
2. **Docket executes nothing domain-specific.** Every acceptance procedure
   delegates to the repo's own tools. Docket shells out, reads exit codes
   and values, records results.
3. **Git is the database.** Contracts are files; amendment history is commit
   history; revs are explicit in-file so they survive outside git too.

## File layout

```
.contracts/
  skills-loading.contract.yaml      # one file per contract domain
  pipeline-replay.contract.yaml
  evidence/
    C-004/bundle-003.json           # filed bundles, append-only
    C-006/...
```

## Schema by example

One contract file, four clause archetypes — these four cover the space:

```yaml
contract: skills-loading
rev: 3
source: .sfd/contracts.md (SFD Gate 2, 2026-06-12)   # which horse, when
signed:
  - {rev: 3, by: pyro, date: 2026-06-14}

clauses:
  # Archetype 1: test-checked
  - id: C-004
    obligation: >
      Mode selection MUST follow shape rules: caller runtime=True forces
      tool mode; frontmatter mode=tool wins over caller; otherwise token
      budget decides inline vs tool.
    acceptance:
      test: tests/skills/unit/test_compilation.py::test_shape_select
    anchors:
      - surface: "skill-attach × mode-selection"   # SFD state-inventory cell
      - decision: D-012                            # decision-log entry

  # Archetype 2: metric-checked
  - id: C-011
    obligation: >
      Skill discovery MUST resolve 100 skills in under 200ms on the
      reference machine.
    acceptance:
      metric: scripts/bench_discovery.py --skills 100
      threshold: "p95 < 200ms"
    anchors:
      - surface: "skill-attach × loading"

  # Archetype 3: non-surface horse (incident-born)
  - id: C-012
    obligation: >
      DLQ replay MUST be idempotent — replaying the same batch twice
      produces no duplicate events.
    acceptance:
      test: tests/pipeline/test_replay_idempotent.py
    anchors:
      - incident: postmortem-2026-06-14-dlq-dupes

  # Archetype 4: human-verdict negative clause
  - id: C-013
    obligation: >
      The progress view MUST NOT use proportional-area encodings
      (pie/donut charts).
    acceptance:
      verdict: human        # explicit: can never go green mechanically
    anchors:
      - decision: D-007     # a rejected alternative, paid for during convergence
```

### Field reference

| Field | Required | Semantics |
|---|---|---|
| `contract`, `rev`, `source`, `signed` | yes | file-level identity, version, horse, authority trail |
| `id` | yes | stable, per-project monotonic (`C-NNN`); inherited from the producer's clause log when one exists |
| `obligation` | yes | prose with exactly one RFC-2119 keyword: `MUST` or `MUST NOT` (v0 bans `SHOULD` — decide or defer) |
| `acceptance` | yes | exactly one of: `test:` (runner ref) · `metric:` + `threshold:` · `command:` + `expect:` (exit code / output match) · `verdict: human` |
| `anchors` | yes (≥1) | typed provenance: `surface:` (state-inventory cell) · `decision:` · `incident:` · `regulation:` · `sla:` · `compat:` — the many-horses field |
| `status` | no | `active` (default) · `deferred` · `retired` (retired ≠ deleted; history preserved) |
| `notes` | no | residuals and known limits (e.g. "token estimation ±15%, uncontracted") |

Deliberately absent (v0 YAGNI, revisit only with evidence of need):
severity tiers, `SHOULD`/advisory clauses, per-clause owners, multi-party
authorities, dependency edges between clauses.

## The door policy (admission checks A1–A7)

Run by `docket import` / `docket add`. Two outcome classes: **refuse**
(clause does not enter) and **flag** (clause enters carrying an obligation
to resolve).

| # | Check | Outcome | Message style |
|---|---|---|---|
| A1 | acceptance present and of a known type; `verdict: human` legal but must be explicit | refuse | "no acceptance procedure — how would I check this?" |
| A2 | ≥1 typed anchor | refuse, overridable by `--sign-unanchored` (recorded, carries the authority's signature) | "where did this come from?" |
| A3 | acceptance target exists (test file, script) | **flag** `PENDING-HARNESS` | "clause is law; it cannot go green until the harness exists" |
| A4 | obligation contains exactly one of MUST / MUST NOT | refuse | "a hope, not an obligation" |
| A5 | overlap: same acceptance target claimed twice with different expectations | **flag** `OVERLAP` | "resolve before first verdict" |
| A6 | qualitative performance words (fast, reliable, scalable, ...) require numbers | refuse | "give me a number, a test, or defer the clause" |
| A7 | schema validity, unique IDs | refuse | plain validation error |

Two rationale notes that future maintainers will want:

- **A3 is a flag, not a refusal**, because the door checks that the
  acceptance *definition* exists, not its *implementation* — refusing would
  fight TDD's natural order (clause first, harness next).
- **`verdict: human` is a feature, not a hole.** Some obligations are
  legitimately judgment calls (taste, brand, ethics). Forcing them through
  fake mechanical acceptance would hide the judgment inside a vibesy
  command. Declaring them keeps the judgment visible, routed to the
  authority, and countable (a contract that is 80% human-verdict clauses is
  telling you something).

## Evidence bundles

Filed by whoever did the work (agent loop, human, CI), append-only, JSON:

```json
{
  "clause": "C-004",
  "claim": "satisfied",
  "filed_by": "claude-loop#18",
  "rev_at_filing": 3,
  "evidence": [
    {"kind": "test", "ref": "test_shape_select", "result": "8/8 PASS"},
    {"kind": "conformance", "ref": "docket check C-004", "result": "green", "at": "2026-06-12T17:31"},
    {"kind": "trace", "ref": "loop transcript #18", "note": "3 iterations, stop=contract-green"}
  ],
  "residual": "token estimation heuristic ±15% — flagged, not contracted"
}
```

A **failure report** is the same shape with `"claim": "stuck"` plus a
`stuck_on` field — a loop that exhausts its budget files one instead of
going silent (see `02-surfaces.md`, dead-loop flow).

## Verdicts, amendments, and contract quality

- Evidence bundles are valid **against a rev**. Amending a clause bumps the
  file rev and invalidates that clause's bundles → re-verdict required only
  where affected.
- Rejecting a bundle requires a reason, and the reason is typed:
  **work defect** (the work missed) or **clause defect** (the work satisfied
  the clause, but the clause was wrong). Clause defects accumulate as
  **per-clause calibration** — defects per verdict, the contract's own
  quality metric. A clause that survives ten verdicts unamended is validated
  in the only sense that matters; a clause with 2 defects in 5 verdicts is
  the worst law on the books and says so in `status`.
- Nobody validates contracts upfront beyond the door. Form is machine-checked
  at admission; content fidelity is *signed* (an authority act, not a
  score); sufficiency is validated by use. "Top-notch contracts" decompose
  into exactly those three, and only the first can be front-loaded.
