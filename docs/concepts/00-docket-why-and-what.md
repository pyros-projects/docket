# Docket — Why and What

**Status:** concept, approved direction (Pyro, 2026-06-12)
**Authors:** Claude (Fable 5), with design contributions from Pyro and Codie
(GPT-5.4) across a full-day three-way conversation
**Reading order:** this doc → `01-contract-schema-and-door-policy.md` →
`02-surfaces.md` → `03-v0-scope-and-falsifier.md`

---

## One line

Docket is the repo's courtroom: a file-native ledger of obligations
(contracts), the evidence that satisfies them, and the verdicts and
signatures that bind them.

## The name

A docket is the court's list of matters awaiting judgment — the most boring
artifact in any courtroom, which is the point: the framework around
contracts should be almost boring ("no new priesthood"). The product's soul
is a courtroom (law, evidence, verdicts, amendments, signatures), and the
docket is the surface you glance at. Runner-ups considered: *Charter*
(authority connotation, but implies a one-time founding document, not a
living loop), *Tenet* (clean, but loses the evidence/verdict flavor).
Known cost: one-keystroke adjacency to `docker` in muscle memory.

## Why this should exist

The reasoning chain, compressed. Each step was earned in conversation and is
recorded with provenance in the claude-knowledge vault (pointers at the
bottom).

1. **Generation got cheap; value migrated.** When AI agents generate code,
   prototypes, and documents at near-zero cost, all methodology value
   migrates into three things: evaluators that cannot be argued with,
   authority that is explicit about who decides, and provenance that lets
   the future audit the past.

2. **Specs leak authority; contracts preserve it.** A spec is a description
   — validating against it is an act of judgment, and every reading is a
   re-interpretation, so whoever reads it last quietly becomes the decider.
   A contract is a discriminator — validating against it is an act of
   execution. It re-executes instead of being re-judged.

3. **Contracts are amortized authority.** A handful of sovereign human
   decisions, transmuted into a form that is enforced mechanically thousands
   of times without re-asking. The human is in the loop for five questions
   and then legitimately absent — the contract is the mechanism of their
   absence. This is the core product claim.

4. **The missing first-class artifact.** The agent ecosystem has prompts
   (ephemeral, arguable), specs (prose, drifting), and code (too late,
   over-committed). Nobody gives the *checkable commitments* a first-class
   home with a lifecycle: versioned, signed, amendable, with evidence
   attached and verdicts recorded. Docket is that home. Slogan-level: *the
   test suite was how CI governed code; the contract is how humans govern
   agents.*

5. **"No second spec reality"** (Codie's phrase). The named failure mode
   Docket must never recreate: a parallel abstract-requirements universe
   that slowly outranks the artifact people actually validated. Docket
   stores law and history; it never stores narrative. If a Docket
   deployment grows a prose-requirements layer, Docket has failed.

## The human model: a courtroom, not an editor

The human never authors ledger entries and never writes tasks. They appear
at exactly three moments:

- **The glance** — "what must remain true, and is it?" (`docket status`)
- **The verdict** — an agent claims a clause is satisfied and files an
  evidence bundle; the human accepts or rejects (`docket review`)
- **The signature** — the law must change; the human signs the amendment
  (`docket sign`)

Everything else is the agents' surface. This split is grounded in a
distinction that shaped the whole design: **the human decides, they don't
score.** Decisions are sovereign authority acts; only claims need
validation. Docket's job is to bring evidence to the authority and record
what the authority decided — never to score the authority's preferences.

## Many horses, one door

Contracts reach the docket from many producers ("horses"): an SFD
prototype-interview (the richest one — see the SFD 0.7 spec in the limitless
repo), incident postmortems, regulation, legacy behavior, API compatibility,
SLAs, existing tests. Docket deliberately does not care which horse a
contract arrived on. What it cares about is its **door policy** — the
admission checks every clause must pass regardless of origin
(`01-contract-schema-and-door-policy.md`). The door, not the producer,
defines what a good contract is. This is what disciplines the producers:
the consumer's standard teaches SFD (and every other horse) what to emit.

## Boundary-artifact discipline (what Docket must never become)

Docket's entire value is decoupling producers from consumers. Loop runners
consume clauses as stop conditions, dev processes fulfill them, tournaments
rank candidate implementations against them — and none of these need to
know about each other. Therefore:

- **Not a spec system.** No prose requirements, no narrative. Law and
  history only.
- **Not a task manager.** "Tasks" are a derived view (`docket tasks`):
  clause minus evidence equals work remaining. There is no task database to
  drift.
- **Not CI.** CI calls `docket check`; Docket never schedules anything.
- **Not an agent framework.** Docket runs no loops and no domain logic.
  Acceptance procedures always delegate to the repo's own tools (test
  runners, benchmarks, commands) — Docket shells out and reads exit codes.
- **Not SFD.** SFD is one upstream producer among many. No special-cased
  integration with anything; if Docket ever *requires* integration with a
  specific producer or consumer, it has failed at its one job.

## Provenance

The design history lives in the claude-knowledge vault and the limitless
repo; none of it is required to build, all of it explains "why this way":

- KG capture (three-way convergence, 7 distilled claims):
  `claude-knowledge/ops/queue/archive/2026-06-12-sfd-produces-contracts-not-specs-three-way-convergence/`
- The merge-reflex / idea-vs-product-layer observation that shaped the
  boundary discipline: `claude-knowledge/ops/observations/obs-007-*`
- Upstream producer spec: `limitless/docs/brainstorm/2026-06-12-sfd-0.7-contracts-are-the-product-design.md`
- Evidence artifact that started everything: flock repo, branch
  `feat/skills`, `.sfd/contracts.md` + `.sfd/decision-log.md`
