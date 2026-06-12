# tipsy — converged surface prototype (scripted session transcript)

Round 2 — interactive mode removed (flags only), weird-input handling.
Frozen 2026-06-12 ("this feels right, freeze it").

## Happy path (tips rounded to nearest $0.10, ties up)

```
$ tipsy 42.50
Bill:  $42.50

  10%   tip $4.30    total $46.80
  15%   tip $6.40    total $48.90
  20%   tip $8.50    total $51.00
$ echo $?
0
```

```
$ tipsy 100
Bill:  $100.00

  10%   tip $10.00   total $110.00
  15%   tip $15.00   total $115.00
  20%   tip $20.00   total $120.00
$ echo $?
0
```

## Pasted dollar sign — accepted, identical to the bare number

```
$ tipsy '$20'
Bill:  $20.00

  10%   tip $2.00    total $22.00
  15%   tip $3.00    total $23.00
  20%   tip $4.00    total $24.00
$ echo $?
0
```

## Negative and zero bills — rejected, exit 2, nothing on stdout

```
$ tipsy -5
tipsy: bill amount must be a positive number (got: -5)
$ echo $?
2

$ tipsy 0
tipsy: bill amount must be a positive number (got: 0)
$ echo $?
2
```

## Weird inputs — one-line errors, exit 2

```
$ tipsy abc
tipsy: not a valid bill amount: 'abc'
$ echo $?
2

$ tipsy 12.345
tipsy: bill amounts have at most 2 decimal places (got: 12.345)
$ echo $?
2

$ tipsy 1000000
tipsy: bill amount too large (max $999999.99)
$ echo $?
2

$ tipsy 12 34
tipsy: expected exactly one bill amount
usage: tipsy <amount>
$ echo $?
2

$ tipsy --json
tipsy: unknown option: --json
$ echo $?
2
```

## No arguments — usage, exit 2. NO interactive prompt. Ever.

```
$ tipsy
usage: tipsy <amount>
       tipsy --help
$ echo $?
2
```

## Piped stdin — ignored; stdin is never read

```
$ echo "42.50" | tipsy
usage: tipsy <amount>
       tipsy --help
$ echo $?
2
```

## Help

```
$ tipsy --help
tipsy — tiny tip calculator

usage: tipsy <amount>

Prints 10/15/20% tip options (rounded to the nearest 10 cents, ties up)
and the resulting totals for the given bill amount.

amounts: positive, at most 2 decimal places, optional leading $,
         maximum $999999.99

exit codes: 0 success, 2 usage or validation error
$ echo $?
0
```

## Performance

Invocation-to-output under 50ms at p95 on the reference machine — "feels
instant" at the table.
