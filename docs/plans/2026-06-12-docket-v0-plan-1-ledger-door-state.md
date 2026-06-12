# Docket v0 — Plan 1: Ledger, Door, Derived State (read-mostly)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** The read-mostly half of docket v0 per `docs/concepts/03`: contract files load, the Accord (A1–A9) admits/refuses/flags, state derives at runtime, and `import`/`check`/`status`/`audit`/`tasks`/`file` work end-to-end. Plan 2 adds the courtroom (review/amend/sign) and the recursive fixture.

**Architecture:** Python package `docket`, file-native, no daemon, no DB. Law lives in `.contracts/*.contract.yaml`; history is append-only JSON under `.contracts/evidence/` and `.contracts/amendments/`; every state is computed from law + history at runtime — nothing persists a status. Acceptance always delegates to the repo's own tools via subprocess; docket judges exit codes and threshold extractions only.

**Tech Stack:** Python ≥3.12, uv, pydantic v2 (schema), ruamel.yaml (round-trip YAML so amendments diff cleanly), pytest. CLI is stdlib argparse — deliberately boring. No rich, no color deps; output is the plain monospace committed to in `docs/concepts/02`.

**Authority note (read first):** `docs/concepts/00`–`03` are the spec. This plan is execution material, not a second spec reality — where the concepts underdetermine a mechanic, the decision is recorded in "Design decisions" below and the concept docs win any conflict. The graduation fixtures (`docs/dojo/runs/*/.contracts/*.contract.yaml`) are ground truth: **the door must admit all 24 mdtodo clauses with zero refusals.** That is a standing regression on every door change.

---

## Design decisions beyond the concept docs

These were underdetermined by `docs/concepts/01`–`03` and are decided here (flag to Pyro/Codie at review):

1. **`command:` acceptance is judged by exit code only.** The graduation fixtures bake assertions into the shell string (`"tipsy -5 >/dev/null 2>&1; test $? -eq 2 && ..."`); `expect:` is displayed human intent, never parsed. Matches "exit codes and thresholds only" (D0-006). Commands and metric scripts run under **bash** (`subprocess.run(..., shell=True, executable="/bin/bash")`) — tipsy C-009 uses process substitution, which `/bin/sh` rejects with exit 2 (Codie review finding).
2. **`threshold:` grammar = label + comparator + number + unit, fuzzy-matched against `name: value` lines on the metric script's stdout.** "peak RSS < 64 MB on the 100 MB reference input" binds the output line whose label tokens overlap {peak, rss}. This is how two clauses share one bench script (mdtodo C-011/C-012). Unit token must match after normalization; no silent unit conversion in v0.
3. **History record kinds:** `evidence/<clause>/bundle-NNN.json` (filed claims), `evidence/<clause>/check-NNN.json` (conformance runs — `check` records results so `status` can show broken/freshness without re-running domain code), `amendments/rev-NNN.json` (law-change events incl. the founding import; concept 01 lists amendments as stored history). Verdict records are Plan 2.
4. **Evidence invalidation is derived, never performed:** a record is valid iff no amendment record with `rev > rev_at_filing` touches its clause. Nothing is deleted or rewritten (append-only).
5. **Admission flags are re-derived live**, not stored: PENDING-HARNESS clears by itself when the test file appears; OVERLAP clears when a clause is amended. The door's flag output at import is a report, not state.
6. **A4/A8 split:** A4 refuses zero RFC-2119 keywords or any SHOULD/MAY ("a hope, not an obligation" / "decide or defer"); A8 refuses >1 MUST/MUST NOT or explicit enumeration structure ("(1)…(2)…", newline-dash lists). Conservative on purpose: gestalt clauses like mdtodo C-003 (one MUST pinning a whole layout) must pass — that's the A8-by-gestalt doctrine from the review-gate inbox, implemented as restraint.
7. **A5 overlap is metric-scoped:** same test nodeid claimed by two clauses → flag both; same metric script → flag only if the two thresholds' label tokens overlap (C-011 "peak RSS" vs C-012 "wall clock" share a script and are NOT an overlap — their notes record the resolution).
8. **A3 for `command:`** scans every command-position token, not just the first: the command string is split on shell operators (`|`, `&&`, `||`, `;`, `$(`, `<(`, `(`), each segment's leading token is resolved (`shutil.which` or repo-relative), and known wrappers (`timeout`, `env`, `nice`, `nohup`, `stdbuf`) plus their numeric/option arguments are seen through. So mdtodo C-002's `timeout 30 mdtodo …` flags on the missing `mdtodo`, and tipsy C-006's `echo '42.50' | tipsy …` flags on the missing `tipsy` — missing harness must be PENDING-HARNESS at the door, never a later broken check (Codie review finding; the shallow first-token version violated A3's TDD-order rationale).
9. **`test:` runner is a template**, default `pytest -q {ref}`, overridable in optional `.contracts/runners.yaml` (`runners: {test: "uv run pytest -q {ref}"}`). Docket cannot know the repo's test tool; one mapping line is plumbing, not spec.
10. **Coverage universe is an optional, producer-agnostic manifest** `.contracts/coverage.yaml` (`cells:` + `deferred:` lists). With it, `audit` shows covered/uncovered/deferred; without it, covered cells only plus "no coverage manifest — uncovered regions unknown." Never reads `.sfd/` or any producer dir (boundary discipline).
11. **Import exit codes:** 0 = processed and ≥1 clause admitted (refusals are the door working, not an error); 2 = file unreadable/unparseable or zero admitted. Every refusal line cites its check in brackets (`[A4]`) — that's the D0-007 "refusals each cite A1–A9" hook.
12. **Unsigned contracts import with a warning** ("law without signature"); the ratifying signature is Plan 2's `docket sign`.
13. **`--root DIR` global flag** (default cwd) so tests drive throwaway ledgers; `main(argv) -> int` for in-process testing. Subprocess is reserved for acceptance delegation (D0-006), not for testing docket itself.
14. **Status TASKS column deferred.** The concept-02 mock shows `TASKS 4/4`, but v0's schema has no sub-task source to derive it from honestly. Status shows CLAUSE / EVIDENCE / STATE + the footer counts. (Deviation — surfaced for Pyro; revisit if a derivation source appears.)
15. **State precedence** (first match wins): `retired → deferred → stuck → review → broken → stale → pending-harness → overlap → holding → unstarted`. Display glyphs: ✔ holding · ⚖ review · ✘ broken · ↻ re-verdict (stale) · ⚠ stuck · ◌ pending-harness · ⚑ overlap · ○ unstarted · ⏸ deferred. `overlap` is a first-class state (concepts/02 lists "pending-harness / overlap" in the derived vocabulary), and **status always appends outstanding flags to the STATE cell** (e.g. `✔ holding ⚑OVERLAP`) so an Accord flag can never hide behind a stronger state (Codie review finding). (stuck/review/stale fully materialize in Plan 2; the engine defines them now so the enum never changes.)

## File structure

```
pyproject.toml                      # uv project, console script: docket
src/docket/__init__.py             # __version__
src/docket/model.py                # pydantic: Contract, Clause, Acceptance union, records
src/docket/storage.py              # Ledger: load/save .contracts/, append-only history IO
src/docket/accord.py               # the door: A1–A9, DoorReport
src/docket/runner.py               # subprocess delegation, threshold matching, check records
src/docket/state.py                # pure derivation: ClauseView, precedence, validity
src/docket/render.py               # ALL terminal output templates (incl. two-exit footer)
src/docket/cli.py                  # argparse wiring, exit codes, main(argv)
tests/conftest.py                  # tmp-ledger factory, run_cli helper
tests/test_model.py
tests/test_storage.py
tests/test_door.py                 # incl. test_refusals_a1_a4_a6_a7  (binds D0-001)
tests/test_import.py               # golden + bad-twin fixtures (feeds D0-007)
tests/test_exec.py                 # incl. test_delegation_only       (binds D0-006)
tests/test_state.py                # incl. test_no_stored_state       (binds D0-002)
tests/test_check.py
tests/test_status.py
tests/test_audit.py
tests/test_tasks_file.py
fixtures/sfd-variant-run.contract.yaml   # verbatim copy of the mdtodo graduation contract
fixtures/bad-door.contract.yaml          # one clause per refusal/flag, exercises A1–A9
```

`.contracts/` of the docket repo itself stays empty until Plan 2 (recursive fixture).

---

### Task 1: Project scaffold

**Files:**
- Create: `pyproject.toml`, `src/docket/__init__.py`, `src/docket/cli.py`, `tests/test_model.py` (smoke only)

- [ ] **Step 1: Scaffold with uv (never raw pip/python)**

```bash
cd /home/pyro/projects/agents/docket
uv init --package --name docket --python 3.12 .
uv add pydantic ruamel.yaml
uv add --dev pytest
```

If `uv init` balks at the non-empty dir, create `pyproject.toml` by hand:

```toml
[project]
name = "docket"
version = "0.1.0"
description = "The repo's courtroom: contracts, evidence, verdicts. File-native, deliberately boring."
requires-python = ">=3.12"
dependencies = ["pydantic>=2.7", "ruamel.yaml>=0.18"]

[project.scripts]
docket = "docket.cli:entry"

[dependency-groups]
dev = ["pytest>=8.0"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/docket"]
```

- [ ] **Step 2: Minimal package + CLI entry**

`src/docket/__init__.py`:
```python
__version__ = "0.1.0"
```

`src/docket/cli.py`:
```python
import sys


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ["--version"]:
        from docket import __version__
        print(f"docket {__version__}")
        return 0
    print("docket: no command given (try: docket status)", file=sys.stderr)
    return 2


def entry() -> None:  # console-script shim
    raise SystemExit(main())
```

- [ ] **Step 3: Smoke test**

`tests/test_model.py`:
```python
from docket.cli import main


def test_version(capsys):
    assert main(["--version"]) == 0
    assert capsys.readouterr().out.startswith("docket ")
```

Run: `uv run pytest -q` — Expected: `1 passed`.

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml uv.lock src/ tests/
git commit -m "v0 scaffold: uv package, docket console script"
```

---

### Task 2: Schema models (`model.py`)

The pydantic layer. Must load both graduation fixtures unmodified — they are the schema's ground truth alongside `docs/concepts/01`.

**Files:**
- Create: `src/docket/model.py`
- Test: `tests/test_model.py` (extend)

- [ ] **Step 1: Write failing tests**

Append to `tests/test_model.py`:
```python
from pathlib import Path

import pytest
from pydantic import ValidationError

from docket.model import Clause, Contract, load_contract_file

REPO = Path(__file__).resolve().parents[1]
MDTODO = REPO / "docs/dojo/runs/graduation-mdtodo/mdtodo/.contracts/mdtodo.contract.yaml"
TIPSY = REPO / "docs/dojo/runs/pressure-tipsy/tipsy/.contracts/tipsy.contract.yaml"


def test_graduation_fixtures_load():
    for path, name, n in [(MDTODO, "mdtodo", 24), (TIPSY, "tipsy", 16)]:
        c = load_contract_file(path)
        assert isinstance(c, Contract)
        assert c.contract == name
        assert len(c.clauses) == n
        assert c.signed[0].rev == 1


def test_acceptance_union_discriminates():
    c = load_contract_file(MDTODO)
    kinds = {cl.id: cl.acceptance.kind for cl in c.clauses}
    assert kinds["C-001"] == "test"
    assert kinds["C-011"] == "metric"
    assert kinds["C-002"] == "command"
    assert kinds["C-020"] == "human"


