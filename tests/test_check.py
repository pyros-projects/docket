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
