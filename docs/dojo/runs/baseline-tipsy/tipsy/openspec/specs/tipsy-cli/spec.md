# tipsy-cli Specification

## Purpose

Capture the converged SFD surface and frozen contracts (Rev 1, 2026-06-12) for
`tipsy`, a flags-only CLI tip calculator: given a bill amount, print 10/15/20%
tip options and totals. Derived from `prototype/tipsy-session.md` v3 and
`.sfd/contracts.md`; this artifact persists the converged state across sessions.

## Requirements

### Requirement: Tip table on valid bill amount

`tipsy <bill-amount>` SHALL print to stdout a `Bill: $<amount>` line, a blank
line, and three rows for 10%, 15%, and 20% in the form
`  <pct>%   tip  <tip>   total  <total>`, with all amounts `$`-prefixed,
two-decimal, comma-grouped, and right-aligned per column, then exit 0.

#### Scenario: Standard bill

- **WHEN** the user runs `tipsy 87.20`
- **THEN** the table shows tips $8.70 / $13.10 / $17.40 and totals $95.90 / $100.30 / $104.60 and the exit code is 0

### Requirement: Tips round to the nearest 10 cents, ties up

Tip amounts SHALL equal the raw percentage of the bill rounded to the nearest
multiple of $0.10, with ties rounding up. Totals SHALL equal bill plus the
rounded tip exactly; totals are never rounded independently.

#### Scenario: Tie rounds up

- **WHEN** the user runs `tipsy 42.50`
- **THEN** the 10% tip displays as $4.30 (raw $4.25) and its total as $46.80

### Requirement: Lenient input normalization, strict validation

The bill argument SHALL accept an optional leading `$` and `,` thousands
separators (stripped before parsing) and SHALL otherwise be a positive decimal
number with at most 2 decimal places, no greater than 999,999,999.99.

#### Scenario: Dollar sign and commas accepted

- **WHEN** the user runs `tipsy '$42.50'` or `tipsy 1,234.56`
- **THEN** the command succeeds exactly as for the plain numeric forms

#### Scenario: Invalid inputs rejected

- **WHEN** the argument is non-numeric, zero, negative, has more than 2 decimal places, or exceeds the maximum
- **THEN** tipsy writes a single `tipsy: <message>` line to stderr, writes nothing to stdout, and exits 2

### Requirement: Flags only — no interactive mode

`tipsy` SHALL never read stdin or prompt. Invocation without arguments SHALL
fail with `tipsy: missing bill amount` plus a usage hint on stderr and exit 2.
This requirement is a user non-negotiable recorded at surface convergence.

#### Scenario: Bare invocation errors immediately

- **WHEN** the user runs `tipsy` with no arguments (even with data on stdin)
- **THEN** stderr shows the missing-amount error and usage hint, stdin is not read, and the exit code is 2

### Requirement: Help output

`tipsy -h` and `tipsy --help` SHALL print the converged usage text (usage line,
rounding note, accepted formats, options block) to stdout and exit 0.

#### Scenario: Help flag

- **WHEN** the user runs `tipsy --help` or `tipsy -h`
- **THEN** the converged help text is printed to stdout and the exit code is 0

### Requirement: Feels fast

A tipsy invocation SHALL complete (process start to full output) in under
50 ms at p95 on the user's machine, perform no network or file I/O, and produce
deterministic byte-identical output for identical invocations.

#### Scenario: Instant response

- **WHEN** the user runs `tipsy 42.50` twenty times
- **THEN** the p95 wall-clock duration is below 50 ms and all outputs are byte-identical
