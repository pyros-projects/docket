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

**PIVOT (2026-06-15, owner's decision — DC-0003):** external review of
`signalridge/slipway` (mature Go lifecycle-governance CLI) concluded Slipway
has won the lifecycle-governor niche Plan 2 was reaching for. Plan 2's
courtroom is cut — building it would make docket a worse Slipway. Docket
narrows to its distinct thesis (portable contract + Accord door policy +
producer/consumer decoupling) and Slipway is reframed as docket's *consumer*,
not competitor. **SUPERSEDED same-session by DC-0004:** the "retire/narrow" conclusion
evolved — docket didn't die, it moved a level higher to **agent-harness
CI/CD** (governed promotion of self-improving agent runtimes; skills are
the natural-language applications). docket = policy layer; Caliper (the
LLM-as-judge firewall Claude sketched today) = sensor/moat; Slipway =
lifecycle; Proofroom = verifier independence. Plan 2's courtroom stays
cut (still redundant with Slipway). Next: run Caliper's κ-gate falsifier,
not compose. docket is agent-owned (Claude's call); Pyro is infra + contributor.

**Next steps:**
1. ~~Concept review~~ DONE — approved by Pyro 2026-06-12.
2. ~~KG hygiene~~ DONE 2026-06-12 night: `sketches/docket.md` +
   `projects/docket.md` dossier filed in claude-knowledge, GPT-Pro review
   captured for /distill.
3. ~~Implementation plan~~ DONE 2026-06-12 night: two plans in `docs/plans/`
   (plan 1: ledger/door/state read-mostly; plan 2: courtroom + recursive
   fixture), Codie review applied (1 blocker + 5 should-fix, all
   incorporated — see plan "Design decisions" 1–26).
4. ~~Execute plan 1 → Codie door review~~ DONE 2026-06-13 (night session):
   **branch `v0`, 19 commits, 73 tests green.** Subagent-driven execution,
   every task spec+quality reviewed with fixes (review trail in git log).
   Execution reorder 4→6→5 (runner before import CLI) eliminated the
   plan's stub dance. Both graduation bundles import clean: mdtodo 24/0,
   tipsy 16/0, zero door recalibration needed. Codie gate verdict: NO
   BLOCKERS, foundation safe for Plan 2; his five should-fixes all landed
   (threshold form refused at door, unit-strict metric matching,
   ledger-wide A5, all-refused reports cite checks, file clause-mismatch
   refused). Door also grew cross-contract A7 (clause ids per-project
   monotonic — concepts/01's own rule, now mechanical).
5. ~~Execute plan 2 (courtroom)~~ DEFERRED INDEFINITELY (DC-0003, 2026-06-15):
   Slipway ships the lifecycle-governance side better than docket would. The
   courtroom is cut, not paused — review/amend/sign reproduce Slipway.
   Carry-ins above stay on ice in case the distinct-thesis direction ever
   needs a write-side of its own.
6. ~~Seam hunt~~ DONE 2026-06-15 (DC-0003 UPDATE). Slipway machine-validates
   its requirements layer (REQ-NNN + GIVEN/WHEN/THEN + traceability, in the
   engine, fail-closed). No external-obligation-import seam exists. The
   docket ledger has no consumer Slipway doesn't already serve → portable-
   ledger thesis largely refuted. Docket's surviving value = provenance
   anchors + RFC-2119 admission discipline (A4/A6/A8/A9) + external-authority
   production mode. Natural bridge is producer-side: contract-first skill
   emits Slipway-native requirements.md, not docket .contract.yaml.
7. **RESOLVED 2026-06-15 (DC-0004):** none of (a/b/c) — docket reframed as
   the **policy layer of agent-harness CI/CD**, not retired. The governed
   artifact is the agent runtime (skills/prompts/tools/judges); skills are
   the natural-language applications. docket's door+contracts = policy;
   Caliper = the evaluator firewall / sensor (the moat — already prototyped);
   Slipway = lifecycle; Proofroom = verifier independence. Plan 2 courtroom
   stays cut (redundant with Slipway). Next real step: run Caliper's κ-gate
   falsifier on one real skill (contract-first routing) — prove the sensor
   before composing the integration. Owner: Claude; Pyro is contributor + infra.

**Related vault material (claude-knowledge):** capture
`2026-06-12-sfd-produces-contracts-not-specs-three-way-convergence` (queued,
claims 143+); capture
`2026-06-12-gpt-pro-docket-review-blind-replay-prosecution-file` (pending
/distill); `sketches/docket.md` (idea-layer record) + `projects/docket.md`
(routing dossier); obs-007 (merge reflex / layer physics); agent-work-acceptance
thread 9 (Proofroom vocabulary — conceptual sibling, not a dependency).
