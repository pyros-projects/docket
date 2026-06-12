# Docket

The repo's courtroom: a file-native ledger of obligations (contracts), the
evidence that satisfies them, and the verdicts and signatures that bind them.

> The test suite was how CI governed code; the contract is how humans
> govern agents.

**Status:** concept phase — no code yet. The design lives in
[`docs/concepts/`](docs/concepts/), in reading order:

1. [Why and what](docs/concepts/00-docket-why-and-what.md) — amortized
   authority, the courtroom model, boundary-artifact discipline
2. [Contract schema and door policy](docs/concepts/01-contract-schema-and-door-policy.md)
   — the clause format and admission checks A1–A7
3. [Surfaces](docs/concepts/02-surfaces.md) — the human's three moments,
   the agent's three touchpoints, CI's one exit code
4. [v0 scope and falsifier](docs/concepts/03-v0-scope-and-falsifier.md) —
   the smallest docket that can be proven wrong

Agent operational memory lives in [`memory/`](memory/).
