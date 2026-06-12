---
id: IN-20260612-7d2c
date: '2026-06-12'
type: inbox
scope: project
title: "GPT-Pro review of the mdtodo bundle — blind surface replay named, five pressure points (review-gate input)"
---

GPT-Pro reviewed the mdtodo graduation bundle + docket concept (relayed
verbatim by Pyro, 2026-06-12 late evening). Verdict: "a very strong first
real specimen... boring enough that the method cannot hide behind domain
glamour." Distillation-ready KG capture:
`claude-knowledge/captures/2026-06-12-gpt-pro-docket-review-blind-replay-prosecution-file.md`.

**Nothing below is law.** These are amendment candidates and v0 design
inputs for Pyro's open review gate on `docs/concepts/03`. Per the no-second-
spec-reality rule, any adoption happens by amending the concept docs'
example artifacts, not by treating this note as requirements.

## Namings worth adopting

- **Blind surface replay** (alt: contract reconstructability test) — the
  round-trip protocol as the empirical adequacy test for the SFD→Docket
  seam: can a fresh agent reconstruct accepted behavior from contract +
  coverage inventory alone?
- **Prosecution file** — the SFD bundle's role: contract = what agents
  consume; bundle = how humans audit whether the law was born honestly.
- **The triad** — SFD converges behavior; Docket preserves it as executable
  authority; blind replay tests whether anything leaked during compression.

## Five pressure points (amendment candidates)

1. **Validated ≠ proven must be loud.** All 24 mdtodo clauses are signed law
   with PENDING-HARNESS flags. `status`/`import` output must make "signed
   law, not passing reality" painfully visible.
2. **Provenance mismatch — VERIFIED.** `mdtodo.contract.yaml` says
   `signed: [{rev: 1, by: Pyro, date: 2026-06-12}]`; `decision-log.md:68`
   says "Contract remains rev 1 (pre-signing)". Real contradiction in the
   graduation fixture. Candidate: door flags contract-vs-bundle
   contradictions when importing with the SFD bundle present ("supporting
   artifact says pre-signing, contract says signed"). Also: fix the fixture
   or keep it as the dogfood case.
3. **A8 atomicity-by-gestalt doctrine.** C-003 (golden text layout) is one
   MUST pinning ~8 rendering facts; splitting would worsen the contract.
   A8 needs the nuance: atomic by surface gestalt, not by grammatical
   subcondition. C-003 is the doctrine's test case.
4. **Signed darkness needs a first-class audit view.** Five undecided
   regions in the decision log (symlinks, large-tree feedback, non-UTF-8,
   duplicate inputs, zero-TODOs × unreadable). If `docket audit` doesn't
   render open questions, implementing agents silently create law.
   (Concept 02's audit already shows UNCOVERED cells; open *questions* are a
   distinct dark-region type.)
5. **Named benchmark environment.** C-011/C-012 numbers anchor to "NVMe-class
   developer laptop." Candidate artifact:
   `.contracts/benchmarks/reference-machine.yaml`, referenced by metric
   acceptance — otherwise future evidence is slippery.

## Concrete proposal: mdtodo as the golden import fixture

GPT-Pro proposes the mdtodo bundle as the golden `docket import` fixture
(rich clause variety, exercises flags/coverage/human-verdict without
implementation burden). Complements — does not replace — tipsy's signed
bundle as the leading *fulfillment-run* candidate (TH-0001): import fixture
≠ fulfillment case. Fits D0-007 directly.

## Verbatim mock-ups (design input for v0 surfaces)

Expected import result sketch:

```
$ docket import .contracts/mdtodo.contract.yaml --with-sfd .sfd/
DOCKET IMPORT — mdtodo rev 1
source: .sfd/clause-log.md (SFD Gate 2, 2026-06-12)
signature: Pyro, 2026-06-12
clauses:
  admitted: 24
  refused: 0
  retired/superseded: C-015 absent from contract, preserved in clause log
flags:
  PENDING-HARNESS: 24
  OVERLAP: 0 active
  THIN-EVIDENCE: 0
coverage:
  surface cells covered: 12/12
  open questions: 5
  behavioral leaks from blind replay: 0
state:
  validated law, not yet proven
```

Expected audit sketch:

```
$ docket audit
COVERAGE — mdtodo rev 1
surface cells: 12/12 covered
acceptance:     24/24 pending harness
NFRs:           2/2 numbered
human verdict:  1 clause
open questions: 5 unsigned-or-deferred gaps
dark regions:
  - symlinked directories during recursion
  - very-large-tree progress feedback
  - non-UTF-8 / binary-ish markdown files
  - duplicate / overlapping inputs
  - zero TODOs with unreadable files
```

Note `--with-sfd`: a flag that reads the producer bundle for provenance/
coverage display. Boundary-discipline check needed at review: it must stay
format-generic (any bundle following the handoff format), never
SFD-code-specific, or it violates the one-job rule.
