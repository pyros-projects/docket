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


def test_tasks_excludes_review_and_stuck(ledger_root, capsys):
    (ledger_root / "tests").mkdir(); (ledger_root / "tests/test_demo.py").write_text("x=1\n")
    write_history(ledger_root, "C-001", "bundle-001.json",
                  {"clause": "C-001", "claim": "stuck", "stuck_on": "flaky",
                   "filed_by": "l", "rev_at_filing": 1, "evidence": []})
    code, out, err = run_cli(["tasks", "--next"], ledger_root, capsys)
    assert code == 0
    assert "docket clear" in out          # stuck waits for a verdict, not a worker


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
