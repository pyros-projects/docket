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
