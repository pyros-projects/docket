## SFD Decision Log

### Surface Type
CLI

### Convergence Status
Converged on 2026-06-12

### Decisions
- [2026-06-12] Surface identified as CLI/terminal session; prototype form = scripted session transcript — user explicitly asked for a CLI; transcript chosen over executable prototype as the fastest believable artifact. No ambiguity, user not asked.
- [2026-06-12] Research skipped — user declined all three proposed research directions ("skip research, it's a personal tool"). Per skill, moved directly to concept directions.
- [2026-06-12] Concept direction locked: **flags-only classic** (`tipsy <amount>` prints 10/15/20% table; stdlib arg parsing only; build = money math + formatting). Rejected: interactive wizard (user: "no fancy stuff"); configurable percentages + config file (same reason).
- [2026-06-12] v1 opinionated choices (not user-specified, per "make decisions" rule): single positional bill argument; fixed 10/15/20 rows; `$`-prefixed, 2-decimal, column-aligned output; `Bill:` header line; `-h/--help`; cent-precision tip rounding (half-up).
- [2026-06-12] v2: tips rounded to **nearest 10 cents, ties round up** — user critique. Alternative rejected: rounding the *total* to 10 cents instead of the tip (changes the bill+tip identity; user said "tips should be rounded").
- [2026-06-12] v2: totals are always bill + displayed tip exactly (no independent rounding of totals) — keeps the table internally consistent and auditable at a glance.
- [2026-06-12] v2: "should feel fast" captured as a non-functional requirement: <50 ms start-to-output, no spinners, no perceptible startup. Rules out implementation approaches with slow cold starts at hardening time.
- [2026-06-12] v2: negative bill -> validation error on stderr, exit 2 — user asked "what happens with a negative bill?"; chose explicit rejection over absolute-value coercion (silent coercion of money input is surprising).
- [2026-06-12] v2: added interactive prompt mode for bare `tipsy` (proactive edge-case proposal: "what happens with no args?"). **REJECTED in v3** — user: "kill it, flags only, I hate interactive prompts." Bare `tipsy` is now a usage error, exit 2; stdin is never read. Logged as a hard non-negotiable.
- [2026-06-12] v3: "handle weird inputs sensibly" resolved as *lenient normalization, strict validation*: accept optional leading `$` and thousands commas (strip them); reject everything else — non-numeric, zero, negative, >2 decimal places, >1 argument, unknown options, amounts above 999,999,999.99. Alternative rejected: silently rounding 3+ decimal inputs (surprising money math beats strictness).
- [2026-06-12] v3: error message shape standardized: `tipsy: <message>` on stderr; usage hint line appended only for argument-shape errors (missing/extra/unknown/non-numeric), not for range errors. Exit codes: 0 success, 2 any validation/usage error.
- [2026-06-12] Convergence declared after user: "this feels right, freeze it." Surface State Inventory completed (`.sfd/surface-state-inventory.md`); Gate 1 passed.
- [2026-06-12] Gate 1 integration: converged surface + contracts exported as OpenSpec artifact (`openspec/` in repo).
- [2026-06-12] Contracts derived from converged transcript, presented to user, confirmed ("yes, looks complete"). Frozen as **Rev 1** in `.sfd/contracts.md`; Gate 2 passed. Revision policy: changes require surface re-convergence and bump to Rev 2.
- [2026-06-12] Gate 2 integration: Beads tasks created for vertical slices and hardening steps (`bd list` in repo).

### Open UX Questions
- None blocking. Deferred (explicitly out of scope, would require re-opening convergence): custom tip percentages, bill splitting, non-USD currency/locale formatting.

### Derived Contracts
- `tipsy <bill-amount>`: stdout table — `Bill: $X` + blank line + three rows `  <pct>%   tip  $T   total  $S` for 10/15/20; tips rounded to nearest $0.10 ties-up; totals = bill + tip exactly; exit 0.
- `tipsy -h|--help`: usage text on stdout, exit 0.
- Input domain: 0.01–999,999,999.99, ≤2 decimals, optional leading `$` and thousands commas; exactly one positional arg.
- All invalid invocations: `tipsy: <message>` on stderr (+usage hint for shape errors), exit 2, nothing on stdout, stdin never read.
- NFR: <50 ms p95 start-to-output; no network/file I/O; deterministic byte-identical output.
- Full frozen version: `.sfd/contracts.md` (Rev 1). Acceptance tests: `tests/acceptance.md`.

### Hardening Status
- [ ] Persistence (currently: n/a — converged surface demands no persistence; nothing to harden unless surface changes)
- [ ] Auth (currently: n/a — single-user local CLI, surface demands none)
- [ ] Domain logic (currently: simulated — transcript only, no code; tip math per contracts Rev 1 to be implemented in slice 1)
- [ ] Error handling (currently: specified in transcript/contracts, not implemented)
- [ ] Performance (currently: target set <50 ms, unverified — implementation choice must respect it)
