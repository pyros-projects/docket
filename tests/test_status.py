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


def test_status_writes_nothing(ledger_root, capsys):
    import hashlib
    def fp():
        return {p: hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(ledger_root.rglob("*")) if p.is_file()}
    before = fp()
    run_cli(["status"], ledger_root, capsys)
    assert fp() == before
