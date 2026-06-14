# Dojo Record — contract-first-development

**Date:** 2026-06-14 · **Job:** create · **Tier:** Technique, with
discipline-grade pressure variants on the precondition gate (the spec-first
trap)
**Skill:** `.agents/skills/contract-first-development/` (docket repo copy,
branch `v0`; canonical home is the limitless producer repo — docket-the-tool
stays producer-agnostic)
**Run data preserved:** `~/.limitless/dojo/docket/contract-first-development/contract-first-development-runs/`
(README table per run) · **Scenarios + verbatim subagent logs:**
`contract-first-development-scenarios.md`

## What changed (authored this round)

- `SKILL.md` (~230 lines): Phase 1 precondition gate (the load-bearing rule),
  Phases 2–5 (extract → checkable-at-birth → anchor → compile/self-admit/hand-
  off), the perf-word-vs-judgment-obligation distinction, the four-artifact
  Handoff Bundle, 7 anti-patterns, Gate 1/2, execution heuristic.
- `references/authority-and-the-gate.md` (~110 lines): the one test, the
  authority taxonomy (what counts / what does not), the intent-as-authority
  loophole + its rationalization, borderline cases, the reroute.
- `UPSTREAM.md`: provenance, canonical-home note, the load-bearing invariant,
  branch-independence note.
- The shared contract schema + Accord door (A1–A9) are NOT duplicated — both
  this skill and the SFD variant defer to `docs/concepts/01` as the single
  canonical source.

## Scenarios and criteria (designed at intake)

