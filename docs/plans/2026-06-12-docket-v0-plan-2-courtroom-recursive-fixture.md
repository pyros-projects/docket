# Docket v0 — Plan 2: The Courtroom + Recursive Fixture

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** The write side of docket v0: verdicts on evidence bundles and failure reports (typed rejections, per-clause calibration), the legislature (`amend`/`add`/`sign` — draft → re-admission → signature → rev bump → scoped evidence invalidation), and the shipping gate: docket's own requirements as a docket contract, imported through its own door and green under its own check.

**Architecture:** Builds strictly on Plan 1's modules. New module `legislature.py` owns drafts and signing; verdict records are the third append-only history kind under `evidence/<clause>/`. Law changes only ever happen via draft → re-admission → sign; review's failure-report verdicts (split/defer) run that same path inline because the authority is present at the verdict moment.

**Tech Stack:** unchanged (Python ≥3.12, uv, pydantic v2, ruamel.yaml, pytest, argparse).

**Prerequisite:** Plan 1 complete, suite green, Codie's door review addressed. Read Plan 1's "Design decisions" — they carry over. New decisions below.

---

## Design decisions (Plan 2 additions)

16. **Verdict record** `evidence/<clause>/verdict-NNN.json`: `{bundle, clause, verdict, rejection_type?, reason?, note?, by, rev, at}` where `verdict ∈ accepted|rejected|split|deferred|reassigned|reentered`. Calibration counts ALL verdict history (clause-defect ratio survives amendments — that's the point of measuring the law).
17. **Review is flag-driven for agents/tests, prompt-driven for humans:** `--accept`, `--reject {work,evidence,clause} --reason`, `--verdict {split,defer,reassign,reenter}`. With no flags and a TTY, prompt interactively (thin `input()` loop over the same code path).
18. **Failure-report verdicts that change law auto-sign inline** (split/defer): the authority issuing the verdict is the signer; the full path draft → re-admission → sign → rev bump → amendment record still runs, in one act. Non-law verdicts (reassign, reenter) only write a verdict record.
19. **Split takes replacement clauses from a YAML file** (`--from split.yaml`, a list of clause mappings; `--edit` opens `$EDITOR` on a pre-filled template). The original clause is `status: retired` (retired ≠ deleted), successors are door-checked before signing.
20. **`docket sign revN`** applies the pending draft for rev N; with no draft and N == current rev it *ratifies* (appends a signature to the current law — the v0-kickoff signature). Signing always prints the five-question checklist (due diligence, not ledger state).
21. **One draft at a time per contract** (`.contracts/drafts/<name>.rev<N>.yaml`); a second `amend`/`add` while one exists is refused — concept 02's conflict cell.
22. **`holding` includes mechanically-green clauses:** "evidence green at current rev" (concepts/02) covers an accepted verdict OR a valid green check record. Without this, a CI-green clause displays `unstarted`, which lies. Precedence already routes unjudged bundles to `review`/`stuck` above this branch, so no extra bundle qualifier — a judged-and-rejected bundle followed by a green check is `holding` again (the work was redone and conformance proves it; Codie review finding on the earlier `not bundles` formulation, which would have suppressed mechanical holding forever after any judged bundle).
23. **D0-007's `expect` is concretized** to the exit-code-only command pattern the graduation fixtures established; the "refusals each cite A1–A9" intent is mechanically pinned by `tests/test_import.py::test_refusals_cite_door_checks`. Recorded in the clause's `notes:`.
24. **Pyro's signature is not automated.** The recursive fixture ships `signed: []`; the final step hands the ratification (`docket sign rev1 --by pyro`) to Pyro — the third human moment stays human.
25. **`--sign-unanchored` works on `add` exactly as on `import`** (concepts/03 includes the override for both; Codie review blocker on an earlier draft of this plan that dropped it from `add`). The override is granted at draft time, persisted in a sidecar `drafts/<name>.rev<N>.overrides.json`, honored by the re-admission check at sign time, recorded in the amendment record, and deleted with the draft. The signature on the override is the drafting authority's — exactly the "legal but signed and recorded" semantics of A2.
26. **Inline signing prints the checklist too:** split/defer verdicts on failure reports are signatures (decision 18), so the five-question checklist prints in that path as well — the due diligence does not get skipped because the authority was already in the room (Codie review finding).

## File structure

```
src/docket/legislature.py          # drafts, diff, next id, sign, ratify
src/docket/cli.py                  # + review, amend, add, sign
src/docket/render.py               # + review/draft/sign templates, checklist
src/docket/state.py                # holding refinement (decision 22)
tests/test_review.py               # incl. test_typed_rejection_calibration (D0-005)
tests/test_amend.py                # incl. test_rev_bump_scoped_invalidation (D0-003)
tests/test_surfaces.py             # incl. test_red_states_have_two_exits   (D0-004)
tests/test_legislature.py
tests/test_recursive_fixture.py
.contracts/docket-v0.contract.yaml # the recursive fixture (law of this repo)
.contracts/runners.yaml            # runners: {test: "uv run pytest -q {ref}"}
```

---

### Task 1: Review — read path and accept

**Files:**
- Modify: `src/docket/cli.py`, `src/docket/render.py`
- Test: `tests/test_review.py`

- [ ] **Step 1: Failing tests**

`tests/test_review.py`:
```python
import json

from tests.conftest import run_cli, write_history


def _filed(root, clause="C-001", claim="satisfied", **extra):
    payload = {"clause": clause, "claim": claim, "filed_by": "claude-loop#18",
               "rev_at_filing": 1,
               "evidence": [{"kind": "test", "ref": "test_exit_zero", "result": "8/8 PASS"},
                            {"kind": "trace", "ref": "loop transcript #18",
                             "note": "3 iterations, stop=contract-green"}],
               "residual": "token estimation ±15% — flagged, not contracted"}
    payload.update(extra)
    write_history(root, clause, "bundle-001.json", payload)


def test_review_lists_pending(ledger_root, capsys):
    _filed(ledger_root)
    code, out, err = run_cli(["review"], ledger_root, capsys)
    assert code == 0
    assert "C-001" in out and "⚖" in out


def test_review_nothing_pending_says_so(ledger_root, capsys):
    code, out, err = run_cli(["review"], ledger_root, capsys)
    assert code == 0
    assert "nothing to review" in out.lower()


def test_review_shows_bundle(ledger_root, capsys):
    _filed(ledger_root)
    code, out, err = run_cli(["review", "C-001", "--show"], ledger_root, capsys)
    assert "EVIDENCE BUNDLE — C-001" in out
    assert "filed by: claude-loop#18" in out
    assert "claim:" in out and "satisfied" in out
    assert "8/8 PASS" in out
    assert "residual:" in out


def test_review_accept_records_verdict(ledger_root, capsys):
    _filed(ledger_root)
    code, out, err = run_cli(["review", "C-001", "--accept", "--by", "pyro"],
                             ledger_root, capsys)
    assert code == 0
    assert "✔ C-001 accepted · pyro · rev 1" in out
    v = json.loads((ledger_root / ".contracts/evidence/C-001/verdict-001.json").read_text())
    assert v["verdict"] == "accepted" and v["bundle"] == "bundle-001"


def test_review_stale_bundle_needs_refile(ledger_root, capsys):
    from docket.storage import Ledger
    _filed(ledger_root)
    Ledger(ledger_root).append_amendment("demo", {
        "rev": 2, "by": "pyro", "kind": "amend",
        "changes": [{"id": "C-001", "change": "modified"}]})
    p = ledger_root / ".contracts/demo.contract.yaml"
    p.write_text(p.read_text().replace("rev: 1", "rev: 2"))
    code, out, err = run_cli(["review", "C-001", "--accept", "--by", "pyro"],
                             ledger_root, capsys)
    assert code == 2
    assert "stale" in err and "rev" in err
```

Run: `uv run pytest tests/test_review.py -q` — Expected: FAIL (no `review` command).

- [ ] **Step 2: Implement render + command**

Add to `src/docket/render.py`:
```python
def bundle_view(clause, bundle) -> str:
    lines = [f"EVIDENCE BUNDLE — {clause.id} {short_name(clause)}"
             f"     filed by: {bundle.get('filed_by', '?')}",
             f"  claim:     {bundle.get('claim')}"]
    rows = []
    for e in bundle.get("evidence", []):
        right = e.get("result") or e.get("note") or ""
        rows.append((e.get("ref", e.get("kind", "?")), right))
    width = max((len(r[0]) for r in rows), default=0) + 6
    for i, (ref, right) in enumerate(rows):
        prefix = "  evidence:  " if i == 0 else "             "
        lines.append(f"{prefix}{ref:<{width}}{right}")
    if bundle.get("residual"):
        lines.append(f"  residual:  {bundle['residual']}")
    if bundle.get("claim") == "stuck":
        lines.insert(0, f"FAILURE REPORT — {bundle.get('filed_by', '?')}")
        del lines[1]
        lines.insert(1, f"  stuck on: {bundle.get('stuck_on', '?')}")
    return "\n".join(lines)


def calibration_line(defects: int, total: int, worst: bool) -> str:
    base = f"clause calibration: {defects} defect{'s' * (defects != 1)} in {total} verdict{'s' * (total != 1)}"
    return base + (" — worst clause on the books" if worst else "")
```

Add to `src/docket/cli.py` (parser):
```python
    rev = sub.add_parser("review", help="verdicts on evidence bundles and failure reports")
    rev.add_argument("clause", nargs="?", default=None)
    rev.add_argument("--show", action="store_true")
    rev.add_argument("--accept", action="store_true")
    rev.add_argument("--reject", choices=["work", "evidence", "clause"], default=None)
    rev.add_argument("--reason", default=None)
    rev.add_argument("--verdict", choices=["split", "defer", "reassign", "reenter"],
                     default=None)
    rev.add_argument("--from", dest="from_file", type=Path, default=None)
    rev.add_argument("--note", default=None)
    rev.add_argument("--by", default=None)
```

Command (this task implements list/show/accept; reject in Task 2, failure verdicts in Task 5):
```python
def _pending(led, root):
    """(contract, clause, bundle) for every valid bundle without a verdict."""
    from docket.state import derive_views
    out = []
    for contract in led.contracts():
        for clause in contract.clauses:
            floor = led.last_amend_rev(contract.contract, clause.id)
            judged = {v.get("bundle") for v in led.records(clause.id, "verdict")}
            for b in led.records(clause.id, "bundle"):
                if b["_file"].removesuffix(".json") in judged:
                    continue
                out.append((contract, clause, b, floor))
    return out


def cmd_review(args) -> int:
    import getpass
    from docket.render import bundle_view, calibration_line
    from docket.storage import Ledger

    led = Ledger(args.root)
    pend = _pending(led, args.root)
    if args.clause is None:
        if not pend:
            print("nothing to review — the docket is quiet")
            return 0
        for contract, clause, b, _ in pend:
            kind = "failure report" if b.get("claim") == "stuck" else "bundle"
            print(f"⚖ {clause.id} {kind} {b['_file']} filed by {b.get('filed_by')}")
        return 0

    mine = [(c, cl, b, f) for c, cl, b, f in pend if cl.id == args.clause]
    if not mine:
        print(f"docket review: nothing pending on {args.clause}", file=sys.stderr)
        return 2
    contract, clause, bundle, floor = mine[-1]
    by = args.by or getpass.getuser()

    if int(bundle.get("rev_at_filing", 0)) < floor or contract.rev != bundle.get("rev_at_filing"):
        print(f"docket review: bundle is stale — filed at rev {bundle.get('rev_at_filing')}, "
              f"law is rev {contract.rev}. refile against current law.", file=sys.stderr)
        return 2

    print(bundle_view(clause, bundle))
    if args.show:
        return 0

    if args.accept:
        p = led.append_record(clause.id, "verdict", {
            "bundle": bundle["_file"].removesuffix(".json"), "clause": clause.id,
            "verdict": "accepted", "by": by, "rev": contract.rev})
        print(f"✔ {clause.id} accepted · {by} · rev {contract.rev} · → "
              f"{p.relative_to(args.root)}")
        return 0
    # --reject: Task 2; --verdict: Task 5; interactive: Task 2 step 4
    print("review: pass --accept, --reject TYPE --reason …, or --verdict …",
          file=sys.stderr)
    return 2
```

Dispatch: add `"review": cmd_review`.

- [ ] **Step 3: Run & commit**

Run: `uv run pytest tests/test_review.py -q` — Expected: PASS (reject tests come next).

```bash
git add src/docket/cli.py src/docket/render.py tests/test_review.py
git commit -m "review: pending list, bundle view, accept verdict, stale-rev refusal"
```

---

### Task 2: Typed rejection + calibration (D0-005)

**Files:**
- Modify: `src/docket/cli.py`
- Test: `tests/test_review.py` (extend)

- [ ] **Step 1: Failing tests**

Append to `tests/test_review.py`:
```python
def test_reject_requires_typed_reason(ledger_root, capsys):
    _filed(ledger_root)
    code, out, err = run_cli(["review", "C-001", "--reject", "clause"],
                             ledger_root, capsys)
    assert code == 2
    assert "reason" in err


def test_typed_rejection_calibration(ledger_root, capsys):
    """D0-005: typed reason recorded; clause-defect counts queryable per clause."""
    _filed(ledger_root)
    code, out, err = run_cli(
        ["review", "C-001", "--reject", "clause",
         "--reason", "evidence satisfies the clause, but this is not what I meant",
         "--by", "pyro"], ledger_root, capsys)
    assert code == 0
    assert "CLAUSE DEFECT" in out
    assert "flagged for amendment" in out
    assert "clause calibration: 1 defect in 1 verdict" in out
    assert "fix the code" in out and "amend the contract" in out  # D0-004 on reject

    import json
    v = json.loads((ledger_root / ".contracts/evidence/C-001/verdict-001.json").read_text())
    assert v["verdict"] == "rejected"
    assert v["rejection_type"] == "clause-defect"
    assert v["reason"].startswith("evidence satisfies")

    # queryable per clause: derived calibration on the view
    from docket.state import derive_views
    from docket.storage import Ledger
    led = Ledger(ledger_root)
    view = {x.clause.id: x for x in derive_views(led.contract("demo"), led, ledger_root)}
    assert view["C-001"].calibration == (1, 1)


def test_work_and_evidence_defects_typed(ledger_root, capsys):
    _filed(ledger_root)
    code, out, err = run_cli(["review", "C-001", "--reject", "work",
                              "--reason", "misses the precedence rule", "--by", "pyro"],
                             ledger_root, capsys)
    assert "WORK DEFECT" in out
    _filed(ledger_root)  # bundle-002
    code, out, err = run_cli(["review", "C-001", "--reject", "evidence",
                              "--reason", "no runnable reference", "--by", "pyro"],
                             ledger_root, capsys)
    assert "EVIDENCE DEFECT" in out
    assert "calibration: 0 defects in 2 verdicts" in out  # only clause defects count
```

Wait — first rejection in `test_work_and_evidence_defects_typed` uses a fresh ledger (fixture), so verdict counts restart; the second `_filed` files `bundle-002` after `bundle-001` got its verdict. The final calibration line counts clause-defects only: 0 of 2. The test is consistent.

Run: `uv run pytest tests/test_review.py -q` — Expected: new tests FAIL.

- [ ] **Step 2: Implement reject branch in `cmd_review`**

Insert before the final error return:
```python
    if args.reject:
        if not args.reason:
            print("docket review: rejection requires a reason (--reason)", file=sys.stderr)
            return 2
        rtype = f"{args.reject}-defect"
        led.append_record(clause.id, "verdict", {
            "bundle": bundle["_file"].removesuffix(".json"), "clause": clause.id,
            "verdict": "rejected", "rejection_type": rtype,
            "reason": args.reason, "by": by, "rev": contract.rev})
        all_v = led.records(clause.id, "verdict")
        defects = sum(1 for v in all_v if v.get("rejection_type") == "clause-defect")
        # worst on the books = max defect ratio among clauses with ≥1 defect
        worst = _is_worst(led, contract, clause.id)
        print(f"→ recorded as {rtype.replace('-', ' ').upper()}"
              + (" (not work defect)" if rtype == "clause-defect" else ""))
        tail = calibration_line(defects, len(all_v), worst)
        if rtype == "clause-defect":
            print(f"  {clause.id} flagged for amendment · {tail}")
        else:
            print(f"  {tail}")
        from docket.render import TWO_EXITS
        print()
        print(TWO_EXITS)
        return 0


def _is_worst(led, contract, clause_id: str) -> bool:
    def ratio(cid):
        vs = led.records(cid, "verdict")
        d = sum(1 for v in vs if v.get("rejection_type") == "clause-defect")
        return (d / len(vs)) if vs else 0.0
    mine = ratio(clause_id)
    return mine > 0 and all(ratio(c.id) <= mine for c in contract.clauses)
```

- [ ] **Step 3: Interactive prompt (thin wrapper, same code path)**

In `cmd_review`, where the final error return was, add a TTY fallback:
```python
    if sys.stdin.isatty():
        choice = input("accept / reject / comment? > ").strip().lower()
        if choice == "accept":
            args.accept = True
            return cmd_review(args)
        if choice == "reject":
            args.reject = input("type (work/evidence/clause)? > ").strip()
            args.reason = input("reason? > ").strip()
            return cmd_review(args)
        print(f"comment noted (not recorded — verdicts only): {choice}")
        return 0
    print("review: pass --accept, --reject TYPE --reason …, or --verdict …",
          file=sys.stderr)
    return 2
```

(Recursion re-enters with flags set; the bundle re-print is acceptable v0 noise.)

- [ ] **Step 4: Run & commit**

Run: `uv run pytest tests/test_review.py -q` — Expected: PASS.

```bash
git add src/docket/cli.py tests/test_review.py
git commit -m "typed rejections: work/evidence/clause defects, per-clause calibration (D0-005)"
```

---

### Task 3: The two-exits invariant test (D0-004)

**Files:**
- Test: `tests/test_surfaces.py`

- [ ] **Step 1: Write the aggregate invariant test (should pass already — it's a lock, not a feature)**

`tests/test_surfaces.py`:
```python
"""D0-004: every red state surfaced by status/check/review prints at least
one work-exit and one law-exit."""
import re

from tests.conftest import run_cli, write_history

WORK_EXIT = re.compile(r"fix the code|redo the work|change the work")
LAW_EXIT = re.compile(r"amend the contract|change the law|docket amend")


def _red_check(root):
    (root / "tests").mkdir(exist_ok=True)
    (root / "tests/test_demo.py").write_text(
        "def test_exit_zero():\n    assert False, 'drifted'\n")


def test_red_states_have_two_exits(ledger_root, capsys):
    _red_check(ledger_root)

    # check FAIL
    _, out, _ = run_cli(["check", "C-001"], ledger_root, capsys)
    assert WORK_EXIT.search(out) and LAW_EXIT.search(out), out

    # status with broken clause
    _, out, _ = run_cli(["status"], ledger_root, capsys)
    assert WORK_EXIT.search(out) and LAW_EXIT.search(out), out

    # review rejection
    write_history(ledger_root, "C-001", "bundle-001.json",
                  {"clause": "C-001", "claim": "satisfied", "filed_by": "l",
                   "rev_at_filing": 1, "evidence": []})
    _, out, _ = run_cli(["review", "C-001", "--reject", "work",
                         "--reason", "missed it", "--by", "pyro"],
                        ledger_root, capsys)
    assert WORK_EXIT.search(out) and LAW_EXIT.search(out), out
```

Run: `uv run pytest tests/test_surfaces.py -q` — Expected: PASS (if any surface lacks an exit, fix `render.py`, not the test).

- [ ] **Step 2: Commit**

```bash
git add tests/test_surfaces.py
git commit -m "lock the two-exits invariant across check/status/review (D0-004)"
```

---

### Task 4: Legislature — drafts, amend, concurrent-draft refusal

**Files:**
- Create: `src/docket/legislature.py`
- Modify: `src/docket/cli.py`
- Test: `tests/test_legislature.py`

- [ ] **Step 1: Failing tests**

`tests/test_legislature.py`:
```python
from pathlib import Path

from tests.conftest import run_cli

CLAUSE_EDIT = """\
id: C-001
obligation: >
  demo MUST exit 0 on success and report version with --version.
acceptance:
  test: tests/test_demo.py::test_exit_zero
anchors:
  - decision: D-001
"""


def test_amend_creates_draft_with_diff_and_impact(ledger_root, capsys, tmp_path):
    f = tmp_path / "edit.yaml"
    f.write_text(CLAUSE_EDIT)
    code, out, err = run_cli(["amend", "C-001", "--from", str(f)], ledger_root, capsys)
    assert code == 0
    assert "draft rev 2: C-001 obligation changed" in out
    assert "admission re-check" in out
    assert "sign-off required" in out
    assert (ledger_root / ".contracts/drafts/demo.rev2.yaml").exists()
    # law unchanged until signed
    assert "rev: 1" in (ledger_root / ".contracts/demo.contract.yaml").read_text()


def test_amend_two_laws_refused_at_readmission(ledger_root, capsys, tmp_path):
    f = tmp_path / "edit.yaml"
    f.write_text(CLAUSE_EDIT.replace(
        "demo MUST exit 0 on success and report version with --version.",
        "demo MUST exit 0 and MUST print version."))
    code, out, err = run_cli(["amend", "C-001", "--from", str(f)], ledger_root, capsys)
    assert code == 2
    assert "A8" in err
    assert not (ledger_root / ".contracts/drafts/demo.rev2.yaml").exists()


def test_concurrent_draft_refused(ledger_root, capsys, tmp_path):
    f = tmp_path / "edit.yaml"
    f.write_text(CLAUSE_EDIT)
    assert run_cli(["amend", "C-001", "--from", str(f)], ledger_root, capsys)[0] == 0
    code, out, err = run_cli(["amend", "C-001", "--from", str(f)], ledger_root, capsys)
    assert code == 2
    assert "draft" in err and "exists" in err


def test_retire_draft(ledger_root, capsys):
    code, out, err = run_cli(["amend", "C-001", "--retire"], ledger_root, capsys)
    assert code == 0
    assert "status: retired" in (ledger_root / ".contracts/drafts/demo.rev2.yaml").read_text()
```

Run: `uv run pytest tests/test_legislature.py -q` — Expected: FAIL.

- [ ] **Step 2: Implement `src/docket/legislature.py`**

```python
"""The legislature: draft → re-admission → signature → rev bump → invalidation.

Law changes never touch the contract file directly; they become a draft at
.contracts/drafts/<name>.rev<N>.yaml. docket sign applies it. One draft per
contract at a time.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from docket.accord import DoorReport, run_door
from docket.model import dump_contract, load_contract_data
from docket.storage import Ledger


class DraftExists(Exception):
    pass


class DraftRefused(Exception):
    def __init__(self, report: DoorReport):
        self.report = report
        super().__init__("draft refused at re-admission")


def draft_path(led: Ledger, name: str, rev: int) -> Path:
    return led.dir / "drafts" / f"{name}.rev{rev}.yaml"


def any_draft(led: Ledger, name: str) -> Path | None:
    d = led.dir / "drafts"
    hits = sorted(d.glob(f"{name}.rev*.yaml")) if d.exists() else []
    return hits[0] if hits else None


def next_clause_id(data: dict) -> str:
    prefix, top = "C", 0
    for c in data.get("clauses", []):
        m = re.match(r"^([A-Z][A-Z0-9]*)-(\d+)", str(c.get("id", "")))
        if m:
            prefix = m.group(1)
            top = max(top, int(m.group(2)))
    return f"{prefix}-{top + 1:03d}"


def clause_index(data: dict, clause_id: str) -> int:
    for i, c in enumerate(data.get("clauses", [])):
        if c.get("id") == clause_id:
            return i
    raise KeyError(clause_id)


def create_draft(led: Ledger, name: str, mutate,
                 sign_unanchored: str | None = None) -> tuple[Path, DoorReport, dict]:
    """mutate(data) edits the raw contract mapping in place."""
    if (existing := any_draft(led, name)):
        raise DraftExists(str(existing))
    data = led.contract_data(name)
    old = {c["id"]: dict(c) for c in data.get("clauses", [])}
    mutate(data)
    data["rev"] = int(data["rev"]) + 1
    report = run_door(data, led.root, sign_unanchored=sign_unanchored)
    if report.refusals:
        raise DraftRefused(report)
    p = draft_path(led, name, data["rev"])
    dump_contract(data, p)
    if report.overrides:  # decision 25: persisted so sign's re-door honors them
        p.with_suffix(".overrides.json").write_text(json.dumps(report.overrides))
    changes = diff_changes(old, data)
    return p, report, {"rev": data["rev"], "changes": changes}


def diff_changes(old: dict[str, dict], new_data: dict) -> list[dict]:
    new = {c["id"]: dict(c) for c in new_data.get("clauses", [])}
    out = []
    for cid in new:
        if cid not in old:
            out.append({"id": cid, "change": "added"})
        elif _norm(new[cid]) != _norm(old[cid]):
            kind = "retired" if new[cid].get("status") == "retired" \
                and old[cid].get("status") != "retired" else "modified"
            out.append({"id": cid, "change": kind})
    for cid in old:
        if cid not in new:
            out.append({"id": cid, "change": "removed"})  # shouldn't happen: retire, don't delete
    return out


def _norm(c: dict) -> dict:
    return {k: (str(v).strip() if isinstance(v, str) else v)
            for k, v in c.items() if not str(k).startswith("_")}


def apply_sign(led: Ledger, name: str, rev: int, by: str, date: str) -> dict:
    """Apply pending draft (rev > current) or ratify current rev."""
    current = led.contract_data(name)
    cur_rev = int(current["rev"])
    draft = draft_path(led, name, rev)

    if draft.exists():
        data = load_contract_data(draft)
        sidecar = draft.with_suffix(".overrides.json")
        overrides = json.loads(sidecar.read_text()) if sidecar.exists() else []
        authority = overrides[0]["signed_by"] if overrides else None
        # re-admission at sign time too; granted A2 overrides are honored
        report = run_door(data, led.root, sign_unanchored=authority)
        if report.refusals:
            raise DraftRefused(report)
        old = {c["id"]: dict(c) for c in current.get("clauses", [])}
        changes = diff_changes(old, data)
        data.setdefault("signed", []).append({"rev": rev, "by": by, "date": date})
        dump_contract(data, led.contract_path(name))
        draft.unlink()
        sidecar.unlink(missing_ok=True)
        led.append_amendment(name, {"rev": rev, "by": by, "kind": "amend",
                                    "changes": changes, "overrides": overrides})
        return {"applied": "draft", "rev": rev, "changes": changes}

    if rev == cur_rev:
        current.setdefault("signed", []).append({"rev": rev, "by": by, "date": date})
        dump_contract(current, led.contract_path(name))
        led.append_amendment(name, {"rev": rev, "by": by, "kind": "sign", "changes": []})
        return {"applied": "ratify", "rev": rev, "changes": []}

    raise FileNotFoundError(f"no draft for rev {rev} (law is rev {cur_rev})")
```

- [ ] **Step 3: CLI `amend`**

Parser:
```python
    amd = sub.add_parser("amend", help="draft a law change (sign to enact)")
    amd.add_argument("clause")
    amd.add_argument("--from", dest="from_file", type=Path, default=None)
    amd.add_argument("--edit", action="store_true")
    amd.add_argument("--retire", action="store_true")
```

Command:
```python
def cmd_amend(args) -> int:
    import os
    import subprocess as sp
    import tempfile

    from ruamel.yaml import YAML
    from docket.legislature import DraftExists, DraftRefused, clause_index, create_draft
    from docket.state import derive_views
    from docket.storage import Ledger

    led = Ledger(args.root)
    contracts = [c for c in led.contracts() if any(cl.id == args.clause for cl in c.clauses)]
    if not contracts:
        print(f"docket amend: unknown clause {args.clause}", file=sys.stderr)
        return 2
    name = contracts[0].contract
    yaml = YAML(typ="rt")

    if args.retire:
        def mutate(data):
            data["clauses"][clause_index(data, args.clause)]["status"] = "retired"
    else:
        if args.edit and not args.from_file:
            data = led.contract_data(name)
            cur = data["clauses"][clause_index(data, args.clause)]
            with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as tf:
                yaml.dump(dict(cur), tf)
                tmp = tf.name
            sp.run([os.environ.get("EDITOR", "vi"), tmp], check=True)
            args.from_file = Path(tmp)
        if not args.from_file:
            print("docket amend: pass --from FILE, --edit, or --retire", file=sys.stderr)
            return 2
        replacement = yaml.load(Path(args.from_file).read_text())

        def mutate(data):
            data["clauses"][clause_index(data, args.clause)] = replacement

    try:
        p, report, info = create_draft(led, name, mutate)
    except DraftExists as e:
        print(f"docket amend: a draft already exists ({e}) — sign or discard it first",
              file=sys.stderr)
        return 2
    except DraftRefused as e:
        for f in e.report.refusals:
            print(f"✘ {f.clause_id} [{f.check}] {f.message}", file=sys.stderr)
        print("docket amend: draft refused at re-admission — law unchanged", file=sys.stderr)
        return 2

    changed = ", ".join(f"{c['id']} {c['change']}" for c in info["changes"]) or "no changes"
    old_clause = next(cl for cl in contracts[0].clauses if cl.id == args.clause)
    field = "status" if args.retire else "obligation"
    print(f"draft rev {info['rev']}: {args.clause} {field} changed")
    print(f"  changes: {changed}")
    print(f"  admission re-check ........ ✔ still checkable, anchors intact")
    n_bundles = len(led.records(args.clause, "bundle"))
    if n_bundles:
        print(f"  impact: {n_bundles} evidence bundle{'s' * (n_bundles != 1)} invalidated "
              f"({args.clause}) → re-verdict needed")
    print(f"sign-off required: docket sign rev{info['rev']}")
    return 0
```

Dispatch: add `"amend": cmd_amend`.

- [ ] **Step 4: Run & commit**

Run: `uv run pytest tests/test_legislature.py -q` — Expected: PASS.

```bash
git add src/docket/legislature.py src/docket/cli.py tests/test_legislature.py
git commit -m "legislature: drafts with re-admission, amend --from/--edit/--retire, one draft at a time"
```

---

### Task 5: `docket sign` — checklist, rev bump, scoped invalidation (D0-003)

**Files:**
- Modify: `src/docket/cli.py`, `src/docket/render.py`
- Test: `tests/test_amend.py`

- [ ] **Step 1: Failing tests**

`tests/test_amend.py`:
```python
import json

from tests.conftest import run_cli, write_history

TWO_CLAUSES = """\
contract: demo2
rev: 1
source: test fixture
signed:
  - {rev: 1, by: pyro, date: 2026-06-12}
clauses:
  - id: C-001
    obligation: >
      demo2 MUST exit 0 on success.
    acceptance:
      test: tests/test_demo.py::test_a
    anchors:
      - decision: D-001
  - id: C-002
    obligation: >
      demo2 MUST NOT write to stdout on error.
    acceptance:
      test: tests/test_demo.py::test_b
    anchors:
      - decision: D-002
"""

EDIT = """\
id: C-002
obligation: >
  demo2 MUST NOT write anything but JSON to stdout on error.
acceptance:
  test: tests/test_demo.py::test_b
anchors:
  - decision: D-002
"""


def _accepted(root, clause):
    write_history(root, clause, "bundle-001.json",
                  {"clause": clause, "claim": "satisfied", "filed_by": "l",
                   "rev_at_filing": 1, "evidence": [{"kind": "test", "ref": "t",
                                                     "result": "PASS"}]})
    write_history(root, clause, "verdict-001.json",
                  {"bundle": "bundle-001", "clause": clause, "verdict": "accepted",
                   "by": "pyro", "rev": 1})


def test_rev_bump_scoped_invalidation(tmp_path, capsys):
    """D0-003: amend bumps rev; only the amended clause's evidence dies."""
    (tmp_path / ".contracts").mkdir()
    (tmp_path / ".contracts/demo2.contract.yaml").write_text(TWO_CLAUSES)
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests/test_demo.py").write_text("def test_a(): pass\ndef test_b(): pass\n")
    _accepted(tmp_path, "C-001")
    _accepted(tmp_path, "C-002")

    edit = tmp_path / "edit.yaml"
    edit.write_text(EDIT)
    assert run_cli(["amend", "C-002", "--from", str(edit)], tmp_path, capsys)[0] == 0
    code, out, err = run_cli(["sign", "rev2", "--by", "pyro"], tmp_path, capsys)
    assert code == 0
    assert "rev 2 in force" in out and "amendment recorded" in out

    law = (tmp_path / ".contracts/demo2.contract.yaml").read_text()
    assert "rev: 2" in law
    assert law.count("rev: 2") >= 1 and "by: pyro" in law   # signed entry appended

    from docket.state import derive_views
    from docket.storage import Ledger
    led = Ledger(tmp_path)
    views = {v.clause.id: v for v in derive_views(led.contract("demo2"), led, tmp_path)}
    assert views["C-001"].state == "holding"      # untouched clause keeps its evidence
    assert views["C-002"].state == "stale"        # amended clause needs re-verdict


def test_sign_prints_checklist(tmp_path, capsys):
    (tmp_path / ".contracts").mkdir()
    (tmp_path / ".contracts/demo2.contract.yaml").write_text(TWO_CLAUSES)
    edit = tmp_path / "edit.yaml"
    edit.write_text(EDIT)
    run_cli(["amend", "C-002", "--from", str(edit)], tmp_path, capsys)
    code, out, err = run_cli(["sign", "rev2", "--by", "pyro"], tmp_path, capsys)
    for q in ("Desire", "Domain", "Feasibility", "Oracle", "Risk"):
        assert q in out


def test_sign_ratifies_current_rev_without_draft(tmp_path, capsys):
    (tmp_path / ".contracts").mkdir()
    (tmp_path / ".contracts/demo2.contract.yaml").write_text(
        TWO_CLAUSES.replace("signed:\n  - {rev: 1, by: pyro, date: 2026-06-12}",
                            "signed: []"))
    code, out, err = run_cli(["sign", "rev1", "--by", "pyro"], tmp_path, capsys)
    assert code == 0
    assert "rev 1 in force" in out
    assert "by: pyro" in (tmp_path / ".contracts/demo2.contract.yaml").read_text()


def test_sign_unknown_rev_fails(tmp_path, capsys):
    (tmp_path / ".contracts").mkdir()
    (tmp_path / ".contracts/demo2.contract.yaml").write_text(TWO_CLAUSES)
    code, out, err = run_cli(["sign", "rev7", "--by", "pyro"], tmp_path, capsys)
    assert code == 2
    assert "no draft" in err
```

Run: `uv run pytest tests/test_amend.py -q` — Expected: FAIL.

- [ ] **Step 2: Implement**

Add to `src/docket/render.py`:
```python
CHECKLIST = """\
SIGNING CHECKLIST — five questions; the answers are your due diligence, not ledger state
  Desire      — is this the behavior we actually want?
  Domain      — is this true in the real domain?
  Feasibility — can this be built and maintained within constraints?
  Oracle      — how do we know pass/fail?
  Risk        — is this validation depth enough for the cost of being wrong?"""
```

CLI parser + command:
```python
    sgn = sub.add_parser("sign", help="enact a draft (or ratify the current rev)")
    sgn.add_argument("rev")                       # "rev2" | "2"
    sgn.add_argument("--by", default=None)
```

```python
def cmd_sign(args) -> int:
    import datetime as dt
    import getpass
    import re as _re

    from docket.legislature import DraftRefused, any_draft, apply_sign
    from docket.render import CHECKLIST
    from docket.storage import Ledger

    led = Ledger(args.root)
    m = _re.fullmatch(r"(?:rev\s*)?(\d+)", args.rev)
    if not m:
        print(f"docket sign: cannot parse rev {args.rev!r}", file=sys.stderr)
        return 2
    rev = int(m.group(1))
    by = args.by or getpass.getuser()
    today = dt.date.today().isoformat()

    # find the contract this rev belongs to: a draft with that rev, else a
    # contract currently at that rev (ratification)
    target = None
    for contract in led.contracts():
        if any_draft(led, contract.contract) and \
                any_draft(led, contract.contract).name.endswith(f"rev{rev}.yaml"):
            target = contract.contract
            break
        if contract.rev == rev and not any_draft(led, contract.contract):
            target = contract.contract
    if target is None:
        print(f"docket sign: no draft for rev {rev} and no contract at rev {rev}",
              file=sys.stderr)
        return 2

    print(CHECKLIST)
    try:
        result = apply_sign(led, target, rev, by, today)
    except DraftRefused as e:
        for f in e.report.refusals:
            print(f"✘ {f.clause_id} [{f.check}] {f.message}", file=sys.stderr)
        print("docket sign: draft refused at re-admission — law unchanged", file=sys.stderr)
        return 2
    except FileNotFoundError as e:
        print(f"docket sign: {e}", file=sys.stderr)
        return 2

    print(f"✔ rev {rev} in force · amendment recorded ({result['applied']})")
    for ch in result["changes"]:
        print(f"  {ch['id']} {ch['change']}")
    return 0
```

Dispatch: add `"sign": cmd_sign`.

- [ ] **Step 3: Run & commit**

Run: `uv run pytest tests/test_amend.py tests/test_state.py -q` — Expected: PASS (the stale derivation from Plan 1 Task 7 now gets exercised through the real sign path).

```bash
git add src/docket/cli.py src/docket/render.py tests/test_amend.py
git commit -m "docket sign: checklist, draft enactment, ratification, scoped invalidation (D0-003)"
```

---

### Task 6: `docket add` — new law mid-flight

**Files:**
- Modify: `src/docket/cli.py`
- Test: `tests/test_legislature.py` (extend)

- [ ] **Step 1: Failing tests**

Append to `tests/test_legislature.py`:
```python
def test_add_drafts_new_clause_with_door_result(ledger_root, capsys):
    code, out, err = run_cli(
        ["add", "--obligation", "demo MUST reject unknown flags with exit 2.",
         "--acceptance-test", "tests/test_cli_flags.py::test_unknown_flag",
         "--anchor", "incident:postmortem-2026-06-14-flags"],
        ledger_root, capsys)
    assert code == 0
    assert "draft C-002" in out
    assert "door: ✔ admitted" in out and "PENDING-HARNESS" in out
    assert "sign-off" in out
    draft = (ledger_root / ".contracts/drafts/demo.rev2.yaml").read_text()
    assert "C-002" in draft and "postmortem-2026-06-14-flags" in draft


def test_add_refused_clause_creates_no_draft(ledger_root, capsys):
    code, out, err = run_cli(
        ["add", "--obligation", "demo SHOULD be nice.",
         "--acceptance-test", "tests/test_x.py::test_x",
         "--anchor", "decision:D-009"],
        ledger_root, capsys)
    assert code == 2
    assert "A4" in err
    assert not list((ledger_root / ".contracts").glob("drafts/*"))


def test_add_human_verdict_acceptance(ledger_root, capsys):
    code, out, err = run_cli(
        ["add", "--obligation", "Error messages MUST NOT contain stack traces.",
         "--acceptance-human", "--anchor", "decision:D-010"],
        ledger_root, capsys)
    assert code == 0
    assert "verdict: human" in (ledger_root / ".contracts/drafts/demo.rev2.yaml").read_text()


def test_add_sign_unanchored_override_survives_signing(ledger_root, capsys):
    """Concepts/03: the A2 override is legal on add, signed, and recorded."""
    import json
    code, out, err = run_cli(
        ["add", "--obligation", "demo MUST log warnings to stderr.",
         "--acceptance-test", "tests/test_log.py::test_stderr",
         "--sign-unanchored", "pyro"],
        ledger_root, capsys)
    assert code == 0
    assert "admitted unanchored — signed by pyro" in out
    assert (ledger_root / ".contracts/drafts/demo.rev2.overrides.json").exists()

    code, out, err = run_cli(["sign", "rev2", "--by", "pyro"], ledger_root, capsys)
    assert code == 0                              # re-door honors the granted override
    amends = sorted((ledger_root / ".contracts/amendments/demo").glob("rev-002*.json"))
    rec = json.loads(amends[-1].read_text())
    assert any(o["check"] == "A2" and o["signed_by"] == "pyro"
               for o in rec["overrides"])
    assert not (ledger_root / ".contracts/drafts/demo.rev2.overrides.json").exists()
```

Run: `uv run pytest tests/test_legislature.py -q` — Expected: new tests FAIL.

- [ ] **Step 2: Implement**

Parser:
```python
    add = sub.add_parser("add", help="draft a new clause on any horse")
    add.add_argument("--contract", default=None, help="contract name (optional if only one)")
    add.add_argument("--id", default=None)
    add.add_argument("--obligation", required=True)
    add.add_argument("--anchor", action="append", default=[],
                     metavar="TYPE:VALUE", help="e.g. incident:postmortem-x (repeatable)")
    add.add_argument("--acceptance-test", default=None, metavar="REF")
    add.add_argument("--acceptance-metric", default=None, metavar="SCRIPT")
    add.add_argument("--threshold", default=None)
    add.add_argument("--acceptance-command", default=None, metavar="CMD")
    add.add_argument("--expect", default=None)
    add.add_argument("--acceptance-human", action="store_true")
    add.add_argument("--risk", choices=["low", "medium", "high"], default=None)
    add.add_argument("--evidence-required", default=None, metavar="KIND,KIND")
    add.add_argument("--note", default=None)
    add.add_argument("--sign-unanchored", metavar="AUTHORITY", default=None)
```

Command:
```python
def cmd_add(args) -> int:
    from docket.legislature import DraftExists, DraftRefused, create_draft, next_clause_id
    from docket.storage import Ledger

    led = Ledger(args.root)
    contracts = led.contracts()
    if args.contract:
        names = [c.contract for c in contracts if c.contract == args.contract]
    elif len(contracts) == 1:
        names = [contracts[0].contract]
    else:
        print("docket add: multiple contracts — pass --contract NAME", file=sys.stderr)
        return 2
    if not names:
        print(f"docket add: unknown contract {args.contract}", file=sys.stderr)
        return 2
    name = names[0]

    accept_flags = [bool(args.acceptance_test), bool(args.acceptance_metric),
                    bool(args.acceptance_command), args.acceptance_human]
    if sum(accept_flags) != 1:
        print("docket add: exactly one acceptance (--acceptance-test | "
              "--acceptance-metric --threshold | --acceptance-command --expect | "
              "--acceptance-human)", file=sys.stderr)
        return 2
    if args.acceptance_test:
        acceptance = {"test": args.acceptance_test}
    elif args.acceptance_metric:
        if not args.threshold:
            print("docket add: --acceptance-metric needs --threshold", file=sys.stderr)
            return 2
        acceptance = {"metric": args.acceptance_metric, "threshold": args.threshold}
    elif args.acceptance_command:
        if not args.expect:
            print("docket add: --acceptance-command needs --expect", file=sys.stderr)
            return 2
        acceptance = {"command": args.acceptance_command, "expect": args.expect}
    else:
        acceptance = {"verdict": "human"}

    anchors = []
    for a in args.anchor:
        typ, _, val = a.partition(":")
        anchors.append({typ: val})

    new_id = args.id

    def mutate(data):
        nonlocal new_id
        new_id = new_id or next_clause_id(data)
        clause = {"id": new_id, "obligation": args.obligation,
                  "acceptance": acceptance, "anchors": anchors}
        if args.risk:
            clause["risk"] = args.risk
        if args.evidence_required:
            clause["evidence_required"] = args.evidence_required.split(",")
        if args.note:
            clause["notes"] = args.note
        data["clauses"].append(clause)

    try:
        p, report, info = create_draft(led, name, mutate,
                                       sign_unanchored=args.sign_unanchored)
    except DraftExists as e:
        print(f"docket add: a draft already exists ({e})", file=sys.stderr)
        return 2
    except DraftRefused as e:
        for f in e.report.refusals:
            print(f"✘ {f.clause_id or new_id} [{f.check}] {f.message}", file=sys.stderr)
        print("docket add: refused at the door — no draft created", file=sys.stderr)
        return 2

    flags = [f for f in report.flags if f.clause_id == new_id]
    flag_note = f" (flag {', '.join(f.flag for f in flags)})" if flags else ""
    print(f"draft {new_id}: {args.obligation.strip()[:70]}")
    print(f"  door: ✔ admitted{flag_note}")
    for o in report.overrides:
        print(f"  ✍ {o['id']} [A2] admitted unanchored — signed by {o['signed_by']}")
    print(f"sign-off: docket sign rev{info['rev']}")
    return 0
```

Dispatch: add `"add": cmd_add`. The `--sign-unanchored` override works on `add` exactly as on `import` (decision 25, concepts/03): granted at draft time, persisted in the draft's overrides sidecar, honored at sign-time re-admission, recorded in the amendment record.

- [ ] **Step 3: Run & commit**

Run: `uv run pytest tests/test_legislature.py -q` — Expected: PASS.

```bash
git add src/docket/cli.py tests/test_legislature.py
git commit -m "docket add: new law on any horse, door-checked at draft time"
```

---

### Task 7: Failure-report verdicts — the dead-loop exits

**Files:**
- Modify: `src/docket/cli.py`
- Test: `tests/test_review.py` (extend)

- [ ] **Step 1: Failing tests**

Append to `tests/test_review.py`:
```python
SPLIT = """\
- id: C-001a
  obligation: >
    demo MUST exit 0 on success for readable inputs.
  acceptance:
    test: tests/test_demo.py::test_exit_zero
  anchors:
    - decision: D-001
- id: C-001b
  obligation: >
    demo MUST exit 0 within 1s for inputs under 10 MB.
  acceptance:
    test: tests/test_demo.py::test_exit_fast
  anchors:
    - decision: D-001
  status: deferred
"""


def test_failure_report_menu_shows_exits(ledger_root, capsys):
    _filed(ledger_root, claim="stuck", stuck_on="SIGKILL flakes on WSL2")
    code, out, err = run_cli(["review", "C-001", "--show"], ledger_root, capsys)
    assert "FAILURE REPORT" in out
    assert "stuck on: SIGKILL flakes on WSL2" in out


def test_split_replaces_clause_and_signs(ledger_root, capsys, tmp_path):
    _filed(ledger_root, claim="stuck", stuck_on="timing")
    f = tmp_path / "split.yaml"
    f.write_text(SPLIT)
    code, out, err = run_cli(["review", "C-001", "--verdict", "split",
                              "--from", str(f), "--by", "pyro"], ledger_root, capsys)
    assert code == 0
    assert "C-001 → C-001a" in out and "C-001b" in out
    law = (ledger_root / ".contracts/demo.contract.yaml").read_text()
    assert "rev: 2" in law
    assert "C-001a" in law and "C-001b" in law
    assert "status: retired" in law              # original preserved, not deleted

    import json
    v = json.loads((ledger_root / ".contracts/evidence/C-001/verdict-001.json").read_text())
    assert v["verdict"] == "split"


def test_defer_verdict_signs_status_change(ledger_root, capsys):
    _filed(ledger_root, claim="stuck", stuck_on="blocked on upstream")
    code, out, err = run_cli(["review", "C-001", "--verdict", "defer", "--by", "pyro"],
                             ledger_root, capsys)
    assert code == 0
    law = (ledger_root / ".contracts/demo.contract.yaml").read_text()
    assert "status: deferred" in law and "rev: 2" in law


def test_reassign_records_without_law_change(ledger_root, capsys):
    _filed(ledger_root, claim="stuck", stuck_on="flaky")
    code, out, err = run_cli(["review", "C-001", "--verdict", "reassign", "--by", "pyro"],
                             ledger_root, capsys)
    assert code == 0
    law = (ledger_root / ".contracts/demo.contract.yaml").read_text()
    assert "rev: 1" in law                        # law untouched
    # judged failure report → clause back in the work queue
    code, out, err = run_cli(["tasks", "--next"], ledger_root, capsys)
    assert "C-001" in out
```

Run: `uv run pytest tests/test_review.py -q` — Expected: new tests FAIL.

- [ ] **Step 2: Implement the `--verdict` branch in `cmd_review`**

Insert after the `--reject` branch:
```python
    if args.verdict:
        if bundle.get("claim") != "stuck":
            print("docket review: --verdict split/defer/reassign/reenter applies to "
                  "failure reports; use --accept/--reject on satisfied claims",
                  file=sys.stderr)
            return 2
        from docket.legislature import DraftRefused, clause_index, create_draft, apply_sign
        import datetime as dt
        from ruamel.yaml import YAML

        led.append_record(clause.id, "verdict", {
            "bundle": bundle["_file"].removesuffix(".json"), "clause": clause.id,
            "verdict": {"split": "split", "defer": "deferred",
                        "reassign": "reassigned", "reenter": "reentered"}[args.verdict],
            "note": args.note, "by": by, "rev": contract.rev})

        if args.verdict in ("reassign", "reenter"):
            tail = ("back to the work queue" if args.verdict == "reassign"
                    else "back to the producer — the surface itself was wrong")
            print(f"✔ {clause.id} {args.verdict}ed · {tail}")
            print("  …other exits: amend / split / defer "
                  "(change the law) · reassign (change the work)")
            return 0

        # split/defer change the law: draft → re-admission → sign, in one act
        if args.verdict == "split":
            if not args.from_file:
                print("docket review: --verdict split needs --from FILE "
                      "(list of replacement clauses)", file=sys.stderr)
                return 2
            replacements = YAML(typ="rt").load(Path(args.from_file).read_text())

            def mutate(data):
                data["clauses"][clause_index(data, clause.id)]["status"] = "retired"
                data["clauses"].extend(replacements)
        else:  # defer
            def mutate(data):
                data["clauses"][clause_index(data, clause.id)]["status"] = "deferred"

        try:
            p, report, info = create_draft(led, contract.contract, mutate)
        except DraftRefused as e:
            for f in e.report.refusals:
                print(f"✘ {f.clause_id} [{f.check}] {f.message}", file=sys.stderr)
            return 2
        from docket.render import CHECKLIST
        print(CHECKLIST)  # decision 26: inline signing is still signing
        apply_sign(led, contract.contract, info["rev"], by, dt.date.today().isoformat())
        if args.verdict == "split":
            ids = [c["id"] for c in replacements]
            statuses = ["deferred" if c.get("status") == "deferred" else "active"
                        for c in replacements]
            parts = " + ".join(f"{i} ({s})" for i, s in zip(ids, statuses))
            print(f"✔ {clause.id} → {parts}")
        else:
            print(f"✔ {clause.id} deferred · rev {info['rev']} in force")
        print("  …other exits: amend / reassign / defer / re-enter producer")
        return 0
```

- [ ] **Step 3: Run & commit**

Run: `uv run pytest tests/test_review.py -q` — Expected: PASS.

```bash
git add src/docket/cli.py tests/test_review.py
git commit -m "dead-loop exits: split/defer/reassign/reenter verdicts on failure reports"
```

---

### Task 8: Holding refinement + the recursive fixture (the shipping gate)

**Files:**
- Modify: `src/docket/state.py`
- Create: `.contracts/docket-v0.contract.yaml`, `.contracts/runners.yaml`
- Test: `tests/test_state.py` (one case), `tests/test_recursive_fixture.py`

- [ ] **Step 1: Holding-via-green-check (decision 22) — failing test**

Append to `tests/test_state.py`:
```python
def test_holding_via_green_check_without_verdict(ledger_root):
    (ledger_root / "tests").mkdir(); (ledger_root / "tests/test_demo.py").write_text("x=1\n")
    write_history(ledger_root, "C-001", "check-001.json",
                  {"clause": "C-001", "rev": 1, "result": "green", "detail": "PASS"})
    assert _views(ledger_root)["C-001"].state == "holding"
```

In `state.py`, change the final precedence branch:
```python
    elif accepted or (latest_check and latest_check.get("result") == "green"):
        state = "holding"
```
(No bundle qualifier: unjudged bundles already routed to `review`/`stuck` above — decision 22.)

Run: `uv run pytest tests/test_state.py -q` — Expected: PASS.

- [ ] **Step 2: Author the law**

`.contracts/runners.yaml`:
```yaml
runners:
  test: "uv run pytest -q {ref}"
```

`.contracts/docket-v0.contract.yaml` — obligations verbatim from `docs/concepts/03`; D0-007 concretized per decision 23:
```yaml
contract: docket-v0
rev: 1
source: docs/concepts/00..03 (concept convergence, 2026-06-12)
signed: []   # Pyro signs at v0 kickoff — docket sign rev1 --by pyro

clauses:
  - id: D0-001
    obligation: >
      The door MUST refuse clauses without a typed acceptance procedure
      and refuse obligations whose RFC-2119 keyword count is not exactly one.
    acceptance: {test: tests/test_door.py::test_refusals_a1_a4_a6_a7}
    anchors: [{decision: concept-01-door-policy}]

  - id: D0-002
    obligation: >
      Ledger state MUST be derived at runtime from clause files plus
      evidence; no state field may be persisted.
    acceptance: {test: tests/test_state.py::test_no_stored_state}
    anchors: [{decision: concept-01-design-stance}]

  - id: D0-003
    obligation: >
      Amending a clause MUST bump the contract rev and invalidate only
      that clause's evidence bundles.
    acceptance: {test: tests/test_amend.py::test_rev_bump_scoped_invalidation}
    anchors: [{surface: "amend × partial"}]

  - id: D0-004
    obligation: >
      Every red state surfaced by status, check, and review MUST print at
      least one work-exit and one law-exit.
    acceptance: {test: tests/test_surfaces.py::test_red_states_have_two_exits}
    anchors: [{surface: "check × failure"}, {decision: dead-loop-critique}]

  - id: D0-005
    obligation: >
      A rejection MUST record a typed reason (work-defect, evidence-defect,
      or clause-defect) with clause-defect counts queryable per clause.
    acceptance: {test: tests/test_review.py::test_typed_rejection_calibration}
    anchors: [{decision: concept-01-calibration}, {decision: DC-0002-accord-merge}]

  - id: D0-006
    obligation: >
      Docket MUST NOT execute domain logic; acceptance procedures are
      delegated via subprocess and judged by exit code or threshold only.
    acceptance: {test: tests/test_exec.py::test_delegation_only}
    anchors: [{decision: concept-00-boundary-discipline}]

  - id: D0-007
    obligation: >
      A handoff bundle produced by the docket-emitting SFD variant MUST
      import with zero manual reformatting, with every refusal naming its
      door check.
    acceptance:
      command: "rm -rf /tmp/docket-d0007 && mkdir -p /tmp/docket-d0007 && uv run docket --root /tmp/docket-d0007 import fixtures/sfd-variant-run.contract.yaml > /tmp/docket-d0007/out.txt && grep -q 'admitted: 24' /tmp/docket-d0007/out.txt && grep -q 'refused: 0' /tmp/docket-d0007/out.txt"
      expect: >
        exit 0; ≥5 admitted (24 in the golden bundle); refusal lines, when
        present, each cite their door check — citation format pinned by
        tests/test_import.py::test_refusals_cite_door_checks
    anchors: [{compat: sfd-variant-handoff-bundle}]
    notes: >
      Concretized from concepts/03: the prose expect became the exit-code-only
      command pattern the graduation fixtures established (decision 23 in
      docs/plans/2026-06-12-docket-v0-plan-2-*.md). A4 note: the obligation's
      single MUST governs; "with every refusal naming its door check" is the
      same law's manner, not a second law.
```

Note on D0-001's wording: concepts/03 has "MUST refuse … and MUST refuse … lacking exactly one MUST/MUST NOT" — that obligation contains FOUR keyword matches (two operative, two quoted as literals), so our own A8 refuses it. The fixture above keeps exactly one operative MUST and names the quoted keywords descriptively ("RFC-2119 keyword count"), same obligation, door-admissible. This is the recursive fixture doing its job at plan time: docket's own law is the first law the door disciplined. Known v0 limit it exposes: obligations cannot quote RFC-2119 keywords as literals (the door cannot tell mention from use) — record this in the clause's `notes:` if it ever bites a real contract. Surface this in the commit message and to Pyro.

- [ ] **Step 3: Fixture import test (fast, tmp ledger)**

`tests/test_recursive_fixture.py`:
```python
from pathlib import Path

from tests.conftest import run_cli

REPO = Path(__file__).resolve().parents[1]


def test_docket_v0_imports_through_own_door(tmp_path, capsys):
    (tmp_path / ".contracts").mkdir()
    code, out, err = run_cli(
        ["import", str(REPO / ".contracts/docket-v0.contract.yaml")], tmp_path, capsys)
    assert code == 0
    assert "admitted: 7" in out
    assert "refused: 0" in out
```

Run: `uv run pytest tests/test_recursive_fixture.py -q` — Expected: PASS. Any refusal here is a design bug in door or law — fix whichever is wrong (the door wins arguments; the law gets amended).

- [ ] **Step 4: The live gate — green under its own check**

```bash
uv run pytest -q                                   # whole suite first
uv run docket --root . check --all                  # the recursive gate
echo $?
```

Expected: every D0 clause green (D0-007 runs the real import in /tmp), exit 0. The check records land in `.contracts/evidence/D0-*/check-001.json` — commit them; they are the courtroom's first real history. `uv run docket --root . status` should show 7× `✔ holding`.

If a clause is red: the drift line names what diverged. Fix the code or amend the contract — "did not converge, with diagnosis" is a valid fixture outcome, shipping without the fixture passing is not.

- [ ] **Step 5: Commit**

```bash
git add src/docket/state.py tests/test_state.py tests/test_recursive_fixture.py \
        .contracts/ fixtures/
git commit -m "recursive fixture passes: docket-v0 law imports through its own door, green under its own check (D0-001..007; D0-001 wording single-MUST per A8)"
```

---

### Task 9: Closeout — README, falsifier prep, review gate

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Flip the README status line**

Replace the README's `**Status:** concept converged; the tool has no code yet…` paragraph with:

```markdown
**Status:** v0 live — the recursive fixture passes (docket's own requirements
import through its own door and hold green under its own check; see
`.contracts/docket-v0.contract.yaml`). The docket-emitting SFD variant in
[`.agents/skills/surface-first-development/`](.agents/skills/surface-first-development/)
is the producer side. Next: the falsifier run (one real fulfillment loop on
tipsy's signed bundle) per `docs/concepts/03`.
```

- [ ] **Step 2: Verification before claiming done**

```bash
uv run pytest -q                          # all green
uv run docket --root . check --all; echo $?   # 0
uv run docket --root . status             # 7 holding, footer sane
uv run docket --root . audit              # sections render, no manifest warning OK
```

- [ ] **Step 3: Commit + hand off**

```bash
git add README.md
git commit -m "v0: README status — recursive fixture green"
```

Then: (1) Codie review of the courtroom (`/codex:rescue`: legislature draft/sign path, failure-report verdicts, decisions 16–24). (2) Hand Pyro the signature ceremony: `uv run docket --root . sign rev1 --by pyro` — the third human moment, his to perform. (3) The falsifier run (TH-0001: tipsy's 16-clause bundle, one real fulfillment loop, watch the four refutation conditions) is the next session's work — NOT this plan's.

---

## Self-review checklist

- concepts/03 "In" list: import ✔(P1) · add ✔(T6) · check ✔(P1) · status ✔(P1) · audit ✔(P1) · review w/ typed rejection + calibration ✔(T1-2) · amend/sign/add legislature ✔(T4-6) · tasks/file ✔(P1) · single authority, file-native, no daemon/DB ✔ (nothing introduced).
- All seven D0 clause acceptance refs exist as named tests/commands: D0-001 P1/T4 · D0-002 P1/T7+10 · D0-003 T5 · D0-004 T3 · D0-005 T2 · D0-006 P1/T6 · D0-007 T8.
- "Out" list respected: no multi-party authority, no SHOULD, no validator-role fields, no dependency edges, no watch/notify, no TUI/HTML, no CI sugar beyond exit codes, no producer/consumer integration (D0-007 reads a file format, never a producer).
- Type consistency with Plan 1: `Finding(check, clause_id, outcome, message, flag)` · `DoorReport.{admitted,refusals,flags,overrides}` · `Ledger.{records,append_record,append_amendment,last_amend_rev,contract_data,contract_path,runner_template,coverage_manifest}` · `ClauseView.{clause,state,flags,evidence_summary,drift,calibration,last_activity}` · `RunResult.{result,detail,drift,output_tail}` — all uses match definitions.
