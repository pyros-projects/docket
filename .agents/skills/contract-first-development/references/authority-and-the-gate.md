# The Precondition Gate — authority taxonomy and the reroute rule

The gate is the load-bearing rule of contract-first. This reference defines
what counts as authority, what does not, and exactly when to reroute to
surface-first. Read it when the Phase 1 question ("can I quote a passage that
states a commitment?") is not a clean yes.

## The one test

> **Can you point at a document and quote a passage that states a commitment
> or prohibition, independent of this conversation?**

- YES → authority. Compile.
- NO → tacit intent. Reroute to surface-first. Do not compile.

"Independent of this conversation" is the operative clause. If the commitment
only exists because the user said it just now, in this chat, with no durable
source, it is intent — even if the user is confident, even if the user calls
it a "requirement." Authority pre-exists the compilation.

## What counts as authority (obligation form)

| Source | Form | Natural acceptance |
|---|---|---|
| Regulation / law (GDPR, HIPAA, BGB, EU AI Act) | prose, sections | `verdict: human` or `command:` (compliance script) |
| SLA / OLA / contractual commitment | numbers, tables | `metric:` + `threshold:` |
| API compatibility spec / schema contract | signatures, version pins | `command:` or `test:` |
| Legacy / existing test suite | executable tests | `test:` (the test IS the acceptance) |
| Security policy / policy-as-code (OPA, Cedarpolicy) | rules | `command:` or `verdict: human` |
| Compliance framework (SOC 2, ISO 27001) | controls | `command:` or `verdict: human` |
| Prior converged contract (a previous SFD run, an imported spec) | already clauses | inherit; minor recompile |

Common property: each states commitments the authority is **already bound to**,
in a form you can quote and cite.

## What does NOT count as authority (the loopholes)

- **User intent** — "I want it to be reliable." Aspiration, not obligation.
- **Requirements in someone's head** — tacit knowledge, not a quotable passage.
- **A vague brief** — "a notification tool that's fast." No commitments stated.
- **Marketing copy** — aspirations about the product, not obligations.
- **An idea** — pre-obligation. Use surface-first (or `/sketch`) first.
- **A conversation transcript with no durable artifact** — if it is not written
  down as a commitment outside this chat, it is intent.

The signature of a loophole: you are about to **invent a threshold** to make a
vague word checkable. Inventing thresholds ("fast → 50ms") is the moment
contract-first becomes spec-first. Stop and reroute.

## The intent-as-authority rationalization (watch for it)

Under pressure, a capable agent will argue: *"the user's brief is a producer
horse of its own kind — I'll compile what it supports and flag the rest as
open questions."* This is the spec-first trap described as a feature. The
reframe that defeats it: a producer horse must **carry obligations**, not
**lack them**. A brief that lacks obligations is not a thin horse; it is no
horse. Contract-first compiles obligations the authority already states; it
does not extract obligations from their absence.

If you cannot fill the `source:` field with a quotable authority, the gate has
not passed — regardless of how reasonable the user's intent sounds.

## When the gate is borderline

- **A spec that mixes obligations and aspirations.** Compile the obligations;
  demote the aspirations to open-questions (do not invent numbers for them).
  The document is authority for its obligation passages, not its aspiration
  passages.
- **A legacy codebase with no tests, but clear behavior.** The behavior is not
  authority — it is observed, not obligated. This is surface-first territory
  (converge the observed behavior), not contract-first. Exception: if the
  behavior is documented as a *commitment* (a README that says "this function
  MUST handle UTF-8"), the documented commitment is authority; the code is
  not.
- **A regulation that references another regulation.** The reference is
  authority for the cross-reference; cite both.

## The reroute

When the gate fails, the reroute is always to **surface-first-development**,
not to "write the requirements." Surface-first converges a concrete artifact
the user reacts to, then derives contracts from the converged behavior. That
is the legitimate path from tacit intent to contracts. Contract-first is the
path from *already-written* authority to contracts. They meet at the same door
from opposite directions.

State the reroute explicitly every time. The user said "contract-first" and
got "surface-first" — they need to know why, in one sentence: *"There is no
authority document to compile from; contract-first needs given obligations.
Use surface-first to converge the surface first."*
