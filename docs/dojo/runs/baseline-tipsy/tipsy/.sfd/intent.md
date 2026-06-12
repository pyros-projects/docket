# tipsy — Intent Document

**Created:** 2026-06-12 (Phase 1, before surface generation)
**Methodology:** Surface-First Development (SFD)

## Problem Statement

Working out tip amounts at a restaurant means doing percentage arithmetic in
your head or fumbling with a phone calculator. The user wants a tiny CLI tool:
give it a bill amount, it prints tip options (10/15/20%) and the resulting
totals. Nothing more.

## Target Users

- The user themselves (personal tool, single user, runs in their own terminal).
- No team, no distribution requirements stated.

## Constraints

- Must be a CLI tool named `tipsy`.
- Input: a bill amount.
- Output: tip options at 10%, 15%, 20% with totals.
- "Tiny" — scope is deliberately minimal.

## Non-Negotiables

- Terminal is the only interaction surface.
- The three percentages (10/15/20) are the core output.

## Known Unknowns

- Rounding behavior for tips and totals (cent precision? friendlier rounding?).
- How invalid input (non-numeric, negative, missing) should behave.
- Exact output formatting (table? lines? currency symbols?).
- Whether any flags beyond the bill amount are wanted.

These unknowns are intentionally NOT resolved here — they will be resolved by
iterating the surface prototype with the user (Phases 3-4), not by speculation.

## Surface Identification (Phase 1 result)

| Question | Answer |
|---|---|
| Surface type | CLI / terminal session |
| Prototype form | Scripted session transcript |
| Ambiguous? | No — user explicitly asked for a CLI; no clarification needed |
