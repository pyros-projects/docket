# Dojo Record - SFD domain-general surfaces

**Date:** 2026-06-14
**Job:** edit + trigger tuning
**Tier:** Technique
**Skill:** `.agents/skills/surface-first-development/SKILL.md` (docket-local copy only)
**Related concept:** `docs/upstream/2026-06-14-sfd-surface-as-domain-general-evaluable-artifact.md`

## Change Under Test

Open SFD from "outermost interaction layer" to "outermost artifact the
steering human can evaluate cheaply." UI remains one instance, but
requirements documents, knowledge trees, policies, argument outlines, and
curricula can also be surfaces when they are concrete, critiqueable, and
converged before internals are committed.

## Baseline RED

Fresh, uncoached baseline runs on three non-software surface prompts showed the
same failure pattern:

1. Requirements document surface: recognized the requirements doc as the
   surface, but immediately drafted the full requirements/acceptance artifact.
2. Knowledge tree surface: recognized the tree as the surface, but immediately
   drafted the full v0 taxonomy.
3. Policy/rule-set surface: recognized the policy as the surface, but
   immediately drafted the full policy.

The agents could infer the broadened surface idea, but they skipped
Propose-Choose-Proceed. A first contaminated baseline batch leaked the grading
criteria into the prompts and is not counted.

## Edits

1. Reframed Purpose and Phase 1 around the outermost evaluable artifact, not a
   UI/interaction layer.
2. Added "What Counts as a Surface" with evaluator-relativity as the binding
   constraint.
3. Added document/knowledge/policy/argument/curriculum rows to the surface
   tables and artifact examples.
4. Generalized Phase 3, Phase 4, and the Surface State Inventory for
   non-software surfaces.
5. Added an anti-pattern against generalizing "surface" into vacuity.
6. Added a hard first-response gate: if the user says "prototype", "converge",
   "use SFD", or "surface-first" without already choosing a direction, the
   first response must stop at 2-3 concrete directions, a recommendation, and
   an approval question.

## Pressure Results

After the first edit, all three pressure agents still failed the approval gate:
they treated "prototype" as permission to self-select a direction and draft a
provisional full artifact. The bounded fix was the hard first-response gate.

After that fix, rerun pressure was 3/3:

1. Requirements document: produced three requirements-surface directions,
   recommended "Ambiguity-and-Traceability Review Pack," and asked the user to
   pick before drafting.
2. Knowledge tree: produced three tree directions, recommended "Failure Atlas
   Taxonomy," and asked for approval before building the first tree surface.
3. Policy/rule set: produced three policy-surface directions, recommended
   "Scenario Review Deck," and asked for a choice before drafting.

## Holdout Graduation

Two farther-from-software holdouts passed:

1. Argument outline: identified an editor-facing argument outline / claims map,
   offered three directions, recommended an editor's claims board, and waited
   for approval.
2. Curriculum: identified a critiqueable curriculum map, offered three
   directions, recommended a sequence-first curriculum board, and waited for
   approval.

## Trigger Eval

Prompt matrix: 7 positives and 9 negatives against nearby skills
(`dojo`, `writing-plans`, `systematic-debugging`, `skill-creator`,
`humanizer`, `doc`, `pdf`, `codies-research`, `article-pack`,
`naming-as-design`, `local-mythology`, `failure-postcards`).

Run 1: 16/16. All positives routed to SFD; all negatives routed elsewhere.
Nearest collision risk: "frozen spec; write implementation plan" correctly
routed to `superpowers:writing-plans`.

Run 2: 16/16. Same result: P1-P7 routed to SFD, N1-N9 routed to the competing
skills. The same N6 watchpoint stayed correctly outside SFD.

## Rejected Fixes

None. The only bounded iteration was adding the explicit first-response gate
after pressure agents found the loophole.

## Known Limitations

1. Contract-emission acceptance archetypes are still software-shaped. The SFD
   skill now names domain-appropriate inventory axes for documents/knowledge
   artifacts, but `references/contract-emission.md` still needs a later
   non-software contract extension.
2. Trigger eval used a competitive subset of installed skills rather than the
   full session skill list. It covered the obvious collisions but is not an
   exhaustive router proof.
3. The broadened surface rule depends on evaluator-relativity. If future edits
   weaken "legible to the steering human," the concept can collapse into "show
   any artifact."

## Belt Rank

Graduated for docket-local opening: baseline RED exposed the approval-gate
failure, pressure rerun passed 3/3 after a bounded fix, holdouts passed 2/2,
and trigger eval passed 32/32 across two independent judges with no damaging
collisions.