def test_clause_id_pattern_allows_split_suffix():
    Clause.model_validate({
        "id": "C-005a",
        "obligation": "X MUST hold.",
        "acceptance": {"test": "tests/test_x.py::test_x"},
        "anchors": [{"decision": "D-001"}],
    })
    with pytest.raises(ValidationError):
        Clause.model_validate({
            "id": "c5", "obligation": "X MUST hold.",
            "acceptance": {"test": "t.py::t"}, "anchors": [{"decision": "D-001"}],
        })


def test_unknown_anchor_type_rejected():
    with pytest.raises(ValidationError):
        Clause.model_validate({
            "id": "C-001", "obligation": "X MUST hold.",
            "acceptance": {"test": "t.py::t"}, "anchors": [{"vibe": "good"}],
        })
```

Run: `uv run pytest tests/test_model.py -q` — Expected: FAIL (`ImportError: cannot import name 'Clause'`).

- [ ] **Step 2: Implement `src/docket/model.py`**

```python
"""Schema per docs/concepts/01 — the graduation fixtures are ground truth."""
from __future__ import annotations

import datetime as _dt
from pathlib import Path
from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from ruamel.yaml import YAML

ANCHOR_TYPES = ("surface", "decision", "incident", "regulation", "sla", "compat")
QUALITATIVE_WORDS = frozenset({
    "fast", "quick", "quickly", "slow", "reliable", "reliably", "scalable",
    "performant", "efficient", "efficiently", "responsive", "instant",
    "instantly", "lightweight", "snappy", "robust",
})

_yaml = YAML(typ="rt")  # round-trip: amendments must diff cleanly
_yaml.preserve_quotes = True


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class AcceptanceTest(_Strict):
    test: str
    @property
    def kind(self) -> str: return "test"
    @property
    def target(self) -> str: return self.test.split("::", 1)[0]


class AcceptanceMetric(_Strict):
    metric: str
    threshold: str
    @property
    def kind(self) -> str: return "metric"
    @property
    def target(self) -> str: return self.metric.split()[0]


class AcceptanceCommand(_Strict):
    command: str
    expect: str
    @property
    def kind(self) -> str: return "command"
    @property
    def target(self) -> str: return self.command.split()[0]


class AcceptanceHuman(_Strict):
    verdict: Literal["human"]
    @property
    def kind(self) -> str: return "human"
    @property
    def target(self) -> str: return ""


Acceptance = Union[AcceptanceTest, AcceptanceMetric, AcceptanceCommand, AcceptanceHuman]


class Anchor(_Strict):
    """Exactly one key, of a known type (unknown type / wrong arity = A7 schema error)."""
    surface: Optional[str] = None
    decision: Optional[str] = None
    incident: Optional[str] = None
    regulation: Optional[str] = None
    sla: Optional[str] = None
    compat: Optional[str] = None

    @property
    def typ(self) -> str:
        for t in ANCHOR_TYPES:
            if getattr(self, t) is not None:
                return t
        raise ValueError("empty anchor")

    @property
    def value(self) -> str:
        return getattr(self, self.typ)

    @field_validator("*", mode="after")
    @classmethod
    def _nonempty(cls, v):
        if v == "":
            raise ValueError("anchor value must be non-empty")
        return v

    @model_validator(mode="after")
    def _exactly_one(self):
        n = sum(getattr(self, t) is not None for t in ANCHOR_TYPES)
        if n != 1:
            raise ValueError(f"anchor must carry exactly one typed key, got {n}")
        return self


class Scope(_Strict):
    applies_to: list[str] = Field(default_factory=list)
    excludes: list[str] = Field(default_factory=list)


class Clause(_Strict):
    id: Annotated[str, Field(pattern=r"^[A-Z][A-Z0-9]*-\d+[a-z]?$")]
    obligation: str
    acceptance: Acceptance
    anchors: list[Anchor] = Field(default_factory=list)  # empty = A2's job, not schema's
    status: Literal["active", "deferred", "retired"] = "active"
    risk: Optional[Literal["low", "medium", "high"]] = None
    evidence_required: Optional[list[str]] = None
    scope: Optional[Scope] = None
    notes: Optional[str] = None


class SignEntry(_Strict):
    rev: int
    by: str
    date: str

    @field_validator("date", mode="before")
    @classmethod
    def _date_str(cls, v):  # YAML parses bare 2026-06-12 as datetime.date
        return v.isoformat() if isinstance(v, _dt.date) else str(v)


class Contract(_Strict):
    contract: str
    rev: int
    source: str
    signed: list[SignEntry] = Field(default_factory=list)
    clauses: list[Clause] = Field(default_factory=list)


def load_contract_data(path: Path) -> dict:
    """Raw mapping — the door needs pre-validation access for A1-vs-A7 routing."""
    with open(path) as f:
        data = _yaml.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: not a YAML mapping")
    return data


def load_contract_file(path: Path) -> Contract:
    return Contract.model_validate(load_contract_data(path))


def dump_contract(contract_data: dict, path: Path) -> None:
    """Round-trip dump of the (possibly ruamel-typed) mapping."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        _yaml.dump(contract_data, f)
```

- [ ] **Step 3: Run tests**

Run: `uv run pytest tests/test_model.py -q` — Expected: all PASS. If a fixture fails validation, the model is wrong, not the fixture — fix the model.

- [ ] **Step 4: Commit**

```bash
git add src/docket/model.py tests/test_model.py
git commit -m "schema models: contract/clause/acceptance per concepts/01, graduation fixtures as ground truth"
```

---

### Task 3: Storage (`storage.py`)

**Files:**
- Create: `src/docket/storage.py`
- Test: `tests/test_storage.py`, `tests/conftest.py`

- [ ] **Step 1: conftest helpers**

`tests/conftest.py`:
```python
import json
from pathlib import Path

import pytest

MINIMAL = """\
contract: demo
rev: 1
source: test fixture
signed:
  - {rev: 1, by: pyro, date: 2026-06-12}
clauses:
  - id: C-001
    obligation: >
      demo MUST exit 0 on success.
    acceptance:
      test: tests/test_demo.py::test_exit_zero
    anchors:
      - decision: D-001
