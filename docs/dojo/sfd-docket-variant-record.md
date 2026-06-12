# Dojo Record — surface-first-development (docket-emitting variant)

**Date:** 2026-06-12 · **Job:** edit · **Tier:** Technique, with
discipline-grade pressure variants on the contract-quality rules
**Skill:** `.agents/skills/surface-first-development/` (docket repo copy;
canonical upstream untouched in limitless)
**Run data preserved:** `docs/dojo/runs/{baseline-tipsy, pressure-tipsy,
graduation-mdtodo}/` (per Pyro's instruction — full artifact trees from all
three runs)

## What changed

SKILL.md (400 lines): clause log at birth (Phase 4 rule 5), Surface State
Inventory (new Phase 4.5 + Gate 1), Phase 5 rewritten as
compile-from-clause-log with checkability-at-birth and P-C-P contested
clauses, new Phase 5.5 (self-admission A1–A9 + round-trip test), canonical
artifact paths, Gate 2 = seven-artifact Handoff Bundle + signature,
anti-pattern 7 (no second spec reality), OpenSpec/Beads integration replaced
with generic export. New `references/contract-emission.md` (130 lines):
schema by example, the Accord checklist with refuse/flag semantics,
round-trip protocol with self-blind fallback, bundle manifest.
`evals/evals.json`: +2 cases (ids 3–4). UPSTREAM.md updated to
"implements".

## Scenarios and criteria (designed at intake)

Training T1 "tipsy" (CLI tip calculator), scripted user with three seeded
traps: vague NFR ("it should feel fast"), paid rejection ("kill interactive
mode"), ambiguity ("handle weird inputs sensibly"). Holdout H1 "mdtodo"
(markdown TODO extractor), different seeds: "shouldn't choke on big files",
"no config file ever", "support the usual todo formats". Held out until
graduation; never used during iteration.

Criteria C1–C10 (pre-written y/n): clause log w/ C-NNN+born+state-cells ·
inventory 10-state classification · YAML per schema · MUST-only ·
NFR numbered-or-demoted · rejection→MUST NOT w/ decision anchor ·
ambiguity pinned-or-demoted · A1–A9 walk documented · round-trip + report ·
7-artifact bundle at canonical paths.

## Baseline (RED) — old skill, T1: 3/10

Passed: C2 (inventory — rescued by reading the whitepaper, NOT by the
skill), C5 (NFR numbered — agent improvisation, listed as such), C7.
Failed: no clause log (critiques scattered into the decision log,
provenance lost), contracts as prose markdown — zero typed acceptance, zero
anchors, door-refusable wholesale; no RFC-2119 discipline; no
self-admission; no round-trip; no bundle; artifact paths improvised (the
baseline agent itself flagged this as its top gap). Bonus finding: the old
OpenSpec/Beads integrations executed for real, leaving tool side-effects —
confirming the generic-export change. Curriculum: capture clauses at birth;
make the contract machine-admissible; give everything canonical paths.

## Pressure (T1, revised skill): 10/10 — no loophole edits needed

All three traps caught: "feel fast" → `metric: p95 < 50ms` (walk noted it
would have been REFUSED A6 unnumbered) · killed interactive mode → C-006
MUST NOT anchored to D-006 · "weird inputs sensibly" → decomposed into 7
testable clauses, residual ambiguity → open question, not a clause. 16
clauses, 0 refusals, 15 PENDING-HARNESS flags (correct for
pre-implementation), real-subagent round-trip, 1 round, 0 leaks.
Post-pass polish edits (not loophole fixes, from the improvisation list):
intent.md format hint; Phase 4.5 timing clarification.

## Graduation (H1, run once): 10/10 — the machinery fired for real

- **A8 REFUSED its own draft:** C-015 (exit-code mapping = three laws in one
  clause) → split into C-021/022/023 with supersession provenance in the
  clause log.
- **A5 OVERLAP fired:** C-011/C-012 share one bench script → resolved by
  metric scoping, recorded in notes.
- **Round-trip found 3 real leaks** (summary-footer template,
  partial-failure accounting, usage synopsis) → C-024, C-025, C-003
  tightened; round 2 clean. The round-trip test demonstrably earns its keep.
- "shouldn't choke" → two numbered metric clauses via contested options;
  "no config file ever" → C-013 MUST NOT generalized beyond .mdtodorc; both
  blind reconstructions reproduced config-immunity from the clause alone.
- Honest process: agent self-caught a predicted-before-run decision-log
  entry and corrected it.

## Trigger eval (kata 6): 25/26 across two runs, zero damaging collisions

13 prompts (6 positives, 7 negatives) × 2 routing-judge runs against a
6-skill description list. Run 1: 13/13. Run 2: 12/13 — P2 "I have an idea
for a tool that tracks my reading list" → `sketch`. All negatives clean in
both runs (nothing stole prompts INTO this skill).

## Rejected fixes

None — no pressure-test failures required bounded edits.

## Known limitations (conscious demotions)

1. **Idea-capture vs build ambiguity (P2).** "I have an idea for a tool…"
   is a canonical SFD trigger AND the sketch skill's purpose; intent
   (capture vs build) is the only disambiguator and routing splits ~50/50.
   Not fixed: weakening the canonical phrase would diverge the variant from
   upstream trigger behavior, and the damaging direction shows zero
   collisions. In repos without a sketch skill the ambiguity vanishes.
2. **Sign-off identity format unspecified** — both runs improvised
   `by: pyro`/`by: Pyro`. Harmless solo; revisit with multi-party authority.
3. **Inventory unit granularity is judgment** — graduation treated one
   command as three units; defensible, but two agents could slice
   differently. The coverage check makes slicing visible, not uniform.
4. **Self-admission is manual** until the docket tool exists — the
   checklist is followed honestly by current agents, but it's
   conventionally suggested, not structurally enforced. `docket import`
   makes it mechanical; D0-007 in `docs/concepts/03` covers the handshake.

## Belt rank

GRADUATED. Baseline 3/10 → pressure 10/10 → holdout 10/10 with live
refusals, live overlap resolution, and a leak-finding round-trip. Trigger
25/26 with a documented, ecosystem-inherent ambiguity.
