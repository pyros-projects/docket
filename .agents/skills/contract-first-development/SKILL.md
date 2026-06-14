---
name: contract-first-development
description: This skill should be used when the user wants to turn PRE-EXISTING authority — a regulation, SLA, API compatibility spec, legacy test suite, security policy, or prior converged contract — into docket-admissible contract clauses. Responds to "compile this SLA/regulation/policy/test-suite into contracts", "make this contract-first", "turn these rules into docket clauses", "contract-first", "given authority", "compile the obligations". Emits obligations the authority already states to .contracts/*.contract.yaml through the Accord door (A1–A9), with provenance anchors and born-checkable acceptance. GUARDRAIL — NOT for building something new from a vague idea: if there is no authority document you can quote, it REFUSES and reroutes to surface-first-development and never invents clauses from intent. That refusal is what keeps contract-first from collapsing into spec-first.
---

# Contract-First Development

## Reference

This is the **given-authority horse**: one of two producer skills that emit
docket-admissible contracts (the other is `surface-first-development`, which
*derives* contracts from a converged prototype). Both terminate at the same
door. For the shared contract schema and the Accord door policy (A1–A9), the
canonical source is `docs/concepts/01-contract-schema-and-door-policy.md` in
this repo — read it. This skill adds only what is unique to compiling *given*
authority: the precondition gate, the authority taxonomy, the perf-word
discipline, and the contract-first Handoff Bundle. For the gate's full
authority taxonomy and the reroute rule, read
[references/authority-and-the-gate.md](references/authority-and-the-gate.md).
For choosing between this skill and surface-first, read
`docs/upstream/2026-06-14-which-horse-surface-first-vs-contract-first-routing.md`.

## Triggers

- User says "compile this SLA/regulation/policy/test suite into contracts"
- User says "make this contract-first" AND points at a document that states commitments
- User says "turn these rules/requirements/obligations into docket clauses" where the rules already exist in writing
- User says "contract-first", "given authority", "compile the obligations"
- User hands you a regulation, SLA, compatibility spec, existing test suite, or security policy and wants it admitted to the docket

## Purpose

You compile **authority that already exists in obligation form** into
checkable contract clauses. The authority states the commitments; your job is
to make them machine-admissible through the Accord door — typed acceptance,
provenance anchors, atomic clauses — and hand the bundle to `docket import`.

You do NOT design obligations. You do NOT invent clauses. You do NOT turn a
vague idea into contracts. If the "authority" is someone's intent, aspiration,
or a brief with no stated commitments, you are in the wrong skill — reroute to
surface-first.

## Phase 1 — The Precondition Gate (do this first, before anything else)

Before compiling a single clause, answer one question: **can you point at a
document and quote a passage that states a commitment or prohibition,
independent of this conversation?**

- **YES** → you have authority. Name it (regulation name + section, SLA title
  + rev, spec + version, test file + suite, policy + clause). Write the name
  to the contract's `source:` field. Proceed to Phase 2.
- **NO** → there is no authority. **STOP. Do not compile.** Reroute to
  surface-first-development and say so explicitly: *"There is no authority
  document here — 'reliable/fast/notify' is intent, not obligation.
  Contract-first compiles given authority; it does not invent it. Use
  surface-first to converge the surface first, then derive contracts."*

The gate is load-bearing. It is the only thing separating contract-first from
spec-first. State the precondition by name every run. Full authority taxonomy
and the intent-as-authority loophole in
[references/authority-and-the-gate.md](references/authority-and-the-gate.md).

### The intent-as-authority loophole (close it)

A capable agent under pressure will rationalize compiling from a vague brief
by treating "the user's intent" as a producer horse. It is not. Authority must
pre-exist in **obligation form** — a passage that states a commitment or
prohibition the authority is already bound to. Intent, aspiration,
"requirements in someone's head," marketing copy, and ideas are not
obligation form. If you find yourself inventing thresholds to make a vague
word checkable, you have crossed the line: stop and reroute.

## Phase 2 — Extract Obligations

Walk the authority and pull out obligations **in the authority's own terms**.
Each obligation is a candidate clause.

- Mine the **negative space**: anything the authority forbids, excludes, or
  prohibits becomes a MUST NOT clause. SLA exclusions, regulatory
  prohibitions, policy denials — these are clauses, often the most important
  ones.
- Carry the authority's definitions verbatim into the obligation. If the SLA
  defines "critical incident" as "full outage or data loss," that definition
  rides in the clause — do not paraphrase it into ambiguity.
- Do not add commitments the authority does not make. If a section is vague,
  that vagueness is recorded (Phase 3), never silently resolved.

## Phase 3 — Make Checkable at Birth

Every clause gets exactly one RFC-2119 keyword (MUST or MUST NOT — never
SHOULD: decide or defer) and a typed `acceptance:`. The authority usually
**carries its own acceptance procedure** — use it. This is contract-first's
advantage over surface-first: clauses are born checkable.

Map the authority's nature to the acceptance archetype:

| Authority carries… | Acceptance archetype |
|---|---|
| A number / threshold (SLA %, latency, response window) | `metric:` + `threshold:` |
| An existing test (legacy suite, compat test) | `test:` (the test IS the acceptance) |
| A runnable check (policy-as-code, compat script) | `command:` + `expect:` |
| Pure human judgment (causation, "no jargon") | `verdict: human` |

### Perf-word vs judgment-obligation — the distinction that matters

Qualitative **performance words** (fast, reliable, responsive, scalable,
robust, snappy) are A6 refusals. Their remedy is **demote or number** — push
them to open-questions, or attach a number the authority states — never
silently accept them as a clause. **Do not route a perf word to `verdict:
human`.** `verdict: human` is reserved for obligations that are *genuinely*
matters of human judgment even when fully specified (e.g. "error messages
MUST NOT use jargon" — there is no mechanical jargon-detector; the judgment is
irreducible). The test: if the word is a performance adjective, it is A6
(demote/number); if the obligation is a judgment call with no possible
mechanical check even in principle, it is `verdict: human`. "Responsive user
experience" is a perf word → demote or number, not verdict: human.

If the authority states a perf word without a number, you have two honest
moves, in order: (1) demote to open-questions and flag it for the authority to
amend with a number; (2) if the authority genuinely intended a judgment
obligation (rare), use `verdict: human` with a `notes:` entry saying exactly
why no number exists and that adding one is a signed law change. Never invent
a number the authority did not state.

## Phase 4 — Anchor to Provenance

Every clause carries ≥1 typed `anchor:` citing the **authority passage** it
compiles from. Provenance is the whole point of contract-first — the clause's
legitimacy comes from where it came from. Anchor types: `regulation:`,
`sla:`, `compat:`, `test:`, `policy:`, `legacy:`, `regulation-section:`,
plus the standard `decision:`/`incident:` where the authority references them.
If you cannot anchor a clause to a passage, you invented it — go back to
Phase 1.

## Phase 5 — Compile, Self-Admit, Hand Off

1. **Compile** `.contracts/<project>.contract.yaml` per the schema in
   `docs/concepts/01`. Clause ids are `C-NNN`, per-project monotonic.
2. **Self-admission walk (the Accord, A1–A9):** walk every clause through the
   door checks as if you were the ledger refusing your own work. Fix refusals
   at the source; record flags honestly. Write the walk to
   `.sfd/admission-walk.md` — one line per clause ("C-001: admitted · C-007:
   A6 flag → numbered → admitted"). A handoff whose contract would bounce off
   the door is not done.
3. **Authority-coverage check:** confirm the clause set accounts for every
   obligation the authority states. Uncovered passages are recorded with a
   reason (out of scope, deferred, non-obligation), not silently dropped.
4. **Hand off** to `docket import`.

## The Contract-First Handoff Bundle (four artifacts)

Lighter than surface-first's seven — there is no prototype, no Surface State
Inventory, no convergence record, because there is nothing to converge:

| # | Artifact | Path |
|---|---|---|
| 1 | Authority pointer | `.sfd/authority.md` (name, version, location, what it covers) |
| 2 | Clause log (extraction provenance) | `.sfd/clause-log.md` (one entry per clause: the passage it came from) |
| 3 | **Contract file (the product)** | `.contracts/<project>.contract.yaml` |
| 4 | Self-admission walk | `.sfd/admission-walk.md` (A1–A9 + coverage) |

The bundle is consumer-agnostic. `docket import` consumes #3 directly; #1, #2,
#4 are the provenance that lets any future reader audit why each clause exists.

## Gates

### Gate 1 — Authority Located (precondition passed)
- [ ] Authority source named and quotable (Phase 1 gate passed, not rerouted)
- [ ] `source:` field populated with the authority name + version

### Gate 2 — Contract Admitted (Handoff Bundle complete)
- [ ] `.contracts/<project>.contract.yaml` emitted per schema; every clause: one MUST/MUST NOT, typed acceptance, ≥1 authority anchor
- [ ] Perf words demoted/numbered (not silently accepted, not defaulted to verdict:human)
- [ ] Self-admission walk (A1–A9) filed; refusals fixed, flags recorded
- [ ] Authority-coverage check filed; no authority passage silently dropped
- [ ] Handoff Bundle complete: authority pointer + clause log + contract + admission walk
- [ ] `docket import` accepts the file (zero door refusals)

## Anti-Patterns

1. **Don't compile from intent.** If you cannot quote a passage stating the
   commitment, you have no authority — reroute to surface-first. This is
   Anti-Pattern #1 because it is the failure mode that defines the skill.
2. **Don't treat "the user's intent" as a producer horse.** Intent is not
   obligation form. A vague brief is not authority.
3. **Don't invent thresholds.** If the authority says "fast" with no number,
   demote it — do not pick a number and call it law. Invented thresholds are
   the signature of spec-first sliding in.
4. **Don't route perf words to `verdict: human` to make them "checkable."**
   Perf words get demoted or numbered; `verdict: human` is for irreducible
   judgment obligations only.
5. **Don't add commitments the authority does not make.** You compile, you do
   not legislate. If a section is silent, record the silence.
6. **Don't build a second spec reality.** The contract file + clause log ARE
   the record. No parallel prose-requirements document.
7. **Don't duplicate surface-first's bundle.** No prototype, no Surface State
   Inventory, no decision log of convergence — there was no convergence. The
   four-artifact bundle is the contract-first shape.

## When NOT to Use This Skill (reroute)

- **No authority document exists** → surface-first. This is the gate firing.
- **The user wants to build something new** → surface-first (converge the
  surface, then derive contracts).
- **The "authority" is the user's preferences or aspirations** → surface-first.
- **You would have to invent the obligations** → surface-first.

In all these cases, say so: *"This is tacit intent, not given authority.
Contract-first compiles obligations that already exist in writing. Use
surface-first to surface them first."*

## Execution Heuristic

1. Is there an authority document I can quote? (If no → reroute to surface-first, stop.)
2. What does it obligate? What does it forbid?
3. What acceptance does the authority itself carry (number / test / command / judgment)?
4. Is this word a perf adjective (demote/number) or a genuine judgment (verdict:human)?
5. Can I anchor this clause to a passage? (If no → I invented it → back to Phase 1.)
6. Does the clause set cover the whole authority?
7. Would this file pass the Accord door (A1–A9)?
