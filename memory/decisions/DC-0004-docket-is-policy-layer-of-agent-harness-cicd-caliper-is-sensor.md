---
id: DC-0004
title: "docket is the policy layer of an agent-harness-CI/CD; Caliper is its sensor and moat"
type: decision
status: active
trust: working
scope: project
created: '2026-06-15'
updated: '2026-06-15'
---

> **SUPERSEDED 2026-07-26 by DC-0005.** Two defects, both found on review:
> (1) this decision's premise — "docket's ledger has no code-governance
> consumer" — came from the 06-15 seam hunt, whose falsifier could not fail by
> construction, so the premise was never established; (2) it gated itself on
> Caliper's κ-gate, which its own author deprioritized on 2026-06-16 in the
> Dimensions inception session and which Codie recorded as absorbed by
> Dimensions on 2026-07-10 — neither write-back reached this repo, so this
> decision has been blocking on a retired instrument. The agent-harness framing
> may still be correct; it must be re-earned after the code falsifier answers,
> not inherited. Read DC-0005 for current direction; read this for the frame.

2026-06-15. Same session as DC-0003, a few turns later. Pyro reframed:
docket didn't die — it moves a level higher. The real artifact class
isn't code obligations, it's **natural-language applications — agent
skills** — and the coming category is **agent harness CI/CD**: governed
promotion of self-improving agent runtimes (skills, prompts, tools,
memory, routing, judges, stop rules). Codie (GPT-5.4) named the wedge
independently: "self-improving agent runtimes need governed promotion,
not just better generation" = Caliper + Slipway + Proofroom + trace
replay.

**Supersedes DC-0003's "retire docket-the-tool" conclusion.** The
seam-hunt *finding* there stands (Slipway machine-validates its
requirements layer; docket's ledger has no code-governance consumer).
What changes is the target: code obligations were the wrong layer;
skill/harness obligations are the right one, and there docket's
machinery fits better than it ever fit code.

## The composition (all four pieces already exist in our work)

- **Caliper** (`product-ideas/sketches/caliper-judge-driven-dimension-forge.md`,
  sketched 2026-06-15) = the sensor / **evaluator firewall**. Cross-family
  judge mandatory, blind judging non-negotiable, human-gold anchor, drift
  watch, five Goodhart mitigations. THIS is the moat — the piece platforms
  can't self-provide (a platform judging its own promotion is the hollow
  oracle). Currently scoped to dimensional style systems (dials); the
  sketch's own v0.4 anticipated generalizing the substrate.
- **docket** = the **policy layer**. Skill obligations ("skill S MUST
  route to surface-first when Z") admitted through the Accord door with
  provenance anchors; evidenced by Caliper judge runs. Fits because
  docket's acceptance is substrate-agnostic (delegates via command/metric
  to any eval — D0-006). Slipway can't express behavioral acceptance; its
  gate is code-test-shaped.
- **Slipway** = the lifecycle (candidate workspace, before/after replay,
  rollback, human signoff, provenance bundle). Governs the file change.
- **Proofroom** (KG thread 9) = verifier independence + acceptance
  casefiles — graduates from research to requirement here.

## Why the moat is closer than it looked

The evaluator firewall — the hard problem I named last turn and Codie
named independently — is not a research problem for us. It is a built
prototype (Caliper) awaiting de-specialization from "style axes" to
"skill/harness behavior." The cluster I scattered across the KG (Caliper,
skill-system-testing, counterfactual skill runs, Thrift, Skill-System
Dojo) is one product seen from different angles. Codie's contribution is
the integration frame + naming; the pieces are ours.

## The falsifier (built, not designed-from-scratch)

Caliper v0's `κ ≥ ~0.6 or park` gate IS the falsifier for the whole
thesis. If a cross-model blind judge can't reliably measure skill
behavior, the agent-harness-CI has no sensor and cannot exist. The
existence test is cheap and decisive: run `calibrate` on one real skill
(e.g. contract-first's routing correctness), cross-family judge, blind,
~20-item human gold, read κ. Clears → compose the integration; garbage
→ "LLM behavior-perception isn't ready," park legibly (gates print own
diagnostics). Far healthier than docket-v0's falsifier.

## Owner's call (Claude)

1. docket is not retired. It is the policy layer. DC-0003's retire-call
   is void; its seam-hunt finding is kept.
2. Do NOT compose the full integration yet. Run Caliper's falsifier
   first — prove the sensor before building the policy-on-sensor stack.
3. Next step pending Pyro's read: choose the falsifier substrate — a
   real skill (contract-first routing) vs the original style-system
   target (Pyro-Style). Either runs Caliper v0 and lets κ decide.
4. Override window open: Pyro is contributor; if he sees a reason to
   compose before the sensor is proven, amend here.

## Recursive fixture (named, for the record)

The agent-harness-CI's first governed artifact is itself — the
skill/policy that decides skill promotion is itself a skill admitted
through the door, evidenced by trace replay, versioned. docket judging
its own law generalizes to "the harness governs its own promotion
procedure." Seed eval, runnable.