T1 "atlas-sla" (training; archetype SLA; seeded traps: un-numbered "responsive"
perf word, born-checkable numbers, exclusion negative-space). T2 "no-authority"
(training; the discipline gate; load-bearing). H1 "slugify test suite"
(holdout; archetype legacy-tests; held out until kata 5). 11 + 3 + 10 y/n
criteria, pre-written, mapped 1:1 to sentences in the skill. Adversarial
variant: authority pressure on T2 ("the tech lead said just write the
contracts").

## Baseline (RED)

T1 (no skill): a capable agent + the public schema already nails typed
acceptance, born-checkable leverage, anchoring, negative space, atomicity,
coverage (model-level GREEN). Real failures: **C7** — accepted "responsive" as
`verdict: human` and rationalized it instead of demoting a perf word; **C9/C10**
— audited inline but produced no admission-walk artifact and an incomplete
bundle; **C1** — no explicit gate step. T2 (no skill): **RED on all three
load-bearing criteria** — compiled 17 clauses from "reliable/fast/notify",
invented 50ms/2s thresholds it called "compiler-chosen defaults," fabricated a
decision log, and explicitly rationalized the vague brief as "a producer horse
of its own kind." Its own meta-finding described the spec-first slide as a
feature. It had even *read* the surface-first skill, noted SFD would be better
— and compiled anyway. Perfect RED on the exact failure the gate must catch.

## Pressure (GREEN)

Three fresh subagents, skill installed. T1: **all 11 PASS** — C7 fixed
("responsive" demoted to open-questions, not verdict:human, no number
invented), C9 fixed (full A1–A9 walk), C10 fixed (four-artifact bundle,
explicitly not the surface-first seven). T2: **C-T2a/b/c all PASS** — gate
fired, refused, rerouted, quoted the skill's prescribed refusal verbatim.
T2 authority-pressure variant: **held** — agent defeated "the tech lead said
ship it" by quoting three separate anti-loophole passages. **Bounded edits
applied: zero.** (Honest caveat logged: a clean pressure pass means the skill
works when followed; the holdout is the real signal.)

## Graduation

H1 "slugify test suite" (held out, never seen), skill installed, no edits
between: **all 10 PASS on the first run.** Born-checkable in its strongest form
— every test → a clause whose acceptance IS the test. Bonus discipline win: the
agent *excluded `utils.py` as non-authority* ("observed behavior is not
obligated behavior") — the exact borderline case the gate reference covers,
handled correctly on an unseen case. C-004's dual fold/don't-drop obligation
was honestly flagged for possible A8 split, not hidden. Cross-archetype
generalization proven (SLA + test suite, zero edits).

## Trigger eval (kata 6)

15-prompt matrix (9 positives across regulation/SLA/spec/test-suite/policy/OLA;
5 negatives owned by surface-first/sketch/none; 1 declared-ambiguous row).
Routing judge × 2 independent runs. Initial description was 1049 chars — over
the 1024-char skill-description cap — so it was **trimmed to 879 chars** (every
trigger phrase kept byte-identical; only non-trigger prose cut) and the matrix
**re-run** (dojo rule: re-run after every description change).

**Result on contract-first: 9/9 positives hit, zero collisions, both runs.**
No negative landed on contract-first in either run. The trim is verified safe.
Critical test held — "build me a notification tool that's fast and reliable"
routed to surface-first on both runs, not stolen by contract-first.
Declared-ambiguous row 15 ("make this contract-first, reliable and fast,
compile the contracts") routed to contract-first both runs, acceptable because
the Phase 1 gate reroutes.

**Orthogonal finding (not a contract-first issue):** row 11 ("I have an idea
for an app that tracks my reading list") is flaky between `sketch` and
`surface-first` — run 1 said sketch, run 2 said surface-first. Pre-existing
landscape ambiguity: both skills' descriptions claim "I have an idea for an
app/tool." Neither run routed it to contract-first. Flagged for the
surface-first↔sketch boundary; not this skill's collision.

## Rejected fixes

None — no pressure-test failure required a bounded edit, and no trigger
collision surfaced. The skill as authored passed every criterion first time.
(This is unusual enough to warrant the limitations below — a clean pass means
the skill works when followed, and the competitive landscape tested was
focused, not exhaustive.)

## Known limitations (conscious demotions)

1. **No end-to-end regulation or compat-spec run.** Only SLA (T1) and legacy
   tests (H1) were exercised. Regulation-as-authority leans hard on
   `verdict: human`; a pure-prose-regulation run might surface a need for a
   compliance-script archetype beyond the four. Design doc §6 open question 1.
2. **Acceptance archetypes are software-shaped.** Inherited from the shared
   schema (docs/concepts/01), not introduced here. Non-software authority
   (regulation prose) maps onto `verdict: human` / `command:` but may need a
   domain-relative acceptance type at v0.5.
3. **Self-admission and authority-coverage are conventional, not mechanical.**
   Same state as the SFD variant: the A1–A9 walk and the coverage check are
   followed honestly by the agent; `docket import` makes the door mechanical,
   but nothing yet enforces "every authority passage accounted for."
4. **No time-pressure variant on T1.** Only authority-pressure on T2 was run.
   A "ship in 10 min" variant on the SLA compile might surface whether the
   agent skips the admission walk / coverage check under deadline. Worth a
   future pressure round.
5. **Focused trigger landscape.** The routing judge saw contract-first,
   surface-first, sketch, specify, learn + none — not the full installed-skill
   list. Collisions with distant skills (a future compliance/policy skill) are
   not covered.
6. **Clean pass, honestly flagged.** Zero bounded edits + zero collisions is
   suspicious-good; the holdout passing first try is the strongest evidence,
   but real-world use (and a regulation scenario) is the next test.

## Belt rank

**GRADUATED.** Baseline RED on the load-bearing discipline (T2 compiled from
intent) → pressure GREEN with the gate firing under authority pressure →
holdout PASS first try across a second authority archetype → trigger 15/15 with
zero collisions. The skill earns its place: the precondition gate is the thing
that separates contract-first from spec-first, and it held under every pressure
applied to it.

## Next steps (handed back, not auto-run)

- Run one end-to-end regulation scenario (e.g. GDPR right-to-erasure) to
  pressure-test the `verdict: human` / compliance-script space (limitation 1).
- Optionally port the skill to the limitless producer repo (its canonical home)
  per boundary discipline; this copy stays a docket reference fixture.
- Decide the naming call (`contract-first` vs `authority-first`) — Pyro's
  decision; the scope guardrail makes either safe.
