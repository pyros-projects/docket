# Clause Log — tipsy

Per-project monotonic C-NNN ids; these survive into `.contracts/tipsy.contract.yaml`
unchanged. Logged at birth, not retrospectively.

## Iteration round 1 (2026-06-12)

- [C-001] Given exactly one valid bill amount argument, tipsy MUST print to stdout a
  bill line plus one tip-option line each for 10%, 15%, and 20% (ascending), each
  showing the rounded tip and the resulting total.
  born: iteration round 1, "looks ok" — user accepted the round-0 output shape
  state-cells: calculate × success

- [C-002] Tips MUST be rounded to the nearest $0.10, ties rounding up.
  born: iteration round 1, in response to "tips should be rounded to the nearest 10 cents"
  state-cells: calculate × success

- [C-003] Each displayed total MUST equal the parsed bill amount plus that line's
  rounded tip, exact to the cent.
  born: iteration round 1, consequence of dime rounding (totals follow the rounded
  tip, not the raw percentage) — accepted with the rounding change
  state-cells: calculate × success

- [C-004] Invocation-to-output MUST complete in under 50ms at p95 on the reference
  machine.
  born: iteration round 1, in response to "it should feel fast" — quantified
  provisionally at 50ms p95; threshold to be confirmed via options at contract compile
  state-cells: calculate × success

- [C-005] tipsy MUST reject zero and negative bill amounts with a single-line error
  on stderr and exit status 2, writing nothing to stdout.
  born: iteration round 1, in response to "what happens with a negative bill?" —
  proposed rejection behavior, accepted by user in round 2 ("good")
  state-cells: calculate × validation-failure

## Iteration round 2 (2026-06-12)

- [C-006] tipsy MUST NOT read stdin under any invocation — no interactive mode
  exists.
  born: iteration round 2, in response to "kill it, flags only, I hate interactive
  prompts" — rejection of the round-1 no-args interactive prompt mode
  state-cells: calculate × empty

- [C-007] Invocation with no arguments MUST print usage to stderr and exit status 2.
  born: iteration round 2, replacement behavior for the killed interactive mode
  state-cells: calculate × empty

- [C-008] tipsy MUST reject non-numeric input with a single-line error on stderr
  naming the rejected input, and exit status 2.
  born: iteration round 2, in response to "it should handle weird inputs sensibly"
  state-cells: calculate × validation-failure

- [C-009] A single leading "$" on the amount argument MUST be accepted; output is
  identical to the same invocation without it.
  born: iteration round 2, weird-inputs policy (people paste "$20"), accepted at freeze
  state-cells: calculate × success

- [C-010] Amounts with more than two decimal places MUST be rejected with a
  single-line error on stderr and exit status 2.
  born: iteration round 2, weird-inputs policy (bills have at most cents), accepted
  at freeze
  state-cells: calculate × validation-failure

- [C-011] Amounts greater than 999999.99 MUST be rejected with a single-line error
  on stderr and exit status 2.
  born: iteration round 2, weird-inputs policy (keeps money math in exact range),
  accepted at freeze; cap value confirmed via options at contract compile
  state-cells: calculate × validation-failure

- [C-012] Invocations with more than one positional argument MUST be rejected with
  usage on stderr and exit status 2.
  born: iteration round 2, weird-inputs policy, accepted at freeze
  state-cells: calculate × validation-failure

- [C-013] `tipsy --help` MUST print usage text to stdout and exit status 0.
  born: iteration round 2, demonstrated in round 0 and round 2 transcripts, accepted
  at freeze
  state-cells: help × success

- [C-014] Error messages MUST NOT contain stack traces, jargon, or multi-line dumps —
  one human-readable line per failure.
  born: iteration round 2, in response to "handle weird inputs sensibly"
  state-cells: calculate × validation-failure

- [C-015] tipsy MUST reject any option other than `--help` with a single-line error
  on stderr naming the unknown option, and exit status 2.
  born: iteration round 2, weird-inputs policy + "no fancy stuff" direction lock
  (no hidden flag surface), accepted at freeze
  state-cells: calculate × validation-failure

## Contract compile (2026-06-12, Phase 5)

- [C-016] A successful calculation MUST exit with status 0.
  born: contract compile — coverage gap: the converged transcript demonstrates
  `echo $?` → 0 on success, but no iteration-round clause pinned it
  state-cells: calculate × success
