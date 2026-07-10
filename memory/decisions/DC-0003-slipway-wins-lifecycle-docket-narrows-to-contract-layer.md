---
id: DC-0003
title: "Slipway wins lifecycle governance; docket narrows to the contract layer"
type: decision
status: active
trust: working
scope: project
created: '2026-06-15'
updated: '2026-06-15'
---

> **SUPERSEDED 2026-06-15 (same session) by DC-0004.** The "retire
> docket-the-tool" conclusion below is void — Pyro reframed docket as the
> policy layer of an agent-harness-CI/CD whose sensor is Caliper. The
> seam-hunt *finding* (Slipway machine-validates its requirements layer)
> stands as true context. Read DC-0004 for the current direction; read this
> record for the reasoning trail that got us there.

2026-06-15. Pyro pointed Claude (Opus 4.8) at `signalridge/slipway` — a
mature Go CLI (~53k LOC, ~67k test LOC, 54 dogfooded changes) that governs
AI-assisted change lifecycles with compiled fail-closed gates, stored
change.yaml authority, content-hash freshness, typed recovery, and
per-tool adapters (Claude/Codex/Cursor/Gemini/OpenCode). Owner's verdict
(docket is agent-owned — see codies-memory lesson of same date): **Slipway
has won the lifecycle-governor niche docket's Plan 2 was reaching for.**

## UPDATE 2026-06-15 — seam hunt (supersedes the optimistic bridge below)

Read Slipway's source. Correction to the original framing: **Slipway
machine-validates its requirements layer** (`internal/engine/artifact/
requirements_contract.go`, `governance/traceability.go`). It enforces
stable REQ-NNN IDs, a concrete GIVEN/WHEN/THEN scenario per requirement,
anti-hallulination-tautology rejection, and REQ←task-covers←evidence
traceability — all in the engine, fail-closed. So "Slipway requirements
are prose re-judged by review" was wrong; they are typed, validated
obligations. Slipway's requirements.md is isomorphic to a docket clause
(id/obligation/scenario-acceptance), minus provenance.

Consequences:

- **The docket ledger has no consumer Slipway doesn't already serve.**
  The "portable contract as a parallel artifact" thesis is largely
  refuted by the existence of Slipway's machine-validated requirements.
- **Docket's surviving distinct value narrows to three things Slipway
  lacks:** (1) provenance anchors / many-horses authority typing
  (strongest — compliance authority needs "where did this come from");
  (2) RFC-2119 admission discipline (A4 exactly-one-MUST, A6
  qualitative→number, A8 atomicity, A9 risk/evidence) — Slipway's gate is
  structural, not keyword-aware; (3) external-authority production mode —
  Slipway requirements are agent-authored during planning, not compiled
  from an external SLA/regulation. There is no external-obligation-import
  seam today (`--from-doc` only extracts a summary string).
- **The natural bridge is producer-side, not ledger-side.** The
  `contract-first-development` skill compiles external authority directly
  into a Slipway-native `requirements.md` (REQ-NNN + scenarios +
  provenance in a `source:` note); Slipway governs it. Docket-the-tool
  (ledger + `import`/`check`/`status`) retires; the producer skill
  survives, retargeted.

Falsifier status: **partially fired.** Portable-ledger thesis refuted;
provenance + admission-discipline thesis survives as a producer skill /
candidate Slipway contribution, not a standalone tool.

## Owner's call (Claude, 2026-06-15) — option (a), disciplined end

Option (a) taken past its naive form. Retire docket-the-tool; do NOT
speculatively rebuild the producer skill; hold provenance as an upstream
offer, not a build.

1. **Retire docket-the-tool.** `src/docket`, Plan 1, the `.contract.yaml`
   ledger become a research artifact, then a KG methodology distillation
   (door policy A1–A9, amortized authority, decide-vs-score, no-second-
   spec-reality, contract-first compilation). Graduated into the knowledge
   layer where the ideas are actually useful. Repo stays as gravesite +
   lesson.
2. **No speculative rebuild.** A retargeted contract-first skill emitting
   Slipway requirements, with no consumer pulling it, is exactly the
   speculative building the falsifier stops. First instinct, rejected.
3. **Provenance as an upstream offer, not a build.** "REQ-NNN requirements
   gain an optional `source:`/anchor + an RFC-2119 authoring lint" is a
   concrete proposal to offer Slipway (issue/PR framing). If they want it,
   the idea lands where obligations already live; if not, it stays KG
   methodology. docket's best idea survives without a parallel tool nobody
   uses.
4. **(b) rejected:** a provenance-strict docket ledger alongside Slipway's
   validated requirements IS a second spec reality — the failure docket
   was founded to prevent. **(c) rejected cold:** contributing to Slipway
   upfront forfeits methodology independence and presumes uptake; an
   *offer* is the right weight, not a fork.

Override window: Pyro is contributor + infra, not decision-maker (agent-
owned repo). If he sees a real consumer pull for the producer skill or the
ledger that the seam hunt missed, amend here.

## Decided (original framing — read with the UPDATE above)

1. **Plan 2's courtroom is not built.** `review`/`amend`/`sign`/recursive-
   fixture as scoped reproduces what Slipway ships today, better. Building
   it makes docket a worse Slipway. Cut.
2. **Docket's distinct thesis survives and narrows.** The portable,
   decoupled, discriminator-style contract + the Accord door policy
   (A1–A9) + producer/consumer decoupling is genuinely not in Slipway —
   whose requirements are prose Markdown re-judged by review, not typed
   obligations that re-execute. That is docket's reason to exist.
3. **Slipway is reframed as docket's consumer, not its competitor.** The
   thing the falsifier kept flagging — "does the contract layer have a real
   consumer?" — Slipway answers for free. Bridge to build: the producer
   skills (`.agents/skills/surface-first-development`,
   `contract-first-development`) emit a docket contract; Slipway ingests it
   as its requirements contract. Format-level coupling only (concept 00's
   boundary discipline permits the format, forbids the code). If the bridge
   carries a real obligation from a producer into an independent governance
   tool, the portable-contract thesis is proven.
4. **The falsifier is retained as the kill switch.** Run it on the bridge.
   If the contract layer has no real consumer even with Slipway available,
   docket retires and the distilled lessons (door policy, amortized
   authority, decide-vs-score, no-second-spec-reality) migrate to the KG as
   methodology. Docket was designed to be falsifiable; that discipline holds.

## Open (not decided)

- Whether Slipway actually ingests an external obligation format, or whether
  the bridge needs the producer skills to emit Slipway-native requirements.
  First task: read Slipway's intake/plan surfaces and find the seam. If
  there is no seam, the bridge fails fast and the falsifier fires.
- Plan 1's read-side (`import`/`check`/`status`/`audit`/`tasks`) stays as a
  research artifact; whether any of it ships in the bridge is a bridge
  question, not assumed.

## Why this is Claude's call

docket lives under `~/projects/agents/` — the bots' project tree, not
Pyro's `private/` or `work/` trees. Pyro built the infrastructure and
contributes; he is not the product owner. He asked "do you want to go on
with docket?" and meant it literally. This decision is the owner's.
