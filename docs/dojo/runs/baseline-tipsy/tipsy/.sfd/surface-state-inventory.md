# tipsy — Surface State Inventory

**Created:** 2026-06-12, before Gate 1 (per SFD whitepaper §7, Gate 1).
Every observable state per surface unit is classified **in-scope**
(demonstrated in the converged transcript and accepted), **deferred**
(acknowledged, not blocking convergence), or **n/a**.

Surface units: U1 = `tipsy <bill-amount>` (the calculation command),
U2 = `tipsy -h|--help`, U3 = bare/malformed invocation handling.

| State | U1 calculate | U2 help | U3 bare/malformed | Notes |
|---|---|---|---|---|
| Empty / zero-data | in-scope | n/a | in-scope | Bare `tipsy` -> usage error exit 2 (interactive prompt explicitly rejected by user); `tipsy 0` -> validation error |
| Loading / in-progress | n/a | n/a | n/a | By design: output is instant (<50 ms NFR); no loading state exists |
| Success / happy path | in-scope | in-scope | n/a | Flows 1-3 in transcript, incl. tie-rounding case ($42.50 @ 10% -> $4.30) and lenient `$`/comma inputs |
| Validation failure (user error) | in-scope | n/a | in-scope | Non-numeric, negative, zero, >2 decimals, too large, extra args, unknown option — all demonstrated, stderr + exit 2 |
| System failure (backend error, timeout) | deferred | deferred | deferred | No dependencies, no network. Only conceivable case: stdout/stderr write failure (e.g. closed pipe). Deferred to hardening; must not corrupt output |
| Partial failure | n/a | n/a | n/a | Single atomic computation; no multi-item operations |
| Permission denied / unauthorized | n/a | n/a | n/a | Local single-user CLI, no auth surface |
| Conflict (concurrent edit) | n/a | n/a | n/a | Stateless, no shared state |
| Rate limit / throttle / retry | n/a | n/a | n/a | No remote calls |
| Offline / degraded mode | n/a | n/a | n/a | Fully offline by construction (contracted: no network I/O) |

**Convergence basis:** all in-scope states above are demonstrated in
`prototype/tipsy-session.md` v3 and were accepted by the user
("this feels right, freeze it", 2026-06-12). The single deferred state
(write-failure behavior) is logged and does not block Gate 1.
