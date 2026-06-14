# Contract-First — the given-authority horse

**Date:** 2026-06-14
**Status:** brainstorm / proposed skill, written for a context-fresh agent. Not
yet built, not dojo-tested. Originated from the skill-spec-kit's Path A / Path B
split (`skill-contract-author` vs `skill-surface-prototyper`), reframed for the
docket world.
**Targets:** a new skill `contract-first-development` (provisional name — see
§6), sibling to `surface-first-development`. Canonical home is the producer's
repo (limitless); in this repo it lives as a reference fixture in
`.agents/skills/` exactly like the SFD variant, and docket-the-tool stays
producer-agnostic. This doc is upstream material filed here for tracking, beside
`2026-06-12-sfd-0.7-contracts-are-the-product-design.md`.
**Relation to surface-first:** not an opposing methodology. Both produce
`.contract.yaml` through the same Accord door. The difference is the *source of
the clauses* — discovered (surface-first) vs compiled from given authority
(contract-first). See the routing note next to this doc.
**Branch note:** written on `v0` (baseline surface-first skill). Orthogonal to
the surface-first generalization tracked on `v0-sfd-1` — contract-first has no
surface to generalize, so this concept is branch-independent.

---

## 1. Why (the reasoning, compressed for a fresh context)

Docket's own concept doc 00 says it: *"Many horses, one door. Contracts reach
the docket from many producers: an SFD prototype-interview (the richest one),
incident postmortems, regulation, legacy behavior, API compatibility, SLAs,
existing tests."* The surface-first skill is one horse — the richest, where
authority is tacit and has to be extracted by converging a concrete artifact.

But not all authority is tacit. Sometimes the obligation already exists in
checkable form: a regulation, an SLA table, an API compatibility spec, a legacy
test suite, a security policy, a compliance framework. There is nothing to
converge — the law is the law. Trying to surface-first these is not just wasted
effort, it is *inappropriate*: you do not get to "converge" your way to a lower
security bar by reacting to a convenient prototype. The vault already says this
— *regulations define what, not when* (SFD "When NOT to use").

So there is a second, equally legitimate horse: take **given authority** and
**compile** it into docket clauses through the same door. That is what this
skill is. The skill-spec-kit already proved the split is real: its Path A
(`skill-contract-author`) takes a contract skeleton as an *input precondition*
and never invents the contract; its Path B derives the contract from a converged
surface. Same two horses.

The hard part is naming and scoping, because the obvious name is a trap (§5).

## 2. What this skill is (decision summary)

1. **A producer skill that compiles given authority into docket-admissible
   clauses.** Input: an authority source that already exists in obligation form.
   Output: `.contracts/<project>.contract.yaml` admitted through the Accord.
2. **Not "write contracts from the problem space."** That is spec-first rebadged
   — the anti-pattern the whole thesis rejects (Flock A/B: 17 spec-driven
   requirements → the wrong abstraction). The precondition gate is: *point at
   where the authority already lives.* If you cannot, you are in surface-first
   territory.
3. **Its distinct competence is authority→clause compilation** — turning
   regulation prose, SLA tables, compatibility specs, legacy test suites, and
   policies into clauses. This is the step `docket import` does not do (import
   admits an already-written contract file). So the skill earns its existence
   and is not a wrapper around import.
4. **Shares the door and the format with surface-first; differs in everything
   upstream.** One shared `references/` (schema, Accord A1–A9, round-trip
   principle); two different upstream processes.

## 3. The skill's design

### Phase 1 — Locate the authority (precondition gate)

Where does the obligation already live? Enumerate the source: a regulation
(section cites), an SLA (table + thresholds), an API compatibility spec, a
legacy test suite (file + case names), a security policy, a compliance
framework, a prior converged surface/contract from another run.

**Gate:** if no authority source can be pointed at, **stop and reroute to
surface-first.** This is the load-bearing invariant. State it first, loudest.

### Phase 2 — Extract obligations

Read the authority and pull out obligations *in their own terms*. Each is a
candidate clause. Mine the negative space: what the authority forbids becomes
MUST NOT. This phase is the skill's distinct competence and the inverse of
surface-first's clause derivation — there, clauses are born from accepted
behavior during convergence; here, clauses are born from authority passages.

### Phase 3 — Make checkable at birth

Same rule as surface-first Phase 5: each clause gets exactly one MUST/MUST NOT
and a typed `acceptance:`. **The difference:** given authority usually *carries
its own acceptance procedure*, so contract-first clauses are more often
"born checkable" than surface-first ones:

