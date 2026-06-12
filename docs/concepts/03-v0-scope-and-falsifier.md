# Docket — v0 Scope, Acceptance, Falsifier

**Status:** concept. v0 cut proposed by Claude, pending Pyro's sign-off.
Read `00`–`02` first.

---

## v0 scope (the smallest docket that can be proven wrong)

**In:**

- `.contracts/` format per `01` (schema, four clause archetypes)
- `docket import` / `docket add` — the Accord (door checks A1–A9),
  refuse/flag semantics, `--sign-unanchored` override
- `docket check [clause|--all]` — conformance with drift naming, exit codes
- `docket status` — derived state, the glance
- `docket audit` — coverage views (surface cells, failure states, NFRs,
  risk/evidence match); makes incompleteness inspectable
- `docket review` — verdicts on evidence bundles and failure reports,
  typed rejection (work / evidence / clause defect), per-clause calibration
- `docket amend` / `sign` / `add` — the legislature: draft → re-admission →
  signature → rev bump → evidence invalidation
- `docket tasks --next [--json]` and `docket file` — the agent surface
- Single authority (one signer). Python, file-native, no daemon, no DB.

**Out (deferred until evidence demands them):** multi-party authority,
SHOULD/advisory clauses, validator-role schema fields, clause dependency
edges, watch/notify modes, TUI/HTML boards, multi-repo dockets, CI
integration sugar beyond exit codes, any producer- or consumer-specific
integration.

**Sequencing option (from Accord's v0):** build read-mostly first —
import/audit/check/status before review/amend/sign — if the build wants an
even cheaper first falsification rung. The full courtroom remains the v0
definition of done either way.

## v0 acceptance — written as a docket contract (recursive fixture)

Docket's own requirements, in docket's own format. v0 ships when this file
imports through its own door and goes green under its own `check`:

```yaml
contract: docket-v0
rev: 1
source: docs/concepts/00..03 (concept convergence, 2026-06-12)
signed: []   # Pyro signs at v0 kickoff

clauses:
  - id: D0-001
    obligation: >
      The door MUST refuse clauses without a typed acceptance procedure
      and MUST refuse obligations lacking exactly one MUST/MUST NOT.
    acceptance: {test: tests/test_door.py::test_refusals_a1_a4_a6_a7}
    anchors: [{decision: concept-01-door-policy}]

  - id: D0-002
    obligation: >
      Ledger state MUST be derived at runtime from clause files plus
      evidence; no state field may be persisted.
    acceptance: {test: tests/test_state.py::test_no_stored_state}
    anchors: [{decision: concept-01-design-stance}]

  - id: D0-003
    obligation: >
      Amending a clause MUST bump the contract rev and invalidate only
      that clause's evidence bundles.
    acceptance: {test: tests/test_amend.py::test_rev_bump_scoped_invalidation}
    anchors: [{surface: "amend × partial"}]

  - id: D0-004
    obligation: >
      Every red state surfaced by status/check/review MUST print at least
      one work-exit and one law-exit.
    acceptance: {test: tests/test_surfaces.py::test_red_states_have_two_exits}
    anchors: [{surface: "check × failure"}, {decision: dead-loop-critique}]

  - id: D0-005
    obligation: >
      A rejection MUST record a typed reason (work-defect | evidence-defect
      | clause-defect) and clause-defect counts MUST be queryable per clause.
    acceptance: {test: tests/test_review.py::test_typed_rejection_calibration}
    anchors: [{decision: concept-01-calibration}, {decision: DC-0002-accord-merge}]

  - id: D0-006
    obligation: >
      Docket MUST NOT execute domain logic; acceptance procedures are
      delegated via subprocess and judged by exit code or threshold only.
    acceptance: {test: tests/test_exec.py::test_delegation_only}
    anchors: [{decision: concept-00-boundary-discipline}]

  - id: D0-007
    obligation: >
      The flock feat/skills .sfd/contracts.md MUST import with zero manual
      reformatting beyond clause-ification, with every refusal naming its
      door check.
    acceptance: {command: "docket import fixtures/flock-skills.contract.yaml",
                 expect: "exit 0, ≥8 admitted, refusals each cite A1–A7"}
    anchors: [{compat: flock-feat-skills-sfd-artifacts}]
```

(The recursive fixture is the same trick the akinate skill used: the tool's
first real input is itself. "Did not converge, with diagnosis" is a valid
fixture outcome; shipping without the fixture passing is not.)

## The falsifier (what would prove Docket wrong)

One real piece of work through the full pipeline:
**SFD handoff bundle → docket import → agent loops fulfill clauses →
evidence bundles → verdicts → done.** The flock `feat/skills` contracts are
the designated first case (they already exist, they are real, and they were
the artifact that started this design).

Docket is *refuted* — not merely imperfect — if any of these hold after a
honest run:

1. **A second spec reality emerges anyway**: participants reach for a prose
   requirements doc because the clause format cannot carry what they need.
2. **Ledger drift**: the contracts stop matching the code and nobody
   notices, because `check` is not actually being run (the ledger became a
   document, not an instrument).
3. **Evidence decay**: bundles rot into vibes — claims without runnable
   references — and verdicts get rendered anyway.
4. **Verdict fatigue**: the human-verdict moments are so frequent or so
   low-information that Pyro starts rubber-stamping (measured: accept rate
   ≈ 100% with median review time near zero).

Each failure names its lesson: (1) schema too weak → extend or kill; (2)
the loop needs CI enforcement, not human discipline; (3) the door must
extend to evidence admission; (4) the courtroom model over-involves the
authority and needs risk-tiered auto-acceptance — which is a known research
direction in the claude-knowledge acceptance thread, deliberately deferred.

## Relations in the constellation (philosophy citations, not couplings)

Stated once, to pre-empt the merge reflex (see
`claude-knowledge/ops/observations/obs-007`): Docket integrates with
nothing by design. The relations below are *conceptual siblings* whose
principles informed the design — not dependencies, not integration targets.

- **SFD** (limitless): richest contract producer; its 0.7 spec aligns its
  output with Docket's door — via the format, never via code.
- **Loop-shaped work** ("loop not prompt"): loops are the natural clause
  consumers — a clause is an evaluator plus a stop condition. Any loop
  runner qualifies through three file-level touchpoints (tasks/check/file).
- **Proofroom / acceptance-casefile research** (claude-knowledge thread 9):
  same philosophical layer — evidence bundles, verifier independence,
  review-burden metrics. Docket is the smallest practical instantiation of
  that research's vocabulary; whether they ever converge is a question for
  evidence, not for a roadmap.
- **Canon**: admission-gate philosophy applied to dependencies; Docket
  applies it to obligations. Shared principle, zero shared code.

## Next steps (the legitimate pipeline crossings)

1. Pyro reviews these four concept docs; amendments by conversation.
2. KG hygiene: file `sketches/docket.md` in claude-knowledge (idea-layer
   record) and a `projects/docket.md` dossier (routing card) — the proper
   downward/upward layer crossings.
3. On approval: writing-plans for v0 against `03` (this doc), build through
   the recursive fixture, then run the falsifier on flock `feat/skills`.
