# Docket — Surfaces

**Status:** converged via two SFD passes (2026-06-12): first the courtroom,
then the mutation flows after Pyro's critique ("the surface has no way to
fix or update or add contracts — if the loop fails it is dead"). Every
session below is a behavioral commitment, not an illustration.

Three users, three surfaces. The human's is deliberately the smallest.

---

## 1. The human surface — three moments

### Moment 1: the glance

```
$ docket status
DOCKET — flock feat/skills                          rev 3 (2 amendments)
source: .sfd/contracts.md (imported 2026-06-12 · SFD Gate 2)

  CLAUSE                                TASKS     EVIDENCE          STATE
  C-001 with_skills() public API        4/4       12 tests, types   ✔ holding
  C-002 frontmatter schema (flock: ns)  3/3       9 tests           ✔ holding
  C-003 discovery precedence            2/2       5 tests           ✔ holding
  C-004 shape→mode selection            3/3       awaiting verdict  ⚖ review
  C-005 script sandbox + timeouts       0/2       —                 ○ unstarted
  C-006 error taxonomy                  3/3       6 tests, 1 FAIL   ✘ broken
  C-007 optimizer CLI                   —         —                 ⏸ deferred

  1 awaiting your verdict · 1 broken · evidence freshness: 2h
```

State vocabulary (all derived, never stored): `holding` (evidence green at
current rev) · `review` (bundle filed, verdict pending) · `broken`
(acceptance failing) · `unstarted` · `deferred` · `stuck` (failure report
filed) · `pending-harness` / `overlap` (admission flags outstanding).

### Conformance with drift-naming

```
$ docket check C-006
C-006 error taxonomy ..................................... FAIL
  obligation:  SkillScriptError carries stderr, exit code, elapsed time
  evidence:    test_scripts.py::test_script_error_payload   FAIL
  drift:       ScriptRunner.run() raises RuntimeError on timeout
               (type not in contracted taxonomy)

  → fix the code or amend the contract. The docket does not care
    which, but it will not go green by argument.
```

`check` always names the *drift* — what diverged from the law — not just
the failing assertion. Red states must always print their two exits:
change the work, or change the law.

### Moment 2: the verdict

```
$ docket review C-004
EVIDENCE BUNDLE — C-004 shape→mode selection     filed by: claude-loop#18
  claim:     satisfied
  evidence:  test_shape_select decision matrix      8/8 PASS
             docket check C-004                     green @ 17:31
             loop trace #18 (3 iterations, stop reason: contract-green)
  residual:  token estimation heuristic ±15% — flagged, not contracted

accept / reject / comment? > accept
✔ C-004 accepted · pyro · rev 3 · → .contracts/evidence/C-004/bundle-003.json
```

Rejection requires a typed reason — and the type is the contract-quality
feedback loop:

```
accept / reject / comment? > reject
reason? > evidence satisfies the clause, but this is not what I meant
→ recorded as CLAUSE DEFECT (not work defect)
  C-004 flagged for amendment · clause calibration: 2 defects in
  5 verdicts — worst clause on the books
```

### Moment 3: the signature

Content amendment (law changes are drafted, re-admitted, signed; stale
evidence dies with the old rev):

```
$ docket amend C-004 --edit
draft rev 5: C-004 obligation changed
  - mode selection by token estimate (chars/4)
  + mode selection by tiktoken count, ±5% tolerance
  admission re-check ........ ✔ still checkable, anchors intact
  impact: 2 evidence bundles invalidated (C-004) → re-verdict needed
sign-off required: pyro

$ docket sign rev5
✔ rev 5 in force · amendment recorded
```

New law mid-flight, on a non-surface horse:

```
$ docket add --anchor incident:postmortem-2026-06-14-dlq-dupes
  draft C-012: "DLQ replay MUST be idempotent (double-replay = no dupes)"
  acceptance: test: tests/pipeline/test_replay_idempotent.py
  door: ✔ admitted (flag PENDING-HARNESS — test does not exist yet)
sign-off: pyro            $ docket sign rev6 ✔
```

## 2. The dead-loop exit (no deadlock by design)

A loop that exhausts its budget without contract-green files a **failure
report**, never silence. The verdict menu on a failure report includes
changing the law:

```
$ docket review C-005
FAILURE REPORT — claude-loop#23 · budget exhausted (5 iterations)
  stuck on: SIGKILL test flakes on WSL2 (timing)

verdict? > split
✔ C-005 → C-005a (sandbox enforced, active)
         + C-005b (timeout precision, deferred)
  …other exits: amend / reassign / defer / re-enter producer
                (the surface itself was wrong — back to SFD)
```

Invariant: **every red state has an exit that is either "change the work"
or "change the law,"** and changing the law always runs draft → admission
re-check → sign → rev bump → invalidate affected evidence.

## 3. The agent surface — files and JSON, no SDK

```
# next obligation with no green evidence — the derived task view
$ docket tasks --next --json
{"clause":"C-005a","obligation":"subprocess scripts SIGKILLed on
 timeout_seconds overrun","acceptance":{"test":"tests/skills/unit/
 test_scripts.py::test_subprocess_timeout"},"rev":6,"filed_evidence":[]}

# filing evidence = appending a bundle file; no API, no daemon
$ docket file C-005a --bundle bundle.json
✔ filed → review queue (status: ⚖)
```

A loop runner needs exactly three touchpoints: `tasks --next` (what to do),
`check` (am I done), `file` (claim it). Stop condition = "check is green";
the contract is the evaluator. Nothing else to integrate.

## 4. The CI surface — one exit code

```
$ docket check --all --quiet ; echo $?
1        # any broken/stale clause fails the build; deferred ones don't
```

## Surface state inventory (dogfooding the discipline)

| Surface unit | happy | empty | failure | partial | conflict |
|---|---|---|---|---|---|
| `status` | ✔ shown | no contracts → onboarding hint | broken clauses listed | mixed states shown | overlap flags shown |
| `check` | green | no acceptance harness → pending-harness | FAIL + drift naming | per-clause results | — |
| `review` | accept | nothing to review → say so | reject w/ typed reason | failure report menu | stale rev → re-verdict notice |
| `amend`/`sign` | rev bump | — | admission re-check fails → draft rejected | partial invalidation listed | concurrent draft → refuse second draft |
| `import`/`add` | admitted | empty file → noop + warning | refusals A1–A7 | flags | duplicate IDs refused |
| `tasks`/`file` | next task | all green → "docket clear" | malformed bundle refused | — | rev mismatch → refile |

Deferred cells (acknowledged, not blocking concept convergence): watch
modes, multi-repo dockets, notification surfaces ("the docket comes to
you"), HTML/TUI status board.
