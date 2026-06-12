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