"""


@pytest.fixture
def ledger_root(tmp_path: Path) -> Path:
    (tmp_path / ".contracts").mkdir()
    (tmp_path / ".contracts" / "demo.contract.yaml").write_text(MINIMAL)
    return tmp_path


def run_cli(argv: list[str], root: Path, capsys) -> tuple[int, str, str]:
    from docket.cli import main
    code = main(["--root", str(root), *argv])
    cap = capsys.readouterr()
    return code, cap.out, cap.err


def write_history(root: Path, clause: str, name: str, payload: dict) -> Path:
    d = root / ".contracts" / "evidence" / clause
    d.mkdir(parents=True, exist_ok=True)
    p = d / name
    p.write_text(json.dumps(payload))
    return p
```

- [ ] **Step 2: Failing tests**

`tests/test_storage.py`:
```python
from docket.storage import Ledger


def test_discovers_contracts(ledger_root):
    led = Ledger(ledger_root)
    assert [c.contract for c in led.contracts()] == ["demo"]


def test_append_only_numbering(ledger_root):
    led = Ledger(ledger_root)
    p1 = led.append_record("C-001", "bundle", {"clause": "C-001", "claim": "satisfied",
                                               "filed_by": "t", "rev_at_filing": 1, "evidence": []})
    p2 = led.append_record("C-001", "bundle", {"clause": "C-001", "claim": "satisfied",
                                               "filed_by": "t", "rev_at_filing": 1, "evidence": []})
    assert p1.name == "bundle-001.json" and p2.name == "bundle-002.json"
    assert len(led.records("C-001", "bundle")) == 2


def test_amendment_records(ledger_root):
    led = Ledger(ledger_root)
    led.append_amendment("demo", {"rev": 1, "by": "pyro", "kind": "import",
                                  "changes": [{"id": "C-001", "change": "added"}]})
    assert led.amendments("demo")[0]["kind"] == "import"
    assert led.last_amend_rev("demo", "C-001") == 1
    assert led.last_amend_rev("demo", "C-999") == 0
```

Run: `uv run pytest tests/test_storage.py -q` — Expected: FAIL (no `docket.storage`).

- [ ] **Step 3: Implement `src/docket/storage.py`**

```python
"""File-native ledger IO. Law = .contracts/*.contract.yaml; history = append-only JSON.

Layout (concepts/01 + design decision 3):
  .contracts/<name>.contract.yaml
  .contracts/evidence/<CLAUSE>/{bundle,check,verdict}-NNN.json
  .contracts/amendments/<name>/rev-NNN-seq-NNN.json
  .contracts/drafts/<name>.rev<N>.yaml          (Plan 2)
  .contracts/runners.yaml                        (optional)
  .contracts/coverage.yaml                       (optional)
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

from ruamel.yaml import YAML

from docket.model import Contract, load_contract_data, load_contract_file

_yaml = YAML(typ="safe")


def now_iso() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


class Ledger:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.dir = self.root / ".contracts"

    # -- law ---------------------------------------------------------------
    def contract_paths(self) -> list[Path]:
        return sorted(self.dir.glob("*.contract.yaml"))

    def contracts(self) -> list[Contract]:
        return [load_contract_file(p) for p in self.contract_paths()]

    def contract(self, name: str) -> Contract:
        return load_contract_file(self.contract_path(name))

    def contract_path(self, name: str) -> Path:
        return self.dir / f"{name}.contract.yaml"

    def contract_data(self, name: str) -> dict:
        return load_contract_data(self.contract_path(name))

    # -- per-clause history (append-only) -----------------------------------
    def _clause_dir(self, clause_id: str) -> Path:
        return self.dir / "evidence" / clause_id

    def records(self, clause_id: str, kind: str) -> list[dict]:
        d = self._clause_dir(clause_id)
        out = []
        for p in sorted(d.glob(f"{kind}-*.json")):
            rec = json.loads(p.read_text())
            rec["_file"] = p.name
            out.append(rec)
        return out

    def append_record(self, clause_id: str, kind: str, payload: dict) -> Path:
        d = self._clause_dir(clause_id)
        d.mkdir(parents=True, exist_ok=True)
        n = len(list(d.glob(f"{kind}-*.json"))) + 1
        p = d / f"{kind}-{n:03d}.json"
        payload.setdefault("at", now_iso())
        p.write_text(json.dumps(payload, indent=2) + "\n")
        return p

    # -- amendment history ---------------------------------------------------
    def _amend_dir(self, contract: str) -> Path:
        return self.dir / "amendments" / contract

    def amendments(self, contract: str) -> list[dict]:
        d = self._amend_dir(contract)
        return [json.loads(p.read_text()) for p in sorted(d.glob("rev-*.json"))]

    def append_amendment(self, contract: str, payload: dict) -> Path:
        d = self._amend_dir(contract)
        d.mkdir(parents=True, exist_ok=True)
        seq = len(list(d.glob("rev-*.json"))) + 1
        payload.setdefault("at", now_iso())
        p = d / f"rev-{payload['rev']:03d}-seq-{seq:03d}.json"
        p.write_text(json.dumps(payload, indent=2) + "\n")
        return p

    def last_amend_rev(self, contract: str, clause_id: str) -> int:
        revs = [a["rev"] for a in self.amendments(contract)
                if any(ch["id"] == clause_id for ch in a.get("changes", []))]
        return max(revs, default=0)

    # -- optional config -------------------------------------------------------
    def runner_template(self, kind: str) -> str:
        defaults = {"test": "pytest -q {ref}"}
        p = self.dir / "runners.yaml"
        if p.exists():
            data = _yaml.load(p.read_text()) or {}
            return (data.get("runners") or {}).get(kind, defaults[kind])
        return defaults[kind]

    def coverage_manifest(self) -> dict | None:
        p = self.dir / "coverage.yaml"
        if not p.exists():
            return None
        data = _yaml.load(p.read_text()) or {}
        return {"cells": list(data.get("cells") or []),
                "deferred": list(data.get("deferred") or [])}
```

- [ ] **Step 4: Run & commit**

Run: `uv run pytest tests/test_storage.py tests/test_model.py -q` — Expected: PASS.

```bash
git add src/docket/storage.py tests/test_storage.py tests/conftest.py
git commit -m "storage: ledger discovery, append-only history, amendment records"
```

---

### Task 4: The Accord — refusal checks A1, A2, A4, A7 (`accord.py`)

**Files:**
- Create: `src/docket/accord.py`
- Test: `tests/test_door.py`

- [ ] **Step 1: Failing tests**

`tests/test_door.py`:
```python
from pathlib import Path

from docket.accord import run_door

REPO = Path(__file__).resolve().parents[1]


def clause(**over):
    base = {
        "id": "C-001",
        "obligation": "The tool MUST exit 0 on success.",
        "acceptance": {"test": "tests/test_x.py::test_x"},
        "anchors": [{"decision": "D-001"}],
    }
    base.update(over)
    return base


def contract(*clauses):
    return {"contract": "t", "rev": 1, "source": "test", "signed": [],
            "clauses": list(clauses)}


def door(data, root=None, **kw):
    return run_door(data, root or REPO, **kw)


def refusal_checks(report):
    return {(f.clause_id, f.check) for f in report.refusals}


def test_a1_missing_acceptance_refused():
    rep = door(contract({k: v for k, v in clause().items() if k != "acceptance"}))
    assert ("C-001", "A1") in refusal_checks(rep)
    assert "how would I check this" in rep.refusals[0].message


def test_a1_unknown_acceptance_type_refused():
    rep = door(contract(clause(acceptance={"vibes": "good"})))
    assert ("C-001", "A1") in refusal_checks(rep)


def test_a2_anchorless_refused_and_overridable():
    rep = door(contract(clause(anchors=[])))
    assert ("C-001", "A2") in refusal_checks(rep)
    rep2 = door(contract(clause(anchors=[])), sign_unanchored="pyro")
    assert rep2.refusals == [] and len(rep2.admitted) == 1
    assert rep2.overrides == [{"id": "C-001", "check": "A2", "signed_by": "pyro"}]


def test_a4_should_refused_decide_or_defer():
    rep = door(contract(clause(obligation="The tool SHOULD be nice to users.")))
    assert ("C-001", "A4") in refusal_checks(rep)


def test_a4_no_keyword_refused():
    rep = door(contract(clause(obligation="The tool exits 0 on success.")))
    assert ("C-001", "A4") in refusal_checks(rep)
    assert "a hope, not an obligation" in rep.refusals[0].message


def test_a4_must_not_counts_once():
    rep = door(contract(clause(obligation="The tool MUST NOT read stdin.")))
    assert rep.refusals == []


def test_a7_duplicate_ids_refused():
    rep = door(contract(clause(), clause()))
    assert ("C-001", "A7") in refusal_checks(rep)


def test_a7_schema_error_refused():
    rep = door(contract(clause(anchors=[{"vibe": "good"}])))
    assert ("C-001", "A7") in refusal_checks(rep)


def test_refusals_a1_a4_a6_a7():
    """D0-001: door refuses missing acceptance and missing/multiple MUST."""
    rep = door(contract(
        {k: v for k, v in clause(id="C-001").items() if k != "acceptance"},
        clause(id="C-002", obligation="The tool exits zero."),
        clause(id="C-003", obligation="The tool MUST be fast."),
        clause(id="C-004"), clause(id="C-004"),
    ))
    assert {("C-001", "A1"), ("C-002", "A4"), ("C-003", "A6"),
            ("C-004", "A7")} <= refusal_checks(rep)
```

Run: `uv run pytest tests/test_door.py -q` — Expected: FAIL (no `docket.accord`). The A6 case in the last test stays red until Task 5 — that's fine; note it and don't chase it in this task.

- [ ] **Step 2: Implement `src/docket/accord.py` (A1/A2/A4/A7 + report shell)**

```python
"""The Accord — door policy A1–A9 per docs/concepts/01.

Two outcome classes: refuse (clause does not enter) and flag (clause enters
carrying an obligation to resolve). Flags are re-derived live by state.py;
the door's output is the import-time report.
"""
from __future__ import annotations

import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path

from pydantic import ValidationError

from docket.model import QUALITATIVE_WORDS, Clause

MESSAGES = {
    "A1": "no acceptance procedure — how would I check this?",
    "A2": "where did this come from?",
    "A3": "clause is law; it cannot go green until the harness exists",
    "A4": "a hope, not an obligation",
    "A4-should": "decide or defer",
    "A5": "resolve before first verdict",
    "A6": "give me a number, a test, or defer the clause",
    "A8": "two laws in one clause — split them",
    "A9": "a high-risk invariant deserves more than one kind of evidence",
}


@dataclass
class Finding:
    check: str
    clause_id: str | None
    outcome: str            # "refuse" | "flag"
    message: str
    flag: str | None = None  # PENDING-HARNESS | OVERLAP | THIN-EVIDENCE


@dataclass
class DoorReport:
    admitted: list[Clause] = field(default_factory=list)
    refusals: list[Finding] = field(default_factory=list)
    flags: list[Finding] = field(default_factory=list)
    overrides: list[dict] = field(default_factory=list)
    file_error: str | None = None


_MUST_NOT = re.compile(r"\bMUST NOT\b")
_MUST = re.compile(r"\bMUST\b(?! NOT)")
_HOPE = re.compile(r"\bSHOULD\b|\bMAY\b")
_ENUM = re.compile(r"\(\s*\d+\s*\)\s|\n\s*[-*]\s")


def _rfc2119_count(obligation: str) -> int:
    return len(_MUST_NOT.findall(obligation)) + len(_MUST.findall(obligation))


def _check_a4(c: dict) -> Finding | None:
    ob = str(c.get("obligation", ""))
    if _HOPE.search(ob):
        return Finding("A4", c.get("id"), "refuse", MESSAGES["A4-should"])
    if _rfc2119_count(ob) == 0:
        return Finding("A4", c.get("id"), "refuse", MESSAGES["A4"])
    return None


def _check_a8(c: dict) -> Finding | None:
    ob = str(c.get("obligation", ""))
    if _rfc2119_count(ob) > 1 or _ENUM.search(ob):
        return Finding("A8", c.get("id"), "refuse", MESSAGES["A8"])
    return None


def _check_a6(c: dict, parsed: Clause | None) -> Finding | None:
    ob = str(c.get("obligation", "")).lower()
    words = set(re.findall(r"[a-z]+", ob))
    if not (words & QUALITATIVE_WORDS):
        return None
    if re.search(r"\d", str(c.get("obligation", ""))):
        return None
    if parsed is not None and parsed.acceptance.kind == "metric":
        return None  # the number lives in the threshold
    return Finding("A6", c.get("id"), "refuse", MESSAGES["A6"])


def run_door(data: dict, root: Path, sign_unanchored: str | None = None) -> DoorReport:
    rep = DoorReport()
    clauses = data.get("clauses") or []
    seen_ids: dict[str, int] = {}
    for c in clauses:
        cid = c.get("id") if isinstance(c, dict) else None
        seen_ids[cid] = seen_ids.get(cid, 0) + 1

    parsed_ok: list[tuple[dict, Clause]] = []
    for raw in clauses:
        if not isinstance(raw, dict):
            rep.refusals.append(Finding("A7", None, "refuse", f"clause is not a mapping: {raw!r}"))
            continue
        cid = raw.get("id")
        # A7: duplicate ids
        if cid is not None and seen_ids.get(cid, 0) > 1:
            rep.refusals.append(Finding("A7", cid, "refuse", f"duplicate clause id {cid}"))
            continue
        # A1: acceptance presence/shape (routed before generic A7)
        if "acceptance" not in raw:
            rep.refusals.append(Finding("A1", cid, "refuse", MESSAGES["A1"]))
            continue
        try:
            parsed = Clause.model_validate(raw)
        except ValidationError as e:
            locs = {err["loc"][0] for err in e.errors() if err["loc"]}
            if "acceptance" in locs:
                rep.refusals.append(Finding("A1", cid, "refuse", MESSAGES["A1"]))
            else:
                rep.refusals.append(Finding("A7", cid, "refuse",
                                            f"schema: {e.errors()[0]['msg']}"))
            continue
        # A4 / A8 / A6
        if (f := _check_a4(raw)):
            rep.refusals.append(f); continue
        if (f := _check_a8(raw)):
            rep.refusals.append(f); continue
        if (f := _check_a6(raw, parsed)):
            rep.refusals.append(f); continue
        # A2: anchors
        if not parsed.anchors:
            if sign_unanchored:
                rep.overrides.append({"id": parsed.id, "check": "A2",
                                      "signed_by": sign_unanchored})
            else:
                rep.refusals.append(Finding("A2", parsed.id, "refuse", MESSAGES["A2"]))
                continue
        parsed_ok.append((raw, parsed))

    for raw, parsed in parsed_ok:
        rep.admitted.append(parsed)
        rep.flags.extend(flag_checks(parsed, [p for _, p in parsed_ok], root))
    return rep


def flag_checks(clause: Clause, cohort: list[Clause], root: Path) -> list[Finding]:
    """A3, A5, A9 — also reused live by state.py (design decision 5)."""
    out: list[Finding] = []
    acc = clause.acceptance
    # A3: acceptance target exists
    if acc.kind in ("test", "metric"):
        if not (Path(root) / acc.target).exists():
            out.append(Finding("A3", clause.id, "flag",
                               f"{acc.target} missing — {MESSAGES['A3']}",
                               flag="PENDING-HARNESS"))
    elif acc.kind == "command":
        from docket.runner import command_harness_missing  # lazy: avoids cycle
        if (tok := command_harness_missing(acc.command, Path(root))):
            out.append(Finding("A3", clause.id, "flag",
                               f"{tok} not resolvable — {MESSAGES['A3']}",
                               flag="PENDING-HARNESS"))
    # A5: overlap (metric-scoped, design decision 7)
    for other in cohort:
        if other.id == clause.id or other.acceptance.kind != acc.kind:
            continue
        if acc.kind == "test" and other.acceptance.test == acc.test:
            out.append(Finding("A5", clause.id, "flag",
                               f"shares {acc.test} with {other.id} — {MESSAGES['A5']}",
                               flag="OVERLAP"))
        elif acc.kind == "metric" and other.acceptance.metric == acc.metric:
            from docket.runner import threshold_label_tokens
            if threshold_label_tokens(acc.threshold) & threshold_label_tokens(other.acceptance.threshold):
                out.append(Finding("A5", clause.id, "flag",
                                   f"shares {acc.metric} with {other.id} and thresholds collide — {MESSAGES['A5']}",
                                   flag="OVERLAP"))
        elif acc.kind == "command" and other.acceptance.command == acc.command \
                and other.acceptance.expect != acc.expect:
            out.append(Finding("A5", clause.id, "flag",
                               f"same command as {other.id}, different expectation — {MESSAGES['A5']}",
                               flag="OVERLAP"))
    # A9: risk/evidence match
    if clause.risk == "high" and len(clause.evidence_required or []) < 2:
        out.append(Finding("A9", clause.id, "flag", MESSAGES["A9"], flag="THIN-EVIDENCE"))
    return out
```

Note: `flag_checks` imports `threshold_label_tokens` lazily from `runner.py` (Task 6). Until then, add a temporary stub at the bottom of `accord.py` and delete it in Task 6:

```python
def _tmp_threshold_label_tokens(t: str) -> set[str]:  # removed in Task 6
    import re as _re
    return set(_re.findall(r"[a-z]+", t.split("<")[0].split(">")[0].lower()))
```

…and use it directly in the A5 metric branch until `runner.py` lands. Keep the lazy-import line commented with `# Task 6 swaps this in`.

- [ ] **Step 3: Run**

Run: `uv run pytest tests/test_door.py -q` — Expected: everything passes except the A6 assertion inside `test_refusals_a1_a4_a6_a7` (A6 implemented above, so actually: all PASS). If A6 false-positives on any mdtodo obligation later, the golden-import test in Task 5 catches it.

- [ ] **Step 4: Commit**

```bash
git add src/docket/accord.py tests/test_door.py
git commit -m "the Accord: refusal checks A1/A2/A4/A6/A7/A8, flag checks A3/A5/A9"
```

---

### Task 5: Door fixtures — golden + bad twin, `import`/`add` CLI

**Files:**
- Create: `fixtures/sfd-variant-run.contract.yaml`, `fixtures/bad-door.contract.yaml`
- Create: `src/docket/render.py` (import report section), extend `src/docket/cli.py`
- Test: `tests/test_import.py`

- [ ] **Step 1: Copy the golden fixture (verbatim, including its known provenance quirk)**

```bash
mkdir -p fixtures
cp docs/dojo/runs/graduation-mdtodo/mdtodo/.contracts/mdtodo.contract.yaml \
   fixtures/sfd-variant-run.contract.yaml
```

- [ ] **Step 2: Author the bad twin**

`fixtures/bad-door.contract.yaml`:
```yaml
contract: bad-door
rev: 1
source: hand-authored door-exercise fixture (one clause per Accord outcome)
signed: []

clauses:
  - id: B-001                      # A1 refuse: no acceptance
    obligation: >
      The tool MUST exit 0 on success.
    anchors:
      - decision: D-001

  - id: B-002                      # A2 refuse: no anchors
    obligation: >
      The tool MUST exit 0 on success.
    acceptance:
      test: tests/test_b.py::test_b002

  - id: B-003                      # A4 refuse: SHOULD
    obligation: >
      The tool SHOULD respond to users politely.
    acceptance:
      test: tests/test_b.py::test_b003
    anchors:
      - decision: D-002

  - id: B-004                      # A6 refuse: qualitative, unnumbered
    obligation: >
      Startup MUST be fast.
    acceptance:
      test: tests/test_b.py::test_b004
    anchors:
      - decision: D-003

  - id: B-005                      # A7 refuse: duplicate id (pair below)
    obligation: >
      The tool MUST write logs to stderr.
    acceptance:
      test: tests/test_b.py::test_b005
    anchors:
      - decision: D-004

  - id: B-005
    obligation: >
      The tool MUST write logs to stdout.
    acceptance:
      test: tests/test_b.py::test_b005x
    anchors:
      - decision: D-004

  - id: B-006                      # A8 refuse: two laws in one clause
    obligation: >
      The tool MUST validate input and MUST write a report file.
    acceptance:
      test: tests/test_b.py::test_b006
    anchors:
      - decision: D-005

  - id: B-007                      # A9 flag: high risk, thin evidence
    obligation: >
      Replays MUST be idempotent.
    acceptance:
      test: tests/test_b.py::test_b007
    anchors:
      - incident: postmortem-001
    risk: high
    evidence_required: [test]

  - id: B-008                      # A3 flag: harness missing
    obligation: >
      The tool MUST reject empty input files.
    acceptance:
      test: tests/test_missing.py::test_b008
    anchors:
      - decision: D-006

  - id: B-009                      # A5 flag pair: same nodeid, both flagged
    obligation: >
      Output MUST be sorted ascending.
    acceptance:
      test: tests/test_b.py::test_shared
    anchors:
      - decision: D-007

  - id: B-010
    obligation: >
      Output MUST NOT contain duplicates.
    acceptance:
      test: tests/test_b.py::test_shared
    anchors:
      - decision: D-007

  - id: B-011                      # clean — admits with no findings
    obligation: >
      The tool MUST exit 2 on invalid invocation.
    acceptance:
      command: "true"
      expect: "exit 0 placeholder for door-fixture purposes"
    anchors:
      - decision: D-008
```

- [ ] **Step 3: Failing tests**

`tests/test_import.py`:
```python
import re
from pathlib import Path

from tests.conftest import run_cli

REPO = Path(__file__).resolve().parents[1]
GOLDEN = REPO / "fixtures/sfd-variant-run.contract.yaml"
BAD = REPO / "fixtures/bad-door.contract.yaml"


def test_sfd_bundle_imports_clean(tmp_path, capsys):
    """D0-007's substance: variant output imports with zero manual reformatting."""
    (tmp_path / ".contracts").mkdir()
    code, out, err = run_cli(["import", str(GOLDEN)], tmp_path, capsys)
    assert code == 0
    assert "admitted: 24" in out
    assert "refused: 0" in out
    assert (tmp_path / ".contracts" / "mdtodo.contract.yaml").exists()
    # every flag line cites its check
    for line in out.splitlines():
        if line.strip().startswith(("◌", "⚑")):
            assert re.search(r"\[A[1-9]\]", line), line
    # C-011/C-012 share a bench script but bind different metrics: NOT an overlap
    assert "OVERLAP" not in out


def test_refusals_cite_door_checks(tmp_path, capsys):
    (tmp_path / ".contracts").mkdir()
    code, out, err = run_cli(["import", str(BAD)], tmp_path, capsys)
    assert code == 0  # ≥1 admitted → processed (design decision 11)
    for cid, check in [("B-001", "A1"), ("B-002", "A2"), ("B-003", "A4"),
                       ("B-004", "A6"), ("B-005", "A7"), ("B-006", "A8")]:
        assert re.search(rf"✘ {cid} \[{check}\]", out), f"{cid} missing [{check}]"
    assert re.search(r"⚑ B-007 \[A9\] THIN-EVIDENCE", out)
    assert re.search(r"◌ B-008 \[A3\] PENDING-HARNESS", out)
    assert re.search(r"⚑ B-009 \[A5\] OVERLAP", out)
    assert "admitted: 5" in out


def test_import_unanchored_override_recorded(tmp_path, capsys):
    (tmp_path / ".contracts").mkdir()
    code, out, err = run_cli(["import", str(BAD), "--sign-unanchored", "pyro"],
                             tmp_path, capsys)
    assert code == 0
    assert "admitted: 6" in out          # B-002 now enters
    import json
    amend = sorted((tmp_path / ".contracts/amendments/bad-door").glob("*.json"))[0]
    rec = json.loads(amend.read_text())
    assert {"id": "B-002", "check": "A2", "signed_by": "pyro"} in rec["overrides"]


def test_import_empty_file_noop_warning(tmp_path, capsys):
    (tmp_path / ".contracts").mkdir()
    empty = tmp_path / "empty.contract.yaml"
    empty.write_text("contract: hollow\nrev: 1\nsource: nothing\nsigned: []\nclauses: []\n")
    code, out, err = run_cli(["import", str(empty)], tmp_path, capsys)
    assert code == 2
    assert "no clauses" in err.lower()
    assert not (tmp_path / ".contracts" / "hollow.contract.yaml").exists()


def test_import_duplicate_contract_refused(ledger_root, capsys):
    src = ledger_root / ".contracts" / "demo.contract.yaml"
    code, out, err = run_cli(["import", str(src)], ledger_root, capsys)
    assert code == 2
    assert "already exists" in err
```

Run: `uv run pytest tests/test_import.py -q` — Expected: FAIL (no `import` command).

- [ ] **Step 4: Implement render + CLI import**

`src/docket/render.py` (start the module — every surface template lives here and only here):
```python
"""All terminal output. Templates are behavioral commitments from concepts/02.

The red-state footer is the D0-004 invariant: every red state prints at
least one work-exit and one law-exit.
"""
from __future__ import annotations

from docket.accord import DoorReport

GLYPH = {"holding": "✔", "review": "⚖", "broken": "✘", "stale": "↻",
         "stuck": "⚠", "pending-harness": "◌", "overlap": "⚑",
         "unstarted": "○", "deferred": "⏸", "retired": "·"}

TWO_EXITS = ("  → fix the code or amend the contract. The docket does not care\n"
             "    which, but it will not go green by argument.")


def import_report(name: str, rev: int, source: str, signed: list,
                  rep: DoorReport, dest: str) -> str:
    lines = [f"DOCKET IMPORT — {name} rev {rev}", f"source: {source}"]
    if signed:
        s = signed[-1]
        lines.append(f"signed: rev {s.rev} by {s.by} ({s.date})")
    else:
        lines.append("signed: NONE — law without signature (sign with: docket sign)")
    lines.append(f"admitted: {len(rep.admitted)}")
    lines.append(f"refused: {len(rep.refusals)}")
    for f in rep.refusals:
        lines.append(f"  ✘ {f.clause_id} [{f.check}] {f.message}")
    if rep.flags:
        lines.append(f"flags: {len(rep.flags)}")
        for f in rep.flags:
            glyph = "◌" if f.flag == "PENDING-HARNESS" else "⚑"
            lines.append(f"  {glyph} {f.clause_id} [{f.check}] {f.flag} — {f.message}")
    for o in rep.overrides:
        lines.append(f"  ✍ {o['id']} [A2] admitted unanchored — signed by {o['signed_by']}")
    lines.append(f"→ {dest}")
    return "\n".join(lines)
```

Rewrite `src/docket/cli.py`:
```python
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from docket import __version__


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="docket")
    p.add_argument("--version", action="version", version=f"docket {__version__}")
    p.add_argument("--root", type=Path, default=Path.cwd(),
                   help="repo root containing .contracts/ (default: cwd)")
    sub = p.add_subparsers(dest="cmd")

    imp = sub.add_parser("import", help="admit a contract file through the Accord")
    imp.add_argument("file", type=Path)
    imp.add_argument("--sign-unanchored", metavar="AUTHORITY", default=None)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.cmd is None:
        print("docket: no command given (try: docket status)", file=sys.stderr)
        return 2
    return {"import": cmd_import}[args.cmd](args)


def cmd_import(args) -> int:
    from docket.accord import run_door
    from docket.model import Contract, dump_contract, load_contract_data
    from docket.render import import_report
    from docket.storage import Ledger, now_iso

    led = Ledger(args.root)
    try:
        data = load_contract_data(args.file)
    except Exception as e:
        print(f"docket import: cannot read {args.file}: {e}", file=sys.stderr)
        return 2

    name = data.get("contract")
    if not name:
        print("docket import: file has no 'contract' name", file=sys.stderr)
        return 2
    dest = led.contract_path(name)
    if dest.exists() and dest.resolve() != Path(args.file).resolve():
        print(f"docket import: {dest} already exists — amend the law, don't re-import it",
              file=sys.stderr)
        return 2

    rep = run_door(data, args.root, sign_unanchored=args.sign_unanchored)
    if not rep.admitted:
        print("docket import: no clauses admitted"
              + (" (file has no clauses)" if not data.get("clauses") else ""),
              file=sys.stderr)
        return 2

    # law: write only admitted clauses (refused clauses do not enter)
    admitted_ids = {c.id for c in rep.admitted}
    data["clauses"] = [c for c in data["clauses"]
                       if isinstance(c, dict) and c.get("id") in admitted_ids]
    dump_contract(data, dest)

    # history: the founding import is an amendment record (design decision 3)
    contract = Contract.model_validate(data)
    led.append_amendment(name, {
        "rev": contract.rev, "by": args.sign_unanchored or "import",
        "kind": "import",
        "changes": [{"id": c.id, "change": "added"} for c in rep.admitted],
        "overrides": rep.overrides,
        "refused": [{"id": f.clause_id, "check": f.check} for f in rep.refusals],
    })

    print(import_report(name, contract.rev, contract.source, contract.signed,
                        rep, str(dest.relative_to(args.root))))
    return 0


def entry() -> None:
    raise SystemExit(main())
```

(`--version` moves to argparse's native action; delete the old hand-rolled branch and update the Task 1 smoke test to expect `SystemExit`: )

```python
def test_version(capsys):
    import pytest
    with pytest.raises(SystemExit) as e:
        main(["--version"])
    assert e.value.code == 0
    assert capsys.readouterr().out.startswith("docket ")
```

- [ ] **Step 5: Run the full suite**

Run: `uv run pytest -q` — Expected: PASS, including `test_sfd_bundle_imports_clean` (24 admitted / 0 refused). If any mdtodo clause is refused, **the door is wrong** — recalibrate the offending check (most likely A6's wordlist or A8's enum regex) until the golden fixture is clean, and add the offending obligation text as a regression case in `test_door.py`.

- [ ] **Step 6: Commit**

```bash
git add fixtures/ src/docket/render.py src/docket/cli.py tests/test_import.py tests/test_model.py
git commit -m "docket import: door report with check citations, golden + bad-twin fixtures"
```

---

### Task 6: Acceptance delegation (`runner.py`)

**Files:**
- Create: `src/docket/runner.py`
- Modify: `src/docket/accord.py` (swap the threshold-token stub for the real import)
- Test: `tests/test_exec.py`

- [ ] **Step 1: Failing tests**

`tests/test_exec.py`:
```python
import json
import stat
from pathlib import Path

from docket.runner import run_acceptance, threshold_label_tokens, parse_threshold
from docket.model import AcceptanceCommand, AcceptanceMetric, AcceptanceTest, AcceptanceHuman
from docket.storage import Ledger


def _script(root: Path, name: str, body: str) -> str:
    p = root / name
    p.write_text(f"#!/bin/sh\n{body}\n")
    p.chmod(p.stat().st_mode | stat.S_IEXEC)
    return name


def test_threshold_parsing():
    assert parse_threshold("p95 < 50ms") == ("<", 50.0, "ms")
    assert parse_threshold("peak RSS < 64 MB on the 100 MB reference input") == ("<", 64.0, "mb")
    assert parse_threshold("wall clock < 5 s on the 100 MB reference input") == ("<", 5.0, "s")
    assert threshold_label_tokens("peak RSS < 64 MB ...") == {"peak", "rss"}
    assert threshold_label_tokens("wall clock < 5 s ...") == {"wall", "clock"}


def test_delegation_only(ledger_root):
    """D0-006: acceptance runs via subprocess, judged by exit code/threshold only."""
    marker = ledger_root / "ran.marker"
    name = _script(ledger_root, "ok.sh", f"touch {marker}\nexit 0")
    res = run_acceptance(AcceptanceCommand(command=f"./{name}", expect="exit 0"),
                         ledger_root, Ledger(ledger_root).runner_template)
    assert res.result == "green"
    assert marker.exists()                       # really ran, out of process
    bad = _script(ledger_root, "bad.sh", "exit 1")
    res2 = run_acceptance(AcceptanceCommand(command=f"./{bad}", expect="exit 0"),
                          ledger_root, Ledger(ledger_root).runner_template)
    assert res2.result == "red"


def test_metric_threshold_judged(ledger_root):
    name = _script(ledger_root, "bench.sh",
                   'echo "peak_rss_mb: 41.2"\necho "wall_clock_s: 3.7"')
    green = run_acceptance(
        AcceptanceMetric(metric=f"./{name}", threshold="peak RSS < 64 MB"),
        ledger_root, Ledger(ledger_root).runner_template)
    assert green.result == "green" and "41.2" in green.detail
    red = run_acceptance(
        AcceptanceMetric(metric=f"./{name}", threshold="wall clock < 2 s"),
        ledger_root, Ledger(ledger_root).runner_template)
    assert red.result == "red"
    lost = run_acceptance(
        AcceptanceMetric(metric=f"./{name}", threshold="latency < 9 ms"),
        ledger_root, Ledger(ledger_root).runner_template)
    assert lost.result == "red" and "not found" in lost.drift


def test_pending_harness_and_human(ledger_root):
    res = run_acceptance(AcceptanceTest(test="tests/nope.py::test_x"),
                         ledger_root, Ledger(ledger_root).runner_template)
    assert res.result == "pending-harness"
    res2 = run_acceptance(AcceptanceHuman(verdict="human"),
                          ledger_root, Ledger(ledger_root).runner_template)
    assert res2.result == "human"


def test_a3_command_sees_through_wrappers_and_pipes(ledger_root):
    from docket.runner import command_harness_missing
    assert command_harness_missing(
        "timeout 30 mdtodo demo/docs >/dev/null 2>&1; test $? -ne 124",
        ledger_root) == "mdtodo"
    assert command_harness_missing(
        "echo '42.50' | tipsy 2>&1; test $? -eq 2", ledger_root) == "tipsy"
    assert command_harness_missing(
        "diff <(tipsy 10) <(tipsy 10)", ledger_root) == "tipsy"
    assert command_harness_missing("true && echo ok", ledger_root) is None


def test_commands_run_under_bash(ledger_root):
    res = run_acceptance(
        AcceptanceCommand(command="diff <(echo a) <(echo a)",
                          expect="process substitution works"),
        ledger_root, Ledger(ledger_root).runner_template)
    assert res.result == "green"
```

Run: `uv run pytest tests/test_exec.py -q` — Expected: FAIL (no `docket.runner`).

- [ ] **Step 2: Implement `src/docket/runner.py`**

```python
"""Subprocess delegation — docket executes nothing domain-specific (D0-006).

Judgment surface: exit codes for test/command; threshold extraction for
metric. Threshold grammar (design decision 2):
  "<label words> <op> <number><unit> [trailing prose]"
matched against `name: value` lines on the metric script's stdout by
label-token overlap.
"""
from __future__ import annotations

import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from docket.model import Acceptance

_THRESH = re.compile(r"^(?P<label>[^<>=]*?)\s*(?P<op>[<>]=?)\s*(?P<num>\d+(?:\.\d+)?)\s*(?P<unit>[A-Za-zµ%]*)")
_OUT_LINE = re.compile(r"^(?P<name>[A-Za-z_][\w .-]*?)\s*[:=]\s*(?P<num>-?\d+(?:\.\d+)?)\s*(?P<unit>[A-Za-zµ%]*)\s*$")


@dataclass
class RunResult:
    result: str            # green | red | pending-harness | human
    detail: str = ""       # one-line summary for records/render
    drift: str = ""        # what diverged (red only)
    output_tail: str = ""  # last lines of subprocess output


def parse_threshold(threshold: str) -> tuple[str, float, str]:
    m = _THRESH.search(threshold)
    if not m:
        raise ValueError(f"unparseable threshold: {threshold!r}")
    return m.group("op"), float(m.group("num")), m.group("unit").lower()


def threshold_label_tokens(threshold: str) -> set[str]:
    m = _THRESH.search(threshold)
    label = m.group("label") if m else threshold
    return set(re.findall(r"[a-z0-9]+", label.lower())) - {"the", "a", "an", "on", "of"}


def _compare(value: float, op: str, bound: float) -> bool:
    return {"<": value < bound, "<=": value <= bound,
            ">": value > bound, ">=": value >= bound}[op]


WRAPPERS = {"timeout", "env", "nice", "nohup", "stdbuf"}
_SEGMENT_SPLIT = re.compile(r"\|\||&&|;|\||\$\(|<\(|\(")


def command_harness_missing(command: str, root: Path) -> str | None:
    """A3 for command acceptance: first command-position token that resolves
    nowhere. Scans every pipeline/subshell segment, sees through wrappers."""
    for segment in _SEGMENT_SPLIT.split(command):
        for tok in segment.strip().split():
            tok = tok.strip("'\"")
            if tok in WRAPPERS or re.fullmatch(r"[A-Z_]+=\S*", tok) \
                    or re.fullmatch(r"-{1,2}[\w-]+|\d+(?:\.\d+)?[smh]?", tok):
                continue  # wrapper, env assignment, option, or duration arg
            if not (shutil.which(tok) or (root / tok).exists()):
                return tok
            break  # segment's command resolves; rest are its arguments
    return None


def _run(cmd: str, root: Path) -> subprocess.CompletedProcess:
    # bash, not sh: graduation fixtures use process substitution (decision 1)
    return subprocess.run(cmd, shell=True, executable="/bin/bash", cwd=root,
                          capture_output=True, text=True, timeout=600)


def _tail(proc: subprocess.CompletedProcess, n: int = 12) -> str:
    return "\n".join((proc.stdout + proc.stderr).strip().splitlines()[-n:])


def run_acceptance(acc: Acceptance, root: Path,
                   runner_template: Callable[[str], str]) -> RunResult:
    if acc.kind == "human":
        return RunResult("human", "verdict: human — route to docket review")

    # A3 live: missing harness is pending, not red (TDD order)
    if acc.kind in ("test", "metric") and not (root / acc.target).exists():
        return RunResult("pending-harness", f"{acc.target} missing")
    if acc.kind == "command":
        if (tok := command_harness_missing(acc.command, root)):
            return RunResult("pending-harness", f"{tok} not resolvable")

    if acc.kind == "test":
        proc = _run(runner_template("test").format(ref=acc.test), root)
        if proc.returncode == 0:
            return RunResult("green", f"{acc.test} PASS", output_tail=_tail(proc))
        return RunResult("red", f"{acc.test} FAIL",
                         drift=_extract_failure(proc), output_tail=_tail(proc))

    if acc.kind == "command":
        proc = _run(acc.command, root)
        if proc.returncode == 0:
            return RunResult("green", f"command exit 0 — expect: {acc.expect}",
                             output_tail=_tail(proc))
        return RunResult("red", f"command exit {proc.returncode}",
                         drift=f"expected: {acc.expect}", output_tail=_tail(proc))

    # metric
    proc = _run(acc.metric, root)
    if proc.returncode != 0:
        return RunResult("red", f"{acc.metric} exit {proc.returncode}",
                         drift="metric script failed", output_tail=_tail(proc))
    op, bound, unit = parse_threshold(acc.threshold)
    want = threshold_label_tokens(acc.threshold)
    for line in proc.stdout.splitlines():
        m = _OUT_LINE.match(line.strip())
        if not m:
            continue
        have = set(re.findall(r"[a-z0-9]+", m.group("name").lower()))
        if want & have:
            value = float(m.group("num"))
            line_unit = m.group("unit").lower() or (have & {"ms", "s", "mb", "gb", "kb"})
            ok = _compare(value, op, bound)
            detail = f"{m.group('name').strip()} = {value} (threshold {op} {bound}{unit})"
            if ok:
                return RunResult("green", detail, output_tail=_tail(proc))
            return RunResult("red", detail,
                             drift=f"measured {value}, contracted {op} {bound}{unit}",
                             output_tail=_tail(proc))
    return RunResult("red", f"threshold {acc.threshold!r}",
                     drift=f"metric matching {sorted(want)} not found in output",
                     output_tail=_tail(proc))


def _extract_failure(proc: subprocess.CompletedProcess) -> str:
    """Drift naming: surface the assertion/error line, not the whole log."""
    lines = (proc.stdout + proc.stderr).splitlines()
    for pat in (r"^E\s+", r"Error", r"assert", r"FAILED"):
        hits = [l.strip() for l in lines if re.search(pat, l)]
        if hits:
            return hits[-1][:160]
    return (lines[-1].strip()[:160]) if lines else "no output"
```

Then in `accord.py`: delete `_tmp_threshold_label_tokens` and keep the lazy `from docket.runner import threshold_label_tokens` inside the A5 metric branch (lazy to avoid an import cycle).

- [ ] **Step 3: Run & commit**

Run: `uv run pytest tests/test_exec.py tests/test_door.py tests/test_import.py -q` — Expected: PASS (the A5 metric-scope behavior on mdtodo C-011/C-012 is now exercised by the golden import test: no OVERLAP).

```bash
git add src/docket/runner.py src/docket/accord.py tests/test_exec.py
git commit -m "runner: subprocess delegation, threshold grammar, drift extraction (D0-006)"
```

---

### Task 7: Derived state (`state.py`)

**Files:**
- Create: `src/docket/state.py`
- Test: `tests/test_state.py`

- [ ] **Step 1: Failing tests**

`tests/test_state.py`:
```python
import hashlib
import json
from pathlib import Path

from tests.conftest import run_cli, write_history
from docket.state import derive_views
from docket.storage import Ledger


def _views(root):
    led = Ledger(root)
    return {v.clause.id: v for v in derive_views(led.contract("demo"), led, root)}


def _bundle(rev=1, claim="satisfied"):
    return {"clause": "C-001", "claim": claim, "filed_by": "loop#1",
            "rev_at_filing": rev,
            "evidence": [{"kind": "test", "ref": "t", "result": "PASS"}]}


def test_unstarted_then_pending_harness(ledger_root):
    # acceptance target tests/test_demo.py does not exist → pending-harness
    assert _views(ledger_root)["C-001"].state == "pending-harness"
    (ledger_root / "tests").mkdir(exist_ok=True)
    (ledger_root / "tests/test_demo.py").write_text("def test_exit_zero(): pass\n")
    assert _views(ledger_root)["C-001"].state == "unstarted"


def test_review_when_bundle_unjudged(ledger_root):
    (ledger_root / "tests").mkdir(); (ledger_root / "tests/test_demo.py").write_text("x = 1\n")
    write_history(ledger_root, "C-001", "bundle-001.json", _bundle())
    assert _views(ledger_root)["C-001"].state == "review"


def test_stuck_on_failure_report(ledger_root):
    (ledger_root / "tests").mkdir(); (ledger_root / "tests/test_demo.py").write_text("x = 1\n")
    write_history(ledger_root, "C-001", "bundle-001.json",
                  _bundle(claim="stuck") | {"stuck_on": "flaky timer"})
    assert _views(ledger_root)["C-001"].state == "stuck"


def test_broken_when_check_red(ledger_root):
    (ledger_root / "tests").mkdir(); (ledger_root / "tests/test_demo.py").write_text("x = 1\n")
    write_history(ledger_root, "C-001", "check-001.json",
                  {"clause": "C-001", "rev": 1, "result": "red", "detail": "FAIL",
                   "drift": "raises RuntimeError"})
    v = _views(ledger_root)["C-001"]
    assert v.state == "broken"


def test_holding_when_accepted_and_green(ledger_root):
    (ledger_root / "tests").mkdir(); (ledger_root / "tests/test_demo.py").write_text("x = 1\n")
    write_history(ledger_root, "C-001", "bundle-001.json", _bundle())
    write_history(ledger_root, "C-001", "verdict-001.json",
                  {"bundle": "bundle-001", "clause": "C-001", "verdict": "accepted",
                   "by": "pyro", "rev": 1})
    write_history(ledger_root, "C-001", "check-001.json",
                  {"clause": "C-001", "rev": 1, "result": "green", "detail": "PASS"})
    assert _views(ledger_root)["C-001"].state == "holding"


def test_stale_after_amendment_invalidates(ledger_root):
    (ledger_root / "tests").mkdir(); (ledger_root / "tests/test_demo.py").write_text("x = 1\n")
    write_history(ledger_root, "C-001", "bundle-001.json", _bundle(rev=1))
    write_history(ledger_root, "C-001", "verdict-001.json",
                  {"bundle": "bundle-001", "clause": "C-001", "verdict": "accepted",
                   "by": "pyro", "rev": 1})
    led = Ledger(ledger_root)
    led.append_amendment("demo", {"rev": 2, "by": "pyro", "kind": "amend",
                                  "changes": [{"id": "C-001", "change": "modified"}]})
    # bump law rev in-file to 2 (what sign does in Plan 2)
    p = ledger_root / ".contracts/demo.contract.yaml"
    p.write_text(p.read_text().replace("rev: 1", "rev: 2"))
    assert _views(ledger_root)["C-001"].state == "stale"


def test_no_stored_state(ledger_root, capsys):
    """D0-002: read surfaces write nothing; no state key persists; derivation is pure."""
    (ledger_root / "tests").mkdir(); (ledger_root / "tests/test_demo.py").write_text("x = 1\n")
    write_history(ledger_root, "C-001", "bundle-001.json", _bundle())

    def fingerprint():
        return {p: hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(ledger_root.rglob("*")) if p.is_file()}

    before = fingerprint()
    for cmd in (["status"], ["audit"], ["tasks", "--next", "--json"]):
        run_cli(cmd, ledger_root, capsys)
    assert fingerprint() == before, "a read surface wrote to disk"


def test_no_state_keys_in_law(ledger_root):
    law = (ledger_root / ".contracts/demo.contract.yaml").read_text()
    for key in ("state:", "green:", "holding:", "broken:"):
        assert key not in law
```

Run: `uv run pytest tests/test_state.py -q` — Expected: FAIL (no `docket.state`; status/audit/tasks not yet wired — those asserts go green in Tasks 8–10; mark the `run_cli` loop with `pytest.mark.xfail` is NOT allowed — instead implement `derive_views` now and let `test_no_stored_state` stay red until Task 10, tracked in the task checklist).

- [ ] **Step 2: Implement `src/docket/state.py`**

```python
"""Derived state — the one place green/red/holding is computed. Never stored.

Precedence (design decision 15, first match wins):
  retired → deferred → stuck → review → broken → stale
  → pending-harness → holding → unstarted
Validity: a record is valid iff rev_at_filing/rev >= last amendment rev
touching its clause (design decision 4).
"""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field
from pathlib import Path

from docket.accord import flag_checks
from docket.model import Clause, Contract
from docket.storage import Ledger


@dataclass
class ClauseView:
    clause: Clause
    state: str
    flags: list[str] = field(default_factory=list)
    evidence_summary: str = "—"
    drift: str = ""
    calibration: tuple[int, int] = (0, 0)   # (clause_defects, verdicts)
    last_activity: str | None = None         # ISO timestamp


def _valid(rec: dict, rev_key: str, floor: int) -> bool:
    return int(rec.get(rev_key, 0)) >= floor


def derive_views(contract: Contract, led: Ledger, root: Path) -> list[ClauseView]:
    views = []
    for clause in contract.clauses:
        views.append(_derive_one(clause, contract, led, root))
    return views


def _derive_one(clause: Clause, contract: Contract, led: Ledger, root: Path) -> ClauseView:
    floor = led.last_amend_rev(contract.contract, clause.id)
    bundles = [b for b in led.records(clause.id, "bundle") if _valid(b, "rev_at_filing", floor)]
    checks = [c for c in led.records(clause.id, "check") if _valid(c, "rev", floor)]
    verdicts = [v for v in led.records(clause.id, "verdict") if _valid(v, "rev", floor)]
    all_verdicts = led.records(clause.id, "verdict")  # calibration counts ALL history

    flags = [f.flag for f in flag_checks(clause, list(contract.clauses), root)]
    defects = sum(1 for v in all_verdicts if v.get("rejection_type") == "clause-defect")
    cal = (defects, len(all_verdicts))

    latest_bundle = bundles[-1] if bundles else None
    latest_check = checks[-1] if checks else None
    judged = {v.get("bundle") for v in verdicts}
    accepted = [v for v in verdicts if v.get("verdict") == "accepted"]
    # an accepted verdict whose bundle got invalidated by a later amendment:
    stale_accept = [v for v in led.records(clause.id, "verdict")
                    if v.get("verdict") == "accepted" and not _valid(v, "rev", floor)]

    state = "unstarted"
    if clause.status == "retired":
        state = "retired"
    elif clause.status == "deferred":
        state = "deferred"
    elif latest_bundle and latest_bundle.get("claim") == "stuck" \
            and latest_bundle["_file"].removesuffix(".json") not in judged:
        state = "stuck"
    elif latest_bundle and latest_bundle["_file"].removesuffix(".json") not in judged:
        state = "review"
    elif latest_check and latest_check.get("result") == "red":
        state = "broken"
    elif stale_accept and not accepted:
        state = "stale"
    elif "PENDING-HARNESS" in flags:
        state = "pending-harness"
    elif "OVERLAP" in flags:
        state = "overlap"
    elif accepted:
        state = "holding"

    summary = "—"
    if latest_bundle:
        kinds = [e.get("kind", "?") for e in latest_bundle.get("evidence", [])]
        summary = ", ".join(f"{kinds.count(k)} {k}" for k in dict.fromkeys(kinds)) or "—"
        if state == "review":
            summary = "awaiting verdict"
    if state == "broken" and latest_check:
        summary = (summary + ", 1 FAIL") if summary != "—" else "1 FAIL"

    stamps = [r.get("at", "") for r in (*bundles, *checks, *verdicts) if r.get("at")]
    return ClauseView(clause=clause, state=state, flags=flags,
                      evidence_summary=summary,
                      drift=(latest_check or {}).get("drift", ""),
                      calibration=cal,
                      last_activity=max(stamps, default=None))


def freshness(views: list[ClauseView]) -> str:
    stamps = [v.last_activity for v in views if v.last_activity]
    if not stamps:
        return "—"
    newest = dt.datetime.fromisoformat(max(stamps))
    age = dt.datetime.now(newest.tzinfo) - newest
    h = int(age.total_seconds() // 3600)
    return f"{h}h" if h < 48 else f"{h // 24}d"
```

- [ ] **Step 3: Run**

Run: `uv run pytest tests/test_state.py -q` — Expected: all pass EXCEPT `test_no_stored_state` (needs status/audit/tasks CLI — Tasks 8–10). Confirm the others are green.

- [ ] **Step 4: Commit**

```bash
git add src/docket/state.py tests/test_state.py
git commit -m "derived state engine: precedence, rev-floor validity, calibration (D0-002 pending CLI)"
```

---

### Task 8: `docket check` (conformance with drift naming)

**Files:**
- Modify: `src/docket/cli.py`, `src/docket/render.py`
- Test: `tests/test_check.py`

- [ ] **Step 1: Failing tests**

`tests/test_check.py`:
```python
from tests.conftest import run_cli


def _harness(root, body):
    (root / "tests").mkdir(exist_ok=True)
    (root / "tests" / "test_demo.py").write_text(body)


def test_check_green_records_and_exits_zero(ledger_root, capsys):
    _harness(ledger_root, "def test_exit_zero():\n    assert True\n")
    code, out, err = run_cli(["check", "C-001"], ledger_root, capsys)
    assert code == 0
    assert "C-001" in out and "green" in out
    recs = list((ledger_root / ".contracts/evidence/C-001").glob("check-*.json"))
    assert len(recs) == 1


def test_check_red_names_drift_and_two_exits(ledger_root, capsys):
    """Feeds D0-004."""
    _harness(ledger_root, "def test_exit_zero():\n    assert False, 'exit was 3'\n")
    code, out, err = run_cli(["check", "C-001"], ledger_root, capsys)
    assert code == 1
    assert "FAIL" in out
    assert "drift:" in out
    assert "fix the code" in out and "amend the contract" in out


def test_check_all_quiet_ci_exit(ledger_root, capsys):
    _harness(ledger_root, "def test_exit_zero():\n    assert False\n")
    code, out, err = run_cli(["check", "--all", "--quiet"], ledger_root, capsys)
    assert code == 1
    assert out == ""


def test_check_pending_harness_not_red(ledger_root, capsys):
    code, out, err = run_cli(["check", "C-001"], ledger_root, capsys)
    assert code == 0
    assert "PENDING-HARNESS" in out


def test_check_human_routes_to_review(ledger_root, capsys):
    p = ledger_root / ".contracts/demo.contract.yaml"
    p.write_text(p.read_text().replace(
        "      test: tests/test_demo.py::test_exit_zero",
        "      verdict: human"))
    code, out, err = run_cli(["check", "C-001"], ledger_root, capsys)
    assert code == 0
    assert "docket review" in out
```

Run: `uv run pytest tests/test_check.py -q` — Expected: FAIL.

- [ ] **Step 2: Implement**

Add to `src/docket/render.py`:
```python
def check_line(clause, res) -> str:
    pad = max(2, 55 - len(f"{clause.id} {short_name(clause)}"))
    head = f"{clause.id} {short_name(clause)} " + "." * pad
    if res.result == "green":
        return f"{head} green"
    if res.result == "pending-harness":
        return f"{head} PENDING-HARNESS\n  {res.detail}"
    if res.result == "human":
        return f"{head} verdict: human — cannot go green mechanically; route to docket review"
    body = [f"{head} FAIL",
            f"  obligation:  {clause.obligation.strip()[:100]}",
            f"  evidence:    {res.detail}"]
    if res.drift:
        body.append(f"  drift:       {res.drift}")
    body.append("")
    body.append(TWO_EXITS)
    return "\n".join(body)


def short_name(clause) -> str:
    words = clause.obligation.strip().split()
    return " ".join(words[:5])[:40]
```

Add to `src/docket/cli.py` (parser + command):
```python
    chk = sub.add_parser("check", help="run acceptance, name drift, record result")
    chk.add_argument("clause", nargs="?", default=None)
    chk.add_argument("--all", action="store_true")
    chk.add_argument("--quiet", action="store_true")
```

```python
def cmd_check(args) -> int:
    from docket.render import check_line
    from docket.runner import run_acceptance
    from docket.storage import Ledger

    led = Ledger(args.root)
    failures = 0
    for contract in led.contracts():
        for clause in contract.clauses:
            if clause.status != "active":
                continue
            if not args.all and args.clause and clause.id != args.clause:
                continue
            if not args.all and not args.clause:
                continue
            res = run_acceptance(clause.acceptance, args.root, led.runner_template)
            if res.result in ("green", "red"):
                led.append_record(clause.id, "check", {
                    "clause": clause.id, "rev": contract.rev,
                    "result": res.result, "detail": res.detail, "drift": res.drift,
                })
            if res.result == "red":
                failures += 1
            if not args.quiet:
                print(check_line(clause, res))
    if not args.all and args.clause is None:
        print("docket check: name a clause or pass --all", file=sys.stderr)
        return 2
    return 1 if failures else 0
```

Register in the dispatch dict: `{"import": cmd_import, "check": cmd_check}`.

**Stale-fails-CI note:** stale (invalidated evidence) does not run here — it's a state, not a check result. `check --all` exit covers broken; the CI surface promise "any broken/stale clause fails the build" is completed in Task 9 step 4 by adding a stale sweep to `cmd_check` after the run loop:

```python
    # stale clauses fail CI too (concepts/02 §4)
    from docket.state import derive_views
    for contract in led.contracts():
        for v in derive_views(contract, led, args.root):
            if v.state == "stale" and (args.all or v.clause.id == args.clause):
                failures += 1
                if not args.quiet:
                    print(f"{v.clause.id} stale — evidence invalidated at rev "
                          f"{contract.rev}; re-verdict needed")
```

(Add it now; it's exercised by Plan 2's amend tests.)

- [ ] **Step 3: Run & commit**

Run: `uv run pytest tests/test_check.py -q` — Expected: PASS.

```bash
git add src/docket/cli.py src/docket/render.py tests/test_check.py
git commit -m "docket check: drift naming, two-exit footer, check records, CI exit codes"
```

---### Task 9: `docket status` (the glance)

**Files:**
- Modify: `src/docket/cli.py`, `src/docket/render.py`
- Test: `tests/test_status.py`

- [ ] **Step 1: Failing tests**

`tests/test_status.py`:
```python
from tests.conftest import run_cli, write_history


def test_status_empty_ledger_onboarding(tmp_path, capsys):
    (tmp_path / ".contracts").mkdir()
    code, out, err = run_cli(["status"], tmp_path, capsys)
    assert code == 0
    assert "no contracts" in out.lower()
    assert "docket import" in out


def test_status_table_and_footer(ledger_root, capsys):
    (ledger_root / "tests").mkdir()
    (ledger_root / "tests/test_demo.py").write_text("x=1\n")
    write_history(ledger_root, "C-001", "bundle-001.json",
                  {"clause": "C-001", "claim": "satisfied", "filed_by": "loop#1",
                   "rev_at_filing": 1,
                   "evidence": [{"kind": "test", "ref": "t", "result": "PASS"}]})
    code, out, err = run_cli(["status"], ledger_root, capsys)
    assert code == 0
    assert out.splitlines()[0].startswith("DOCKET — demo")
    assert "rev 1" in out
    assert "C-001" in out and "⚖" in out and "awaiting" in out
    assert "1 awaiting your verdict" in out
    assert "evidence freshness:" in out


def test_status_shows_broken_with_two_exits(ledger_root, capsys):
    """Feeds D0-004: status red states carry both exits too."""
    (ledger_root / "tests").mkdir()
    (ledger_root / "tests/test_demo.py").write_text("x=1\n")
    write_history(ledger_root, "C-001", "check-001.json",
                  {"clause": "C-001", "rev": 1, "result": "red",
                   "detail": "FAIL", "drift": "RuntimeError not in taxonomy"})
    code, out, err = run_cli(["status"], ledger_root, capsys)
    assert "✘" in out and "1 broken" in out
    assert "fix the code" in out and "amend the contract" in out
```

Run: `uv run pytest tests/test_status.py -q` — Expected: FAIL.

- [ ] **Step 2: Implement**

Add to `src/docket/render.py`:
```python
def status_report(contract, views, fresh: str) -> str:
    n_amend = max(0, contract.rev - 1)
    head = f"DOCKET — {contract.contract}"
    lines = [f"{head:<52}rev {contract.rev} ({n_amend} amendment{'s' * (n_amend != 1)})",
             f"source: {contract.source}", ""]
    lines.append(f"  {'CLAUSE':<38}{'EVIDENCE':<18}STATE")
    for v in views:
        name = f"{v.clause.id} {short_name(v.clause)}"[:36]
        state = f"{GLYPH[v.state]} {v.state if v.state != 'stale' else 're-verdict'}"
        # outstanding Accord flags never hide behind a stronger state (decision 15);
        # skip the flag already shown AS the state (e.g. pending-harness/overlap)
        extra = [f for f in v.flags if f.lower() != v.state]
        if extra:
            state += " " + " ".join(f"⚑{f}" for f in extra)
        lines.append(f"  {name:<38}{v.evidence_summary[:16]:<18}{state}")
    lines.append("")
    n_review = sum(1 for v in views if v.state == "review")
    n_broken = sum(1 for v in views if v.state == "broken")
    lines.append(f"  {n_review} awaiting your verdict · {n_broken} broken · "
                 f"evidence freshness: {fresh}")
    if n_broken:
        lines.append("")
        lines.append(TWO_EXITS)
    return "\n".join(lines)


ONBOARDING = ("no contracts in .contracts/ — this docket is empty.\n"
              "  bring law to the courtroom:  docket import <file.contract.yaml>")
```

Add to `src/docket/cli.py`:
```python
    sub.add_parser("status", help="the glance — derived state of every clause")
```

```python
def cmd_status(args) -> int:
    from docket.render import ONBOARDING, status_report
    from docket.state import derive_views, freshness
    from docket.storage import Ledger

    led = Ledger(args.root)
    contracts = led.contracts()
    if not contracts:
        print(ONBOARDING)
        return 0
    for contract in contracts:
        views = derive_views(contract, led, args.root)
        print(status_report(contract, views, freshness(views)))
    return 0
```

Dispatch: add `"status": cmd_status`.

- [ ] **Step 3: Run & commit**

Run: `uv run pytest tests/test_status.py -q` — Expected: PASS.

```bash
git add src/docket/cli.py src/docket/render.py tests/test_status.py
git commit -m "docket status: derived glance, onboarding empty state, broken footer"
```

---

### Task 10: `docket audit` + `tasks`/`file` (agent surface)

**Files:**
- Modify: `src/docket/cli.py`, `src/docket/render.py`
- Test: `tests/test_audit.py`, `tests/test_tasks_file.py`

- [ ] **Step 1: Failing tests**

`tests/test_audit.py`:
```python
from tests.conftest import run_cli

COVERAGE = """\
cells:
  - "scan × success"
  - "scan × empty"
  - "scan × failure"
deferred:
  - "scan × empty"
"""


def test_audit_without_manifest_names_the_dark(ledger_root, capsys):
    code, out, err = run_cli(["audit"], ledger_root, capsys)
    assert code == 0
    assert "no coverage manifest" in out
    assert "uncovered regions unknown" in out


def test_audit_with_manifest_shows_uncovered(ledger_root, capsys):
    (ledger_root / ".contracts/coverage.yaml").write_text(COVERAGE)
    # demo clause has no surface anchor → all 3 cells uncovered/deferred
    code, out, err = run_cli(["audit"], ledger_root, capsys)
    assert "0/3 covered" in out
    assert "scan × failure" in out          # named, not just counted
    assert "deferred (signed): 1" in out


def test_audit_sections_present(ledger_root, capsys):
    code, out, err = run_cli(["audit"], ledger_root, capsys)
    for token in ("COVERAGE", "surface cells", "failure states", "NFR", "risk"):
        assert token in out
```

`tests/test_tasks_file.py`:
```python
import json

from tests.conftest import run_cli, write_history


def test_tasks_next_json(ledger_root, capsys):
    code, out, err = run_cli(["tasks", "--next", "--json"], ledger_root, capsys)
    assert code == 0
    task = json.loads(out)
    assert task["clause"] == "C-001"
    assert task["rev"] == 1
    assert task["acceptance"] == {"test": "tests/test_demo.py::test_exit_zero"}
    assert task["filed_evidence"] == []


def test_tasks_clear_when_all_green(ledger_root, capsys):
    (ledger_root / "tests").mkdir(); (ledger_root / "tests/test_demo.py").write_text("x=1\n")
    write_history(ledger_root, "C-001", "bundle-001.json",
                  {"clause": "C-001", "claim": "satisfied", "filed_by": "l",
                   "rev_at_filing": 1, "evidence": []})
    write_history(ledger_root, "C-001", "verdict-001.json",
                  {"bundle": "bundle-001", "clause": "C-001",
                   "verdict": "accepted", "by": "pyro", "rev": 1})
    code, out, err = run_cli(["tasks", "--next"], ledger_root, capsys)
    assert code == 0
    assert "docket clear" in out


def test_file_appends_bundle(ledger_root, capsys, tmp_path):
    b = tmp_path / "bundle.json"
    b.write_text(json.dumps({"clause": "C-001", "claim": "satisfied",
                             "filed_by": "claude-loop#7", "rev_at_filing": 1,
                             "evidence": [{"kind": "test", "ref": "t", "result": "PASS"}]}))
    code, out, err = run_cli(["file", "C-001", "--bundle", str(b)], ledger_root, capsys)
    assert code == 0
    assert "filed → review queue" in out and "⚖" in out
    assert (ledger_root / ".contracts/evidence/C-001/bundle-001.json").exists()


def test_file_rev_mismatch_refused(ledger_root, capsys, tmp_path):
    b = tmp_path / "bundle.json"
    b.write_text(json.dumps({"clause": "C-001", "claim": "satisfied",
                             "filed_by": "l", "rev_at_filing": 99, "evidence": []}))
    code, out, err = run_cli(["file", "C-001", "--bundle", str(b)], ledger_root, capsys)
    assert code == 2
    assert "rev mismatch" in err and "refile" in err


def test_file_malformed_refused(ledger_root, capsys, tmp_path):
    b = tmp_path / "bundle.json"
    b.write_text(json.dumps({"clause": "C-001"}))
    code, out, err = run_cli(["file", "C-001", "--bundle", str(b)], ledger_root, capsys)
    assert code == 2
    assert "malformed" in err
```

Run: `uv run pytest tests/test_audit.py tests/test_tasks_file.py -q` — Expected: FAIL.

- [ ] **Step 2: Implement audit render + commands**

Add to `src/docket/render.py`:
```python
FAILURE_TOKENS = ("failure", "denied", "error", "timeout", "conflict", "invalid")


def audit_report(contract, views, manifest) -> str:
    covered = sorted({a.value for v in views for a in v.clause.anchors
                      if a.typ == "surface" and v.clause.status == "active"})
    lines = [f"COVERAGE — {contract.contract}".ljust(52) + f"rev {contract.rev}"]
    if manifest:
        cells = manifest["cells"]
        deferred = [c for c in manifest["deferred"] if c in cells]
        uncovered = [c for c in cells if c not in covered and c not in deferred]
        lines.append(f"  surface cells:   {len([c for c in cells if c in covered])}/{len(cells)} covered"
                     f" · deferred (signed): {len(deferred)} · {len(uncovered)} UNCOVERED")
        for c in uncovered:
            lines.append(f"     UNCOVERED:    {c}")
    else:
        lines.append(f"  surface cells:   covered: {len(covered)} "
                     f"(no coverage manifest — uncovered regions unknown)")
    fail_cov = [c for c in covered if any(t in c.lower() for t in FAILURE_TOKENS)]
    lines.append(f"  failure states:  {len(fail_cov)} contracted")
    metrics = [v for v in views if v.clause.acceptance.kind == "metric"]
    lines.append(f"  NFR targets:     {len(metrics)}/{len(metrics)} numbered")
    high = [v for v in views if v.clause.risk == "high"]
    ok = all(len(v.clause.evidence_required or []) >= 2 for v in high)
    lines.append(f"  risk:            {len(high)} high-risk clause{'s' * (len(high) != 1)}"
                 + (f" · evidence_required ≥2 on all ✔" if high and ok else
                    (" · THIN-EVIDENCE outstanding ✘" if high else "")))
    humans = sum(1 for v in views if v.clause.acceptance.kind == "human")
    lines.append(f"  human verdict:   {humans} clause{'s' * (humans != 1)}")
    flags = sorted({f for v in views for f in v.flags})
    if flags:
        lines.append(f"  open flags:      {', '.join(flags)}")
    lines.append("")
    lines.append("  → uncovered regions are visible. Contract them, defer them signed,")
    lines.append("    or accept the dark. The audit does not pretend completeness —")
    lines.append("    it makes incompleteness inspectable.")
    return "\n".join(lines)
```

Add to `src/docket/cli.py` (parsers):
```python
    sub.add_parser("audit", help="coverage views — incompleteness made inspectable")

    tsk = sub.add_parser("tasks", help="derived task view: clause minus evidence")
    tsk.add_argument("--next", action="store_true")
    tsk.add_argument("--json", action="store_true")

    fil = sub.add_parser("file", help="file an evidence bundle (append-only)")
    fil.add_argument("clause")
    fil.add_argument("--bundle", type=Path, required=True)
```

Commands:
```python
def cmd_audit(args) -> int:
    from docket.render import audit_report
    from docket.state import derive_views
    from docket.storage import Ledger
    led = Ledger(args.root)
    for contract in led.contracts():
        print(audit_report(contract, derive_views(contract, led, args.root),
                           led.coverage_manifest()))
    return 0


def cmd_tasks(args) -> int:
    import json as _json
    from docket.state import derive_views
    from docket.storage import Ledger
    led = Ledger(args.root)
    todo = []
    for contract in led.contracts():
        for v in derive_views(contract, led, args.root):
            if v.state in ("unstarted", "broken", "pending-harness", "stale"):
                todo.append((contract, v))
    if not todo:
        print("docket clear — every active clause is holding or awaiting verdict")
        return 0
    if args.next:
        contract, v = todo[0]
        if args.json:
            bundles = led.records(v.clause.id, "bundle")
            print(_json.dumps({
                "clause": v.clause.id,
                "obligation": v.clause.obligation.strip(),
                "acceptance": v.clause.acceptance.model_dump(exclude_none=True),
                "rev": contract.rev,
                "filed_evidence": [b["_file"] for b in bundles],
            }))
        else:
            print(f"{v.clause.id} [{v.state}] {v.clause.obligation.strip()[:90]}")
        return 0
    for contract, v in todo:
        print(f"{v.clause.id} [{v.state}] {v.clause.obligation.strip()[:90]}")
    return 0


def cmd_file(args) -> int:
    import json as _json
    from docket.storage import Ledger
    led = Ledger(args.root)
    try:
        payload = _json.loads(Path(args.bundle).read_text())
    except Exception as e:
        print(f"docket file: malformed bundle — {e}", file=sys.stderr)
        return 2
    required = {"clause", "claim", "filed_by", "rev_at_filing", "evidence"}
    if not required <= set(payload):
        print(f"docket file: malformed bundle — missing {sorted(required - set(payload))}",
              file=sys.stderr)
        return 2
    target = None
    for contract in led.contracts():
        for clause in contract.clauses:
            if clause.id == args.clause:
                target = (contract, clause)
    if target is None:
        print(f"docket file: unknown clause {args.clause}", file=sys.stderr)
        return 2
    contract, clause = target
    if payload["rev_at_filing"] != contract.rev:
        print(f"docket file: rev mismatch — bundle filed against rev "
              f"{payload['rev_at_filing']}, law is rev {contract.rev}. refile.",
              file=sys.stderr)
        return 2
    if payload["claim"] == "stuck" and "stuck_on" not in payload:
        print("docket file: a failure report needs stuck_on", file=sys.stderr)
        return 2
    p = led.append_record(args.clause, "bundle", payload)
    print(f"✔ filed → review queue (status: ⚖) · {p.relative_to(args.root)}")
    return 0
```

Dispatch: `{"import": cmd_import, "check": cmd_check, "status": cmd_status, "audit": cmd_audit, "tasks": cmd_tasks, "file": cmd_file}`.

- [ ] **Step 3: Run the whole suite — D0-002 closes here**

Run: `uv run pytest -q` — Expected: ALL PASS including `test_no_stored_state` (status/audit/tasks now exist and must not write; if the fingerprint assert fails, find the write and remove it — read surfaces never touch disk).

- [ ] **Step 4: Commit**

```bash
git add src/docket/cli.py src/docket/render.py tests/test_audit.py tests/test_tasks_file.py
git commit -m "audit + agent surface: coverage views, tasks --next --json, file with refile semantics"
```

---

### Task 11: Plan-1 closeout — fixture smoke, README, review gate

**Files:**
- Modify: `README.md` (status line only)
- Test: `tests/test_import.py` (one more case)

- [ ] **Step 1: Tipsy smoke test (second horse fixture)**

Append to `tests/test_import.py`:
```python
def test_tipsy_pressure_bundle_imports_clean(tmp_path, capsys):
    tipsy = REPO / "docs/dojo/runs/pressure-tipsy/tipsy/.contracts/tipsy.contract.yaml"
    (tmp_path / ".contracts").mkdir()
    code, out, err = run_cli(["import", str(tipsy)], tmp_path, capsys)
    assert code == 0
    assert "admitted: 16" in out
    assert "refused: 0" in out
```

Run: `uv run pytest -q` — Expected: ALL PASS.

- [ ] **Step 2: Full-suite verification before claiming done**

```bash
uv run pytest -q
uv run docket --root /tmp/smoke-$$ status 2>&1 | head -3   # onboarding line, no crash
```

- [ ] **Step 3: Commit + request review**

```bash
git add tests/test_import.py
git commit -m "plan 1 closeout: tipsy smoke import"
```

Then STOP. Gate before Plan 2: Codie reviews the door + state implementation against `docs/concepts/01`–`02` (his Accord doctrine; ask specifically about design decisions 6, 7, 15) — `/codex:rescue` with this plan's "Design decisions" section as context. Address findings before opening Plan 2.

---

## Self-review checklist (run after writing, before execution)

- Spec coverage: concepts/03 "In" list — import/add door ✔ (add itself is Plan 2 legislature), check ✔, status ✔, audit ✔, tasks/file ✔; review/amend/sign → Plan 2; recursive fixture → Plan 2.
- D0 bindings in this plan: D0-001 (test_door), D0-002 (test_state), D0-006 (test_exec), D0-007 substance (test_import golden); D0-003/D0-004(review part)/D0-005 → Plan 2.
- The golden-fixture regression (24/24, 0 refusals) guards every door change.
