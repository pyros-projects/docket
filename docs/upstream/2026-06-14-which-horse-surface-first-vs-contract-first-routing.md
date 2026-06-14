# Which horse? — routing between surface-first and contract-first

**Date:** 2026-06-14
**Status:** routing note, shared by both producer skills. Both skills'
descriptions point here so the dispatcher routes correctly and the selection
rule is not duplicated (duplicated rules drift).
**Scope:** upstream material (producer-side), filed in `docs/upstream/` beside
the two skill designs. Docket-the-tool is producer-agnostic and ignores this.

---

## One question: where does the authority live?

The two producer skills are not opposing methodologies and neither is the
"modern" option. They are selected by **the source of the clauses**.

- **Tacit, in a human's head** → **surface-first.** The human knows what they
  want when they see it but cannot specify it from a blank page. Extract the
  authority by converging a concrete artifact they can react to (UI, doc,
  knowledge tree — see the surface-first generalization). Recognition over
  generation.
- **External and fixed** → **contract-first.** The obligation already exists in
  checkable form: a regulation, an SLA, an API compatibility spec, a legacy test
  suite, a security policy, a compliance framework. There is nothing to
  converge — the law is the law. Compile the authority into clauses.

## Decision table

| Signal | Surface-first | Contract-first |
|---|---|---|
| Authority source | a human who can react to a concrete artifact | a document/spec that already states obligations |
| Can you point at the authority? | no — it is tacit, must be surfaced | yes — it exists on disk / in a regulation / in a table |
| Does the authority carry numbers/tests already? | often no (you add them at compile) | usually yes (SLA has thresholds, tests exist) |
| Is convergence appropriate? | yes — the point is to shape it | no — you do not get to shape given law |
| Output | `.contract.yaml` through the Accord | `.contract.yaml` through the Accord (same door) |

## The collision guardrail

The failure mode is reaching for **contract-first** when you should use
**surface-first**, because writing contracts feels more rigorous than
prototyping. That slide rebuilds spec-first by accident (the Flock A/B failure:
17 spec-driven requirements → the wrong abstraction).

Contract-first's precondition gate is the backstop: **if you cannot point at
where the authority already lives, you are in surface-first territory.** "The
user roughly has it in mind" is not authority; that is tacit knowledge waiting
to be surfaced.

The reverse collision is rarer but real: do not surface-first a regulated
domain to "discover" a more convenient obligation set. Given law is not a
prototype to react against.

## What is shared, what differs

- **Shared (one `references/`):** the contract-emission schema, the Accord door
  checks A1–A9, the `.contract.yaml` format, the round-trip *principle*
  (sufficiency is tested, not asserted).
- **Differs (everything upstream):** surface-first converges then derives;
  contract-first locates then compiles. Different preconditions, different
  clause-log semantics (at-birth during iteration vs extraction provenance),
  different anchor sources (inventory cells vs authority passages), different
  Handoff Bundles (seven artifacts vs four).

Both terminate at `docket import`. The door does not care which horse arrived.

## See also

- `2026-06-14-contract-first-skill-given-authority-horse.md` — the contract-first
  skill design (this note's companion).
- `2026-06-12-sfd-0.7-contracts-are-the-product-design.md` — the surface-first
  variant's contract-quality levers (the door-side machinery both skills reuse).
- `docs/concepts/00-docket-why-and-what.md` — "many horses, one door," the
  thesis this routing operationalizes.
