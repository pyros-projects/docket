---
title: docket-project-context
type: project-context
created: '2026-06-12'
updated: '2026-06-12'
---

# Docket — project context

**What:** the repo's courtroom — file-native ledger of obligations
(contracts), evidence bundles, verdicts, signatures. Core claim: contracts
are amortized authority (few human decisions, mechanically enforced many
times). Named failure mode to never recreate: "no second spec reality."

**State (2026-06-12, end of founding day):** concept phase complete AND the
producer side is built and verified. Four concept docs converged (full-day
three-way conversation, Pyro + Claude Fable 5 + Codie GPT-5.4, two SFD
passes). The Accord reconciliation (DC-0002) merged Codie's parallel draft:
door is A1–A9, rejections three-typed, `docket audit` in scope. The
**docket-emitting SFD variant** in `.agents/skills/surface-first-development/`
graduated the dojo (baseline 3/10 → pressure 10/10 → holdout 10/10; record
at `docs/dojo/sfd-docket-variant-record.md`, full run artifacts in
`docs/dojo/runs/` — the graduation contract files there are valid door
fixtures). Flock-as-demo is ruled out; fixtures come from variant runs.
The docket TOOL has no code yet. Pyro has NOT yet signed off on the v0
scope cut in `03` — that is the open gate.

**External review (2026-06-12, night):** GPT-Pro approved the concept via
the mdtodo bundle ("very strong first real specimen"), named **blind
surface replay** and the *prosecution file* reframe, and raised five
pressure points — recorded as review-gate inputs in
`memory/inbox/IN-20260612-7d2c-*` and in TH-0001. mdtodo proposed as the
golden import fixture (D0-007); tipsy remains the fulfillment-run candidate.

**Where this came from:** reading flock `feat/skills` `.sfd/` artifacts →
"SFD produces contracts, not specs" (Pyro) → decide-vs-score correction →
amortized-authority frame → Codie's "contract ledger → tasks → evidence
bundles, no second spec reality" → boundary-artifact discipline (docket
integrates with nothing) → two SFD passes converged surfaces and door.
Full provenance pointers in `docs/concepts/00`, bottom section.

**GATE CLOSED (2026-06-12, late night): Pyro approved the four concept docs.**
The GPT-Pro pressure points (inbox IN-20260612-7d2c) remain amendment
candidates for later — plans build against the concepts as approved.

**Next steps:**
1. ~~Concept review~~ DONE — approved by Pyro 2026-06-12.
2. ~~KG hygiene~~ DONE 2026-06-12 night: `sketches/docket.md` +
   `projects/docket.md` dossier filed in claude-knowledge, GPT-Pro review
   captured for /distill.
3. ~~Implementation plan~~ DONE 2026-06-12 night: two plans in `docs/plans/`
   (plan 1: ledger/door/state read-mostly; plan 2: courtroom + recursive
   fixture), Codie review applied (1 blocker + 5 should-fix, all
   incorporated — see plan "Design decisions" 1–26).
4. Execute plan 1 → Codie door review → execute plan 2 → recursive fixture
   green → Pyro signs rev1 (`docket sign rev1 --by pyro`).
5. Falsifier run on tipsy's signed bundle (one real fulfillment loop, watch
   the four refutation conditions).

**Related vault material (claude-knowledge):** capture
`2026-06-12-sfd-produces-contracts-not-specs-three-way-convergence` (queued,
claims 143+); capture
`2026-06-12-gpt-pro-docket-review-blind-replay-prosecution-file` (pending
/distill); `sketches/docket.md` (idea-layer record) + `projects/docket.md`
(routing dossier); obs-007 (merge reflex / layer physics); agent-work-acceptance
thread 9 (Proofroom vocabulary — conceptual sibling, not a dependency).
