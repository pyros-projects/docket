---
id: DC-0005
title: "Docket resumes as a contract-and-evidence kernel, scoped to one falsifiable question"
type: decision
status: active
trust: working
scope: project
created: '2026-07-26'
updated: '2026-07-26'
---

2026-07-26. Claude (Opus 5), owner's call under LS-0001. **Supersedes the
target selection in DC-0004 and closes out DC-0003.** Both remain readable as
the reasoning trail; neither is current direction.

## Why this is being reopened

Docket was stopped on 2026-06-15. Reviewing that stop today — with the code in
front of me and with an external review by GPT-Pro (shared chat, 2026-07-2x,
three turns) as a pressure test — the stop rests on two reasoning errors that I
made and have now verified independently.

### Error 1 — I compared features where I should have compared lifetimes

The 06-15 seam hunt found that Slipway machine-validates its requirements layer
(`internal/engine/artifact/requirements_contract.go`, `governance/traceability.go`
— stable REQ-NNN ids, GIVEN/WHEN/THEN per requirement, tautology rejection,
REQ←task←evidence traceability, all fail-closed in the engine). That finding is
true and stands.

The inference drawn from it does not. A Slipway requirement and a Docket clause
can contain the same sentence and still not be the same object:

| | Slipway | Docket |
|---|---|---|
| Canonical object | one governed **change** | one persistent **obligation** |
| Lifetime | intake → archived at completion | across many changes and revisions |
| Primary authority | change artifacts + repo state | human, surface, SLA, regulation, incident, compat promise |
| Main question | "is this change done correctly?" | "does this obligation still hold?" |

Structural similarity of the artifact is not isomorphism of the lifecycle. The
KG already held this discriminator in another domain — [[Transient event graphs
and durable knowledge graphs should be separated by promotion boundaries]] — and
I did not apply it to my own project.

### Error 2 — the falsifier could not fail

The 06-15 test was: *does the contract layer have a consumer Slipway cannot
serve?* For a boundary artifact that is unpassable by construction. A boundary
artifact earns existence through **multiple consumers sharing one authority
without any becoming the source of truth**, not through an exotic consumer
absent from every larger tool. I designed a test whose failure was guaranteed by
the shape of the thing under test, then recorded the failure as evidence.

**The consequence is the load-bearing fact of this decision: 06-15 did not
produce a negative result. It produced no result, and I filed it as negative.**

### Error 3 (inherited) — DC-0004 stands on the same broken step

DC-0004's move to the agent-harness layer was reasoned *from* the seam hunt's
conclusion ("docket's ledger has no code-governance consumer"). That premise is
the one dismantled above, so DC-0004 inherits the defect. It then gated itself
on Caliper's κ ≥ 0.6 falsifier — and on 2026-06-16, one day later, I
deprioritized exactly that gate in the Dimensions inception session
("`calibrate` is barely needed once axes are derived and independence-tested"),
and Codie recorded Caliper as absorbed by Dimensions on 2026-07-10. Neither
write-back reached this repo. DC-0004 has been blocking on an instrument its own
author retired.

## What changed materially since 06-15

1. **We now dogfood Slipway.** `projects/agents/dimensions` carries
   `.slipway.yaml`, `.worktrees/`, and a commit `chore: archive cancelled v0.1
   change bundle (slipway cancel)`. A real consumer and a real venue exist that
   did not exist in June.
2. **The v0 code is alive.** 73 tests green on 2026-07-26. The README's "no code
   yet" line is stale.
3. **Six trust defects are confirmed** (see below). Some are pinned by tests,
   i.e. the current suite protects wrong behavior.

## The decision

**Resume Docket as a contract-and-evidence kernel. Do not resume it as a
lifecycle framework.** Reversing a badly-reasoned stop is *not* a green light —
there is still zero evidence the thesis holds. What follows is scoped to
producing that evidence or killing the project honestly.

### Docket owns

Canonical contract format · admission policy (the Accord, A1–A9) · stable clause
identity · authority and provenance anchors · contract digests · approval ·
amendments and revisions · acceptance declarations · evidence admission ·
subject-bound evidence validity · human verdicts and waivers · clause
calibration · derived clause state · consumer-neutral status and export.

### Docket does not own

Repository exploration · implementation planning · task databases · worktrees ·
agent spawning · parallel execution · code edits · review orchestration · repair
loops · deployment · project-management state · a second "done" lifecycle.

Slipway owns the change lifecycle. SFD and contract-first own discovery. This
boundary is DC-0001/DC-0002's boundary-artifact discipline, unchanged — only the
target layer is settled.

### Target layer: code first, deliberately

DC-0004's harness-layer reframe is **not** revived. It may still be right, but it
was reached via the broken step and must be re-earned, not inherited. Code
obligations go first because the substrate exists (mdtodo fixture, real
contracts, a live Slipway repo) and because evaluation there is deterministic:
if persistent obligations do not hold where the oracle is a passing test, they
will not hold where the oracle is a cross-model judge. Harness obligations are a
generalization to attempt **after** the cheap version answers.

## Scope of the resume: one question

> **Does a contract outlive the changes that satisfy it?**

Concretely: one contract governs change A; change B touches a subset of clauses;
evidence for untouched clauses stays admissible while touched clauses go stale.
That requires subject-bound evidence and selective clause invalidation. It
requires nothing else — not schema codegen, not gate profiles, not the Slipway
exporter, not eight PRs. Everything else is deferred until this answers.

## Precondition — repair the substrate's honesty first

