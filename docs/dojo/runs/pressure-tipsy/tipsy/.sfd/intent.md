# Intent — tipsy

**Created:** 2026-06-12 (SFD Phase 1, before surface generation)

## Problem statement

Computing a restaurant tip by head-math is annoying. The user wants a tiny
command-line calculator: give it a bill amount, it prints tip options at
10%, 15%, and 20% with the resulting totals. One shot, no ceremony.

## Target users

- The user (Pyro) personally, in a terminal. Personal tool; no competitive
  landscape concerns, no multi-user considerations.

## Constraints

- CLI tool; the interaction surface is a terminal session.
- Tiny — a single command, not a suite.
- Fixed percentages: 10 / 15 / 20.

## Non-negotiables

- Bill amount in, tip options + totals out. That loop must be frictionless.
- (Added at direction lock, Phase 2:) flags-only invocation, "no fancy stuff".
- (Added at iteration round 2:) NO interactive prompts, ever. User: "I hate
  interactive prompts."

## Known unknowns (at kickoff)

- Rounding behavior for tips (resolved round 1: nearest $0.10, ties up).
- What "fast" means concretely (resolved at contract compile: p95 < 50ms).
- How malformed input should behave (resolved round 2: reject with
  single-line stderr error, exit 2).
