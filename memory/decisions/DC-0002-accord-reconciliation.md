---
id: DC-0002
title: "Accord reconciled into Docket — product stays Docket, the door policy is named the Accord"
type: decision
status: active
trust: confirmed
scope: project
created: '2026-06-12'
updated: '2026-06-12'
---

Codie built a parallel draft of the same product at
`~/projects/agents/accord` (one commit, four concept docs, codies-memory
vault). Both drafts descended from the same 2026-06-12 design conversation.
Codie's verdict, relayed by Pyro: **Docket wins as the product** ("Docket
has the stronger ontology... you can feel the product"), Accord's best
ideas get stolen in. His merge phrasing, adopted verbatim as architecture:

> Docket is the repo's courtroom. Accord is the door policy that decides
> what becomes law.

## Ported from Accord (concept docs updated this date)

1. **Evidence defect** — third typed rejection reason (work | evidence |
   clause); each calibrates a different actor (implementation / filing
   agent's rigor / the law itself).
2. **A8 atomicity** — exactly one obligation per clause, refused at door.
3. **Coverage views** — `docket audit`; "completeness is inspectable, not
   provable; good enough when uncovered regions are visible and signed."
4. **Lightweight risk** — optional `risk:` + `evidence_required:` fields;
   A9 flags THIN-EVIDENCE on high-risk clauses with <2 evidence kinds.
   (This partially accepts Codie's critique that "nobody validates
   upfront beyond the door" was too relaxed — the door got stronger.)
5. **Optional `scope: {applies_to, excludes}`** — anti-scope-lawyering.
6. **validated ≠ proven** lifecycle vocabulary.
7. **Read-mostly-first** noted as a v0 sequencing option.

## Deliberately NOT ported

- **Five validator roles as schema fields** — demoted to the signing
  checklist printed by `docket sign`. Rationale: in a solo-authority world
  all five resolve to the same person (ceremony), and "desire validator"
  re-imports the decide-vs-score confusion — desire is decided, not
  validated. The five questions survive; the fields do not.
- **Gate-centered product identity** — Docket keeps the lifecycle center of
  gravity (courtroom forever, not validation-gate-then-done); verdict
  fatigue, not a weak door, remains the falsifier most likely to kill the
  product.
- Shipping Accord separately — it remains a reference draft in its own
  repo; Codie may record the supersession in his own vault.

## What Docket already had that Accord lacked (kept, unchanged)

Concrete surfaces (three moments, sessions as behavioral commitments),
dead-loop exits / failure reports (every red state prints a work-exit and a
law-exit), the recursive fixture, the SFD-variant working material.
