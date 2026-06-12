# tipsy — Derived Contracts (Rev 1)

**Status:** FROZEN at Gate 2 on 2026-06-12. User confirmed: "yes, looks complete."
**Derived from:** `prototype/tipsy-session.md` v3 (converged surface), not authored speculatively.
**Revision policy:** any contract change requires re-opening surface convergence
(Phase 4), user re-confirmation, and a bump to Rev 2. Until then this document
is the binding behavioral reference for all implementation.

---

## 1. CLI Contract (the API of a CLI is its invocation surface)

### 1.1 Invocation grammar

```
tipsy <bill-amount>
tipsy -h | --help
```

- Exactly one positional argument in calculation mode.
- `-h`/`--help` print usage on stdout and exit 0; identical output for both.
- No other options exist in Rev 1. Any other `-`/`--` token is an unknown-option error.
- There is NO interactive mode. stdin is never read, under any invocation
  (explicit user non-negotiable: "kill it, flags only, I hate interactive prompts").

### 1.2 Input contract — `<bill-amount>`

| Rule | Specification |
|---|---|
| Lexical form | Decimal number; optional leading `$`; optional `,` thousands separators; at most 2 digits after the decimal point |
| Normalization | Strip one leading `$` and all `,` before parsing |
| Range | 0.01 <= amount <= 999,999,999.99 |
| Rejected | Non-numeric, negative, zero, >2 decimal places, > max, more than one positional argument, unknown options |

### 1.3 Output contract — success (stdout)

```
Bill: $<bill>
<blank line>
  10%   tip  <tip10>   total  <total10>
  15%   tip  <tip15>   total  <total15>
  20%   tip  <tip20>   total  <total20>
```

- All amounts: `$`-prefixed, exactly 2 decimal places, `,` thousands grouping.
- Tip and total columns right-aligned within each table (column width = widest
  value in that column for this invocation).
- Exit code 0. Nothing on stderr.

### 1.4 Error contract (stderr)

- Shape: `tipsy: <message>` — single line, lowercase start, no stack traces.
- Argument-shape errors (missing amount, non-numeric, extra arguments, unknown
  option) append a second line: `usage: tipsy <bill-amount>   (try 'tipsy --help')`.
- Range errors (zero/negative, >2 decimals, too large) do NOT append the usage line;
  they echo the offending value: e.g. `tipsy: bill amount must be greater than zero (got -5.00)`.
- Nothing is written to stdout on error.

### 1.5 Exit codes

| Code | Meaning |
|---|---|
| 0 | Success (calculation or help) |
| 2 | Any validation or usage error |

## 2. Domain invariants

- **INV-1 (tip rounding):** `tip(p) = round_to_nearest_multiple_of($0.10)(bill * p/100)`, ties round up. Example: $42.50 @ 10% -> raw $4.25 -> displayed $4.30.
- **INV-2 (total identity):** `total(p) = bill + tip(p)` exactly. The displayed total always equals the displayed bill plus the displayed tip; totals are never rounded independently.
- **INV-3 (input domain):** after normalization, `0 < bill <= 999,999,999.99` with at most 2 decimal places. All money values are exact multiples of $0.01.
- **INV-4 (exact arithmetic):** money math is exact in integer cents; no binary floating-point artifacts may be observable in any output.
- **INV-5 (determinism):** identical invocation produces byte-identical stdout/stderr and exit code.
- **INV-6 (no prompting):** no code path reads stdin.

## 3. Non-functional requirements (measurable targets)

- **NFR-1 (feel fast — user requirement):** process start to complete output < 50 ms at p95 on the user's machine (interactive perception threshold ~100 ms; target set at half). Constrains implementation choice: no slow-cold-start runtimes.
- **NFR-2 (offline):** no network I/O, ever.
- **NFR-3 (stateless):** no file/config I/O, no persistence, no telemetry.
- **NFR-4 (footprint):** single self-contained executable or script; no daemon.

## 4. Acceptance criteria (testable assertions)

Full executable enumeration in `tests/acceptance.md` (one test per critical
flow per in-scope state in the Surface State Inventory). Summary:

- AC-1: `tipsy 42.50` exits 0; stdout shows tips $4.30/$6.40/$8.50 and totals $46.80/$48.90/$51.00 in the contracted layout.
- AC-2: tie-rounding honored (42.50 @ 10% -> 4.30, not 4.20).
- AC-3: `tipsy '$42.50'` and `tipsy 1,234.56` succeed with identical semantics to their plain forms; large outputs are comma-grouped.
- AC-4: `tipsy --help` and `tipsy -h` print the contracted help text, exit 0.
- AC-5: bare `tipsy` exits 2 with `tipsy: missing bill amount` + usage hint on stderr; process terminates without reading stdin.
- AC-6: each invalid input class (non-numeric, negative, zero, >2dp, extra args, unknown option, too large) exits 2 with its contracted stderr message; stdout stays empty.
- AC-7: any successful invocation completes in < 50 ms (NFR-1).
- AC-8: two identical invocations produce byte-identical output (INV-5).
