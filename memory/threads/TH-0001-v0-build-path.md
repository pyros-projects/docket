---
id: TH-0001
title: "v0 build path — review gate, KG crossings, plan, fixture, falsifier"
type: thread
status: active
trust: working
scope: project
created: '2026-06-12'
updated: '2026-06-12'
---

Open gate: Pyro has not yet reviewed/signed the four concept docs (notably
the v0 scope cut in docs/concepts/03).

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

Watch items: docker-typo annoyance in practice; whether A4's MUST-pedantry
or A6's number-demands annoy real authoring (Pyro flagged the question);
whether verdict:human becomes a lazy-clause backdoor (count them).
