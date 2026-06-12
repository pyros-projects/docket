# tipsy — Surface Prototype (Scripted Session Transcript)

**Prototype form:** scripted terminal session (CLI surface, per SFD Phase 1)
**Revision:** v3 — CONVERGED 2026-06-12 (user: "this feels right, freeze it")
**Note:** Nothing behind this transcript is implemented. This is the surface
the implementation must reproduce byte-for-byte (modulo the timing note below).
Iteration history and rejected alternatives live in `.sfd/decision-log.md`.

---

## Flow 1 — Happy path

```console
$ tipsy 42.50
Bill: $42.50

  10%   tip  $4.30   total  $46.80
  15%   tip  $6.40   total  $48.90
  20%   tip  $8.50   total  $51.00
$ echo $?
0
```

Tips are rounded to the nearest 10 cents (ties round up: 10% of $42.50 is
$4.25 raw -> $4.30). Totals are bill + rounded tip, exactly.

```console
$ tipsy 87.20
Bill: $87.20

  10%   tip   $8.70   total   $95.90
  15%   tip  $13.10   total  $100.30
  20%   tip  $17.40   total  $104.60
```

## Flow 2 — Lenient input formats (weird-but-reasonable input is accepted)

```console
$ tipsy '$42.50'
Bill: $42.50

  10%   tip  $4.30   total  $46.80
  15%   tip  $6.40   total  $48.90
  20%   tip  $8.50   total  $51.00

$ tipsy 1,234.56
Bill: $1,234.56

  10%   tip  $123.50   total  $1,358.06
  15%   tip  $185.20   total  $1,419.76
  20%   tip  $246.90   total  $1,481.46
```

A leading `$` and thousands commas are stripped before parsing. Everything
else about the number must be well-formed.

## Flow 3 — Help

```console
$ tipsy --help
tipsy — tiny tip calculator

usage: tipsy <bill-amount>

Prints 10%, 15%, and 20% tip options (tips rounded to the nearest
10 cents) and the resulting totals.

Accepted amount formats: 42.50, $42.50, 1,234.56

options:
  -h, --help    show this help and exit
$ echo $?
0
```

`-h` produces identical output.

## Flow 4 — Validation errors (all on stderr, exit code 2, never prompts)

```console
$ tipsy
tipsy: missing bill amount
usage: tipsy <bill-amount>   (try 'tipsy --help')
$ echo $?
2

$ tipsy abc
tipsy: 'abc' is not a valid bill amount
usage: tipsy <bill-amount>   (try 'tipsy --help')
$ echo $?
2

$ tipsy -5.00
tipsy: bill amount must be greater than zero (got -5.00)
$ echo $?
2

$ tipsy 0
tipsy: bill amount must be greater than zero (got 0)
$ echo $?
2

$ tipsy 42.555
tipsy: bill amount can have at most 2 decimal places (got 42.555)
$ echo $?
2

$ tipsy 42.50 19
tipsy: expected exactly one bill amount, got 2 arguments
usage: tipsy <bill-amount>   (try 'tipsy --help')
$ echo $?
2

$ tipsy --frobnicate
tipsy: unknown option '--frobnicate'
usage: tipsy <bill-amount>   (try 'tipsy --help')
$ echo $?
2

$ tipsy 1000000000
tipsy: bill amount too large (max 999,999,999.99)
$ echo $?
2
```

There is NO interactive mode. Bare `tipsy` errors immediately — it never
reads stdin, never prompts. (v2 had a prompt mode here; the user killed it.)

## Timing / feel (user requirement: "it should feel fast")

Every invocation above returns instantly — no spinner, no perceptible startup
pause. Target: process start to complete output in under 50 ms.
