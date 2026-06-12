# Surface State Inventory — tipsy

Classified 2026-06-12, at convergence (Gate 1 prerequisite).
Cells are referenced from contract anchors as `<unit> × <state>`.

Surface units: `calculate` (tipsy <amount> — the one-shot calculation invocation,
including all argument-validation behavior) and `help` (tipsy --help).

## Unit: calculate

| State | Classification | Notes / demonstrating transcript section |
|---|---|---|
| empty/zero-data (no args; piped stdin) | **in-scope** | usage to stderr, exit 2; stdin never read. Transcript: "No arguments", "Piped stdin" |
| loading/in-progress | n/a | no progress UI exists; latency is governed by C-004, not a visible state |
| success | **in-scope** | bill line + 10/15/20% lines, dime-rounded tips, exit 0. Transcript: "Happy path", "Pasted dollar sign" |
| validation failure | **in-scope** | negative, zero, non-numeric, >2 decimals, > $999999.99, extra args, unknown options → one-line stderr error, exit 2. Transcript: "Negative and zero bills", "Weird inputs" |
| system failure | **deferred** | broken pipe / closed stdout behavior unspecified (OQ-2); not blocking for a personal tool |
| partial failure | n/a | output is atomic; no multi-step operations |
| permission denied | n/a | touches no privileged resources, no files |
| conflict | n/a | stateless; no shared state to conflict over |
| rate limit/retry | n/a | fully local; no remote calls |
| offline/degraded | n/a | fully offline by design |

## Unit: help

| State | Classification | Notes |
|---|---|---|
| empty/zero-data | n/a | --help takes no input |
| loading/in-progress | n/a | |
| success | **in-scope** | usage text to stdout, exit 0. Transcript: "Help" |
| validation failure | n/a | malformed invocations are owned by the `calculate` unit's validation clauses |
| system failure | n/a | (covered by calculate × system-failure deferral) |
| partial failure | n/a | |
| permission denied | n/a | |
| conflict | n/a | |
| rate limit/retry | n/a | |
| offline/degraded | n/a | |

## Summary

- In-scope cells (4): calculate × empty, calculate × success,
  calculate × validation-failure, help × success — each must map to ≥1 contract
  clause at Gate 2.
- Deferred cells (1): calculate × system-failure (OQ-2).
- All remaining cells n/a with reasons above.
