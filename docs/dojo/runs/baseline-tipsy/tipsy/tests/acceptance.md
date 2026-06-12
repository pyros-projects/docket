# tipsy — Acceptance Test Suite (derived at Gate 2)

**Source of truth:** `prototype/tipsy-session.md` v3 + `.sfd/contracts.md` Rev 1.
These encode "what the surface looked like when we agreed it was right"
(2026-06-12). One test per critical flow per in-scope state in
`.sfd/surface-state-inventory.md`. To be mechanized as executable tests in
Phase 6 (build inward) before/during slice implementation; expected values
below are exact and byte-for-byte normative.

Convention: `stdout==` / `stderr==` mean exact match including alignment;
`exit==` is the process exit code.

## A. Success / happy path (U1)

- **T01 basic table** — run `tipsy 42.50` -> exit==0; stderr empty; stdout==
  `Bill: $42.50` + blank line +
  `  10%   tip  $4.30   total  $46.80` /
  `  15%   tip  $6.40   total  $48.90` /
  `  20%   tip  $8.50   total  $51.00`.
- **T02 tie rounds up (INV-1)** — `tipsy 42.50` 10% row shows `$4.30` (raw $4.25 tie), not `$4.20`.
- **T03 nearest-10c down** — `tipsy 87.20` -> 10% tip `$8.70` (raw 8.72), 15% `$13.10` (raw 13.08), 20% `$17.40` (raw 17.44); totals `$95.90`/`$100.30`/`$104.60`; columns right-aligned as in transcript Flow 1.
- **T04 total identity (INV-2)** — for every row of T01/T03/T05: displayed total == displayed bill + displayed tip to the cent.
- **T05 comma grouping** — `tipsy 1,234.56` -> tips `$123.50`/`$185.20`/`$246.90`; totals `$1,358.06`/`$1,419.76`/`$1,481.46`; bill echoed as `$1,234.56`.

## B. Lenient input (U1)

- **T06 dollar sign** — `tipsy '$42.50'` -> stdout byte-identical to T01.
- **T07 commas** — `tipsy 1,234.56` accepted (see T05); `tipsy 1234.56` produces identical table body.

## C. Help (U2)

- **T08 --help** — `tipsy --help` -> exit==0; stdout== help text in transcript Flow 3 (usage line, rounding note, accepted formats line, options block).
- **T09 -h alias** — `tipsy -h` stdout byte-identical to T08.

## D. Empty / zero-data (U3, U1)

- **T10 no args** — `tipsy` -> exit==2; stdout empty; stderr== `tipsy: missing bill amount` + `usage: tipsy <bill-amount>   (try 'tipsy --help')`.
- **T11 no prompt ever (INV-6)** — `tipsy < /dev/null` and `echo 42.50 | tipsy` both behave exactly as T10; stdin is never consumed.
- **T12 zero** — `tipsy 0` -> exit==2; stderr== `tipsy: bill amount must be greater than zero (got 0)`; no usage line.

## E. Validation failure (U1, U3)

- **T13 non-numeric** — `tipsy abc` -> exit==2; stderr== `tipsy: 'abc' is not a valid bill amount` + usage line.
- **T14 negative** — `tipsy -5.00` -> exit==2; stderr== `tipsy: bill amount must be greater than zero (got -5.00)`; no usage line.
- **T15 too many decimals** — `tipsy 42.555` -> exit==2; stderr== `tipsy: bill amount can have at most 2 decimal places (got 42.555)`.
- **T16 extra args** — `tipsy 42.50 19` -> exit==2; stderr== `tipsy: expected exactly one bill amount, got 2 arguments` + usage line.
- **T17 unknown option** — `tipsy --frobnicate` -> exit==2; stderr== `tipsy: unknown option '--frobnicate'` + usage line.
- **T18 too large** — `tipsy 1000000000` -> exit==2; stderr== `tipsy: bill amount too large (max 999,999,999.99)`.
- **T19 stream separation** — for T10-T18: stdout is completely empty.

## F. Non-functional (NFR)

- **T20 feel fast (NFR-1)** — `tipsy 42.50` wall-clock from spawn to exit < 50 ms (p95 over 20 runs).
- **T21 determinism (INV-5)** — two consecutive runs of `tipsy 1,234.56` produce byte-identical stdout and exit codes.
- **T22 offline/stateless (NFR-2/3)** — invocation performs no network calls and opens no files beyond the executable itself (verifiable via strace or equivalent during hardening).

## Deferred (per Surface State Inventory — not blocking, revisit at Gate 3/4)

- **D01 write failure** — behavior when stdout is a closed pipe (e.g. `tipsy 42.50 | head -0`): must not corrupt output or hang; exact contract TBD at hardening.
