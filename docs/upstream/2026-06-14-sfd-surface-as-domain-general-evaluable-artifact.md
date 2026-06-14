# SFD — the surface is domain-general (drop the visual qualifier)

**Date:** 2026-06-14
**Status:** dojo-tested docket-local opening, written for a context-fresh agent.
Originated by Pyro while reviewing the docket-emitting SFD variant
(`.agents/skills/surface-first-development/SKILL.md`); KG-grounded via the
claude-knowledge vault. See
`docs/dojo/sfd-domain-general-surface-record.md` for the local dojo record.
**Targets:** `.agents/skills/surface-first-development/SKILL.md` (this repo's
docket-emitting variant). Earlier upstream-target wording is intentionally
deferred; Pyro scoped this run to docket only.
**Relation to 0.7:** orthogonal. The 0.7 work sharpened the *output* (contracts
are the product; the prototype is the interview instrument). This sharpens the
*input* (what counts as the surface in the first place). They compose cleanly.

---

## 1. Why (the reasoning, compressed for a fresh context)

Pyro's reframe, verbatim in spirit: "surface first" is not a UI-software thing.
If you are a requirements engineer the requirements doc is the surface; if you
want a knowledge base the knowledge tree is the surface; if you want a webapp
the UI is the surface. The surface is whatever the steering human confronts and
reacts to before internals are committed.

The vault already made this move *halfway*. The 2026-04-26 insight "SFD surface
extends to any evaluable visual artifact not only UI mockups" called the
*surface = UI* assumption a blind spot and reframed the unit from *interface* to
*evaluable representation*. But it stopped at the word **visual** — title,
description, and the whole enumerated list (diagrams, ERDs, sequence diagrams,
state machines, infographics) are visual artifacts. That is because its trigger
was backend-heavy features, which still have natural visual representations.

Pyro's two examples break the visual qualifier: a requirements document is
prose; a knowledge tree is structure. Neither is "visual." So the correction is
to drop the qualifier entirely. The surface is the outermost evaluable artifact
of a domain — concrete and confrontable, regardless of medium.

The cognitive foundation already licenses this. "Recognition is cognitively
cheaper than generation" specifies *proposal that can be evaluated* — it says
nothing about *interface* or *visual*. It is about concrete-vs-abstract,
System-1-recognition vs System-2-generation. A requirements doc is concrete and
evaluable to a requirements engineer; a knowledge tree is concrete and
evaluable to a KB architect. The engine that makes SFD work is already
domain-independent; the skill's framing is one step behind its own foundation.

Recursive evidence, under our feet: claude-knowledge is itself a non-software
instance. It converged on a textual/structural surface (the insight format) and
derives contracts from it (`check_links.py`, the pre-commit hook, schema
validators, `/validate` gates). No UI, no visual artifact — full SFD arc present
and load-bearing. `self/identity.md` states this explicitly.

## 2. What changes (decision summary)

1. **Reframe the definition, not the process.** "Surface" → the outermost
   artifact the steering human can evaluate cheaply. UI is one instance; so is
   a requirements doc, a knowledge graph, a policy, an argument outline.
   Propose-choose-proceed, converge-before-derive, clause log, Surface State
   Inventory, round-trip test, contract compilation — all unchanged.
2. **Add the evaluator-relativity rule.** Legibility is relative to whoever
   steers. Visual is the cheapest route to legibility, not a requirement. Pick
   the surface the *decision-maker* can critique. This sharpens the skill's
   loose "stakeholder" to "whoever actually steers."
3. **Generalize the surface-type table** from five software rows to a
   two-axis view: software surfaces (the existing five) **and**
   knowledge/document surfaces (requirements doc, knowledge tree/graph,
   policy/regulation set, argument/essay outline, spec-as-surface).
4. **Tighten "When NOT to Use SFD."** The exclusion shifts from "no meaningful
   interaction surface" to "no human in the steering loop who can evaluate a
   concrete artifact" (pure algorithmic core with no human steering). Smaller
   and more honest.
5. **Flag, do not fix, the acceptance-types gap.** The contract-emission
   acceptance archetypes (test / metric+threshold / command+expect /
   verdict:human) are software-shaped. Non-software surfaces need
   domain-relative acceptance (requirements: testable/traceable; knowledge:
   coverage/no-orphan). That is a v0.5 concern for the docket variant's
   `references/contract-emission.md`, recorded in §5 — it does not block this
   skill change.

