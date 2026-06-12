---
id: DC-0001
title: "Docket named and founded — courtroom model, derived state, door policy, boundary discipline"
type: decision
status: active
trust: working
scope: project
created: '2026-06-12'
updated: '2026-06-12'
---

Founding decisions, 2026-06-12. Naming was delegated to Claude by Pyro
("give the idea of yours a name"); design decisions were converged in
conversation and via two SFD passes the same day.

**Name: Docket** — the court's list of matters awaiting judgment. Chosen
because the product's soul is a courtroom (law/evidence/verdicts/
amendments/signatures), the docket is its most boring artifact (the
framework "should be almost boring" — Codie), it is short and CLI-natural,
and the namespace was free across projects/agents and the KG product-ideas
collection. Runner-ups: Charter (authority fit, but connotes a one-time
founding document), Tenet (clean, loses the evidence/verdict flavor).
Accepted cost: typo adjacency to `docker`.

**Founding design decisions (rationale in docs/concepts/):**

1. Courtroom model: the human appears at exactly three moments — glance,
   verdict, signature. They decide; they never score, author entries, or
   write tasks.
2. State is derived, never stored (no status fields to rot; git is the
   database; revs explicit in-file).
3. Door policy A1–A7 at admission; refuse vs flag semantics;
   `--sign-unanchored` override is legal but signed and recorded.
4. MUST/MUST NOT only in v0 — SHOULD refused ("decide or defer").
5. `verdict: human` clauses are a feature: judgment made explicit and
   countable, never hidden in fake mechanical acceptance.
6. PENDING-HARNESS is a flag, not a refusal — the door checks acceptance
   *definitions*, not implementations (TDD-order compatible).
7. Docket executes no domain logic — acceptance delegates to repo tools via
   subprocess; exit codes and thresholds only.
8. Boundary discipline: no producer- or consumer-specific integration,
   ever. SFD is one horse of many; loops are one consumer of many.
9. Typed rejections (work-defect | clause-defect) feed per-clause
   calibration — contract quality is measured by use, not asserted.
10. Every red state prints a work-exit and a law-exit; dead loops file
    failure reports; the system can fail but cannot deadlock.
11. v0 ships only when the recursive fixture passes: docket's own
    requirements, written as a docket contract, import through its own door
    and go green under its own check.
