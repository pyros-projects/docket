# Provenance — read before editing

**Origin:** authored 2026-06-14 through the dojo (intake → baseline RED →
GREEN → pressure-test → graduation → trigger-eval → package). Dojo record at
`~/.limitless/dojo/docket/contract-first-development/contract-first-development-record.md`;
design spec at `docs/upstream/2026-06-14-contract-first-skill-given-authority-horse.md`.

**What this is:** the **given-authority horse** — sibling to
`surface-first-development`. Both are producer skills that emit
docket-admissible `.contract.yaml` through the same Accord door
(`docs/concepts/01`). They differ only in the *source of clauses*:
surface-first derives them from a converged prototype; contract-first compiles
them from authority that already exists in obligation form (regulation, SLA,
compat spec, legacy test suite, security policy, prior converged contract).
Routing between them:
`docs/upstream/2026-06-14-which-horse-surface-first-vs-contract-first-routing.md`.

**Canonical home:** the producer's repo (limitless), per boundary discipline.
This copy is a reference fixture in the docket repo, mirroring the SFD
variant's arrangement. Docket-the-tool stays producer-agnostic; this directory
must never become a dependency of the docket tool. The schema and Accord door
policy are NOT duplicated here — both skills defer to
`docs/concepts/01-contract-schema-and-door-policy.md` as the single canonical
source. This skill adds only what is unique to compiling given authority.

**The load-bearing invariant:** the Phase 1 precondition gate — *if you cannot
point at a document and quote a passage stating a commitment, reroute to
surface-first; never compile from intent.* This is what separates
contract-first from spec-first. Any edit that weakens it (e.g. allowing "the
user's intent" to count as authority) reverts the skill to spec-first with
extra steps and must be rejected.

**Branch note:** authored on `v0` (baseline surface-first skill). Branch-
independent — contract-first has no surface to generalize, so it sits
unchanged beside whichever surface-first variant (original on `v0`,
generalized on `v0-sfd-1`) wins the comparison.