## 3. The edits (concrete, against the current SKILL.md)

- [ ] **New "What is a surface" definition box** right after Purpose.
      Proposed text:

      > The surface is the outermost artifact the steering human can evaluate
      > cheaply. A UI is one instance. So is a requirements document, a knowledge
      > graph, a policy, an argument outline, a curriculum. The binding
      > constraints are **concreteness** and **legibility to whoever steers** —
      > not clickability, not visualness. Visual representations are usually the
      > cheapest route to legibility, which is why UIs and diagrams dominated
      > historically; they are not a requirement.

- [ ] **Phase 1 (Identify the Surface):** insert a higher-order step *before*
      the surface-type table — "Identify the outermost evaluable artifact of
      this domain: the thing the steering human confronts and reacts to." The
      GUI/CLI/API/pipeline/agent table then reads as *instances of the software
      axis*, not the definition.
- [ ] **"Expected Artifact by Surface Type" table:** keep the five software
      rows; add a second block — **knowledge/document surfaces** — with rows:
      requirements doc → converged requirements + acceptance criteria; knowledge
      base → the tree/graph structure + coverage map; policy/regulation → the
      rule set + exceptions; argument/essay → the outline + claims. First
      artifact principle unchanged: the cheapest concrete representation the
      steerer can react to.
- [ ] **"Why This Works":** append the evaluator-relativity sentence — the
      surface must be legible to the *decision-maker*, not just any stakeholder;
      visual is the default cheap route to legibility, not a prerequisite.
- [ ] **Phase 3 (Generate Surface Proposal):** generalize "use mock data,
      placeholder logic" (software-flavored) to "the cheapest concrete
      representation a stakeholder can react to" — mock data for a UI, a draft
      structure for a knowledge tree, a candidate clause set for a policy.
- [ ] **"When NOT to Use SFD":** replace "no meaningful interaction surface
      (pure background service, embedded firmware)" with "no human in the
      steering loop who can evaluate a concrete artifact." Keep the algorithmic/
      mathematical-core and explicit-override cases.
- [ ] **New anti-pattern (or guardrail note):** "Don't generalize the surface
      into vacuity." The discipline survives because the surface is built
      *first* (ordering), *converged* before it is derived from, and contracts
      come from the converged surface. Broaden the definition of surface;
      do not touch the process. (Pairs with the existing prototype-concreteness
      anchoring-risk anti-pattern — that risk survives the generalization.)

## 4. Guardrails (the two that keep this honest)

1. **Process unchanged.** Only the definition of "surface" and the reach
   criterion change. If a proposed edit touches propose-choose-proceed,
   convergence gates, the clause log, the round-trip test, or contract
   compilation, it is scope creep — reject it.
2. **Evaluator-relativity is load-bearing.** Without it, "surface = any
   artifact" and the methodology becomes "just show people things." The binding
   constraint is *legibility to whoever steers*. State it everywhere the
   surface is defined.

## 5. Open questions (owned, non-blocking)

1. **Acceptance types for non-software surfaces.** The four archetypes are
   software-shaped. Requirements → testable/unambiguous/traceable; knowledge →
   coverage/no-orphan/connectivity. This belongs to the docket variant's
   `references/contract-emission.md` as a v0.5 extension, not this skill
   change. Owner: first non-software SFD run that reaches Gate 2.
2. **Round-trip fidelity for non-visual surfaces.** "Reconstruct the surface
   from contracts + inventory" is natural for a UI (wireframe) and a contract
   YAML (behavior). For a knowledge tree, "reconstruct the structure" needs a
   defined fidelity target (skeleton? connectivity? node labels?). Owner: first
   knowledge-surface run.
3. **Surface State Inventory for non-software surfaces.** The 10-state
   checklist (empty, loading, success, validation failure, …) is UI-flavored.
   What are the equivalent states for a requirements doc (complete / consistent
   / traceable / conflicted / …) or a knowledge tree? Likely a per-domain
   state taxonomy under a shared "convergence is auditable" principle. Owner:
   deferred — flag in the inventory reference, do not redesign now.
4. **Does this change the dojo eval scenarios?** The current scenarios (tipsy
   CLI, mdtodo extractor) are both software surfaces and stay valid as the
   software-axis controls. Adding one knowledge/document-surface scenario
   (e.g. "converge a small requirements doc" or "converge a knowledge-tree
   slice") would test the generalization under the dojo. Recommended before
   calling the change graduated. Owner: the dojo pass that ships this.