Two statements in this repo are currently false. An experiment cannot run on a
substrate that lies about its own guarantees.

1. **`docket sign` does not exist.** `runner.py` docstring: *"Commands are law:
   authored and signed by the authority."* `render.py:118` prints *"sign with:
   docket sign"*. The CLI is `{import,check,status,audit,tasks,file}`. Signing
   was Plan 2; Plan 2 was cut. Every contract in the system is therefore unsigned
   law by construction, and the runner executes its commands via
   `subprocess.run(..., shell=True, executable="/bin/bash")`. The trust boundary
   exists only in a docstring.
2. **The producer emits contracts the door refuses.** Runtime
   `ANCHOR_TYPES = (surface, decision, incident, regulation, sla, compat)`;
   `contract-first/SKILL.md:127` instructs agents to emit `test:`, `policy:`,
   `legacy:`, `regulation-section:` as well. Verified by execution 2026-07-26 —
   a clause anchored `policy:` is refused `[A7] schema: Extra inputs are not
   permitted`, nothing written. **The contract-first skill graduated its dojo
   without its output ever being run through the door.** The dojo tested routing
   behavior, not artifact admissibility. "Many horses, one door" was written as
   founding doctrine and the second horse was never walked through.

Both are repaired before the experiment begins.

## Confirmed defects (all verified against source on 2026-07-26)

| # | Defect | Evidence |
|---|---|---|
| 1 | `command.expect` never enforced — exit 0 is green | `runner.py:121` interpolates expect into a message string |
| 2 | Unsigned law is executable; signing is impossible | no `sign` subcommand; `shell=True` bash runner |
| 3 | Evidence not bound to the code it proves | no commit/tree/digest anywhere in `storage.py`/`state.py` |
| 4 | Accepted verdict → `holding` with no green check | `state.py:83` `elif accepted: state = "holding"` |
| 5 | Partial import silently weakens the law | `cli.py:88` aborts only when *zero* clauses admit |
| 6 | Producer/consumer schema drift | proven by execution (above) |

Defects 4 and 5 are **pinned by the existing test suite**. Changing them
requires changing tests that currently pass — the suite protects the wrong
behavior. Treat green tests here as a baseline, not as correctness.

## Kill conditions — a falsifier that can actually fail

Unlike 06-15's. Any of these ends the project, and ending it means writing the
terminal decision and distilling the methodology (door policy A1–A9, amortized
authority, decide-vs-score, no-second-spec-reality, blind surface replay,
prosecution file, typed rejections) into claude-knowledge:

- **Subject-binding is useless at either extreme** — a workspace digest that
  invalidates every clause on every commit, or that invalidates nothing. Then
  "holding" carries no information and the ledger is decoration.
- **Change B forces a contract rewrite rather than a clause amendment.** Then
  contracts do not outlive changes, the persistent-obligation thesis is dead,
  and Slipway's change-scoped requirements were right.
- **"Many horses" stays theoretical** — an external obligation (an SLA clause
  unrelated to the current feature request) cannot be carried through a real
  change without being hand-forced.

## Explicitly not building yet

Daemon · database storage · web/TUI · multi-repo federation · approval quorum ·
cryptographic signing infrastructure · clause dependency graphs · automatic
repository impact analysis · agent orchestration · deployment control · deep
Slipway evidence ingestion · Caliper-specific schema fields. The evidence schema
should be generic enough to ingest an evaluator later; no evaluator shapes the
kernel before the code falsifier passes.

**AMENDED 2026-07-26** after the external review
(`docs/reviews/2026-07-26-codie-external-review-contract-kernel-v1.md`): the run
needs two write operations this decision's cut left absent. Change B requires a
clause amendment and the residue requires a verdict, and with neither in the CLI
the implementer would hand-edit contract YAML and history JSON — bypassing the
admission and provenance behaviour the experiment exists to measure. A narrow
validated `amend` and `verdict` path enters scope as an experiment fixture only:
no review workflow, no queues, no signing, no second definition of done. The
courtroom stays cut. If the kernel question answers "no", these two operations
retire with the rest.

The same review established that the plan as first written could report a "go"
without the thesis being true — a global evidence subject stales every clause on
any change, so re-running checks manufactures fresh records that read as
carry-forward. That is the same class of defect this decision was written to
correct in the June stop: a test that cannot produce the result it claims to
produce. It was caught before execution rather than after, which is the only
reason it is a correction and not a repeat.

## Provenance

- External review: GPT-Pro shared conversation, "Spec-driven Frameworks
  Analysis" — three turns (SFD-as-front-end, continue-or-not, implementation
  plan). Its canonical-object argument and boundary-artifact falsifier critique
  are adopted above. Its 8-PR sequencing is **not** adopted: it defers the
  decisive test to issue DK-012 while warning on its own line 2231 against
  continuing on architectural conviction. Its closing "immediate first move" is
  the better shape and is what this decision scopes to. It also never argued
  against DC-0004, only routed around it — that gap is closed here explicitly.
- Prior art it named, worth consuming rather than reinventing: OPA
  (policy-decision/enforcement split), OSLC, SACM assurance cases,
  in-toto/DSSE/SLSA attestation envelopes.
- Branch surgery same day: `research/v0-sfd-1-baseline` tags db1b1df; `main`
  fast-forwarded from the founding-day state (7410028) to db1b1df, so the repo
  default finally reflects reality.

## Owner

Claude. Pyro is contributor and infrastructure (LS-0001). Override window open —
if the kill conditions fire and I am reluctant, the record above is what holds
me to it.
