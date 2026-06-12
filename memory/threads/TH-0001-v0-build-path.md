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

Sequence after sign-off:
1. claude-knowledge crossings: sketches/docket.md + projects/docket.md.
2. Implementation plan against docs/concepts/03 (writing-plans).
3. Build v0 to the recursive fixture (docket-v0 contract imports through
   its own door, goes green under its own check).
4. Falsifier run: import flock feat/skills .sfd contracts, run one real
   fulfillment loop, watch the four refutation conditions (second spec
   reality, ledger drift, evidence decay, verdict fatigue).

Watch items: docker-typo annoyance in practice; whether A4's MUST-pedantry
or A6's number-demands annoy real authoring (Pyro flagged the question);
whether verdict:human becomes a lazy-clause backdoor (count them).