| Authority source | Natural acceptance archetype |
|---|---|
| SLA (has numbers) | `metric:` + `threshold:` |
| Legacy test suite | `test:` (the test IS the acceptance) |
| API compatibility spec | `command:` (run the compat check) or `test:` |
| Security / policy-as-code | `command:` (policy check) or `verdict: human` |
| Regulation (prose, judgment-laden) | `verdict: human` (explicit) or `command:` if a compliance script exists |

This is why contract-first maps onto the existing four archetypes more cleanly
than surface-first does — the authority came with a check.

### Phase 4 — Anchor to provenance

Every clause carries ≥1 typed `anchor:` citing the **authority source** (e.g.
`regulation: GDPR-Art.17`, `sla: uptime-tier`, `test: tests/test_compat.py::xyz`,
`legacy: src/old_module.py`). Provenance is the whole point: the clause's
legitimacy comes from where it came from. Surface-first anchors cite inventory
cells and decisions; contract-first anchors cite authority passages.

### Phase 5 — Compile, self-admit, hand off

Write `.contract.yaml` per the shared schema. Run the Accord self-admission walk
A1–A9. Then `docket import`. The bundle is **lighter** than surface-first's
seven-artifact Handoff Bundle — there is no prototype, no Surface State
Inventory, no convergence record:

| Handoff Bundle | Surface-first | Contract-first |
|---|---|---|
| Authority source / pointer | — (the prototype) | ✓ |
| Clause log | at-birth during iteration | extraction provenance |
| Surface State Inventory | ✓ (10-state coverage) | n/a — replaced by authority-coverage check |
| Contract file | ✓ | ✓ (shared) |
| Self-admission walk (A1–A9) | ✓ | ✓ (shared) |
| Round-trip report | ✓ (blind rebuild surface) | different — see §6 |
| Prototype + decision log + intent | ✓ | — |

The "round-trip" question changes shape: there is no converged surface to
rebuild. The analogous test is *"can a blind agent reconstruct the authority's
obligations from the clauses, and does every clause trace to a cite-able
authority passage?"* — weaker on reconstruction, stronger on traceability. Flag
as an open question (§6); do not pretend it is the same test as surface-first's.

## 4. The routing rule (shared, lives in both skills)

One question selects the horse: **where does the authority live?**

- **Tacit, in a human's head** → surface-first. Extract it by converging a
  concrete artifact the human can react to.
- **External and fixed** (regulation, SLA, compatibility, legacy tests, policy)
  → contract-first. Compile it; you do not get to shape it.

Neither is the "modern" option. They are selected by the source of authority,
not by preference or rigor. Full version in the routing note beside this doc;
both skills' descriptions must point at it so the dispatcher routes correctly.

## 5. Guardrails (the two that keep this honest)

1. **The naming trap.** "Contract-first" will be read as *spec-first* — write
   contracts from imagination, then build. That is the anti-pattern. Mitigation:
   the skill's description leads with "compile GIVEN authority," and Anti-Pattern
   #1 is *"Don't author obligations from the problem space. If you cannot point
   at where the authority already lives, reroute to surface-first."* Alternative
   names considered: `authority-first`, `given-authority` (clearer, by source
   not output); kept `contract-first` for continuity with the test kit and with
   how Pyro already refers to it — but the scope guardrail, not the name, is what
   carries the meaning.
2. **The precondition is load-bearing.** "Authority already exists in obligation
   form" is the gate that separates this skill from spec-first. If a future edit
   weakens it to "authority the user roughly has in mind," the skill has become
   spec-first with extra steps. Reject that edit.

## 6. Open questions (owned, non-blocking)

1. **Round-trip test for contract-first.** Not the same as surface-first's
   "blind rebuild the surface." Candidate: a blind agent checks (a) every clause
   traces to a cited authority passage, and (b) the clause set covers the
   authority's obligations (no authority passage left un-clauled without a
   recorded reason). This is an authority-coverage test, analogous to the
   Surface State Inventory's coverage role. Owner: first contract-first run.
2. **Authority-coverage as the contract-first analog of the Surface State
   Inventory.** Surface-first classifies surface-unit × state; contract-first
   classifies authority-passage × obligation-extracted. Same "convergence is
   auditable" principle, different substrate. Worth its own short reference.
3. **Naming call.** `contract-first` (continuity) vs `authority-first` /
   `given-authority` (clarity). Pyro's decision; the guardrail makes either safe.
4. **Where the skill lives.** Producer repo (limitless) is the real home; this
   repo carries it as a `.agents/skills/` reference fixture, mirroring the SFD
   variant and its `UPSTREAM.md`. Docket-the-tool never depends on it.
5. **Dojo eval scenario.** One regulation/SLA-shaped scenario (e.g. "compile an
   SLA into docket clauses") to pressure-test the authority→clause extraction
   and the precondition gate, the way tipsy/mdtodo pressure-tested the surface-
   first levers. Recommended before calling it graduated.
