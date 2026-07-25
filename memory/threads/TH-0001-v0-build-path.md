---
id: TH-0001
title: "v0 build path — review gate, KG crossings, plan, fixture, falsifier"
type: thread
status: closed
trust: working
scope: project
created: '2026-06-12'
updated: '2026-07-26'
---

> **CLOSED 2026-07-26 (DC-0005).** This thread tracked the v0 build path
> through Plan 2 (courtroom) and its falsifier. Plan 2 was cut on 06-15 and
> stays cut. What survives is re-derived into DC-0005's scoped experiment, not
> carried forward from here:
> - **tipsy's signed bundle as the fulfillment-run candidate** → superseded;
>   DC-0005 uses a two-change run (A then B) over one contract, because the
>   question is now clause survival across changes, not a single fulfillment.
> - **mdtodo as the golden import fixture** → survives, and is the intended
>   canonical fixture for the DC-0005 experiment.
> - **The guardian-Goodharting / hollow-oracle watch item** → survives and
>   sharpens: defect 1 (`command.expect` never enforced, exit 0 is green) is a
>   *live instance* of the hollow oracle, found in our own runner. The
>   pre-registered response — "door extends to evidence admission" — is now
>   part of DC-0005's scope rather than a hypothetical.
> - **grill-me / grill-with-docs integration** → not revived; producer-side
>   work is out of scope until the kernel question answers.
> - **GPT-Pro's five pressure points** (IN-20260612-7d2c) → still open
>   amendment candidates; the signed-vs-pre-signing provenance mismatch is
>   subsumed by DC-0005's approval/digest work.
> Everything below is preserved as the reasoning trail.

~~Open gate: Pyro has not yet reviewed/signed the four concept docs (notably
the v0 scope cut in docs/concepts/03).~~ **GATE CLOSED 2026-06-12 late
night — Pyro approved the concepts** and authorized plan-writing. Two
implementation plans written the same night (`docs/plans/2026-06-12-docket-
v0-plan-{1,2}-*.md`, per concepts/03's read-mostly-first sequencing option),
self-reviewed (5 fixes, incl. the D0-001 RFC-keyword self-reference the
recursive fixture caught at plan time), then Codie-reviewed via codex:rescue
(1 blocker: add --sign-unanchored dropped; 5 should-fix: overlap as state,
A3 command-token depth, bash-not-sh for process substitution, checklist on
inline signing, holding-suppression bug — ALL incorporated as design
decisions 1–26). Codie also simulated the door regexes against all 40
graduation-fixture clauses: zero false refusals. Next: execute plan 1.

2026-06-12 (later): Accord fork reconciled per Codie's verdict — see
DC-0002. Door is now A1–A9 ("the Accord"), rejections are three-typed,
`docket audit` added to v0, risk/evidence_required/scope fields adopted
lightweight. Concept docs updated in place; review gate above still open
and now covers the merged state.

Sequence after sign-off:
1. claude-knowledge crossings: sketches/docket.md + projects/docket.md.
2. Implementation plan against docs/concepts/03 (writing-plans).
3. Build v0 to the recursive fixture (docket-v0 contract imports through
   its own door, goes green under its own check).
4. Falsifier run: import a small variant-generated contract file, run one real
   fulfillment loop, watch the four refutation conditions (second spec
   reality, ledger drift, evidence decay, verdict fatigue).

Parallel work item (added 2026-06-12, Pyro): build the docket-emitting SFD
variant. Source material copied into `.agents/skills/surface-first-development/`
(provenance + the 4-point delta in its UPSTREAM.md); upstream 0.7 spec
copied to `docs/upstream/`. Variant is developed here against the door,
eventual home is limitless (producer side).

Parallel work item (added 2026-06-12, late evening — Pyro): integrate
grill-me / grill-with-docs (mattpocock/skills@grill-me, 305K installs;
grill-with-docs adds inline ADR/CONTEXT.md output) into the SFD variant as
the question-driven producer path for surfaceless work — SFD's own "When
NOT to Use" list (no meaningful interaction surface, complexity below the
surface). Shape: either a fallback mode inside the variant or a sibling
"grill" variant. Core move: every resolved branch of the grilling decision
tree lands as a clause-log entry at birth (grill-with-docs' ADRs ≈ the
decision log / the why), then compiles through Phase 5 + self-admission +
round-trip exactly like surface-derived clauses. Second horse, same door.
Caveat from the analysis: questions catch what surfaces hide (invariants,
failure policy); surfaces catch what questions can't name (gestalts) —
fallback, not replacement. Feeds upstream SFD 0.7 in limitless eventually.

Falsifier note (same evening): tipsy's signed bundle (16 admissible
clauses, docs/dojo/runs/pressure-tipsy/) is the leading candidate for
docket v0's first real fulfillment run — Phase 6 as fixture resurrection.

2026-06-12 (night): GPT-Pro review of the mdtodo graduation bundle, relayed
by Pyro — verdict "a very strong first real specimen." Names the round-trip
pattern **blind surface replay** (contract reconstructability test) and
reframes the SFD bundle as a *prosecution file* (contract = what agents
consume; bundle = how humans audit the law's birth). Five pressure points
filed as review-gate inputs in memory/inbox/IN-20260612-7d2c: PENDING-HARNESS
visibility, signed-vs-pre-signing provenance mismatch in the mdtodo fixture
(verified real — contract.yaml signed block vs decision-log line 68), A8
atomicity-by-gestalt doctrine (C-003 test case), open questions as a
first-class audit view ("signed darkness"), named benchmark-environment
artifact for NFR evidence. Proposes mdtodo as the golden *import* fixture
for D0-007 — complements tipsy as the *fulfillment-run* candidate (import
fixture ≠ fulfillment case). KG layer-crossings done the same night:
sketches/docket.md + projects/docket.md dossier filed in claude-knowledge,
review captured for /distill.

Watch items: docker-typo annoyance in practice; whether A4's MUST-pedantry
or A6's number-demands annoy real authoring (Pyro flagged the question);
whether verdict:human becomes a lazy-clause backdoor (count them);
guardian Goodharting (Pyro, 2026-06-12 late): the hollow-oracle attack — agent
authors both work and harness, test always passes, ledger green over broken
reality. Mechanically undetectable by design (boundary discipline). v0
defenses: first-verdict-reads-the-harness discipline, A9 multi-kind
evidence, falsifiers #2/#3 watching for ledger drift / evidence decay.
The structural seam: law is signed, the oracle it points to arrives later
(PENDING-HARNESS) and is never re-signed. If the falsifier run shows decay,
the pre-registered lesson applies (door extends to evidence admission) and
the Proofroom verifier-independence thread (KG thread 9) graduates from
research to requirement.
