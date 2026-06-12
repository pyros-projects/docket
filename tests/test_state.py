import hashlib

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


def test_freshness_handles_naive_and_unparseable_stamps():
    from docket.state import ClauseView, freshness
    from docket.model import Clause
    cl = Clause.model_validate({"id": "C-001", "obligation": "X MUST hold.",
                                "acceptance": {"test": "t.py::t"},
                                "anchors": [{"decision": "D-001"}]})
    views = [ClauseView(clause=cl, state="unstarted", last_activity="2026-06-12T10:00:00"),
             ClauseView(clause=cl, state="unstarted", last_activity="garbage"),
             ClauseView(clause=cl, state="unstarted", last_activity=None)]
    out = freshness(views)
    assert out.endswith(("h", "d")) and not out.startswith("-")


def test_no_state_keys_in_law(ledger_root):
    law = (ledger_root / ".contracts/demo.contract.yaml").read_text()
    for key in ("state:", "green:", "holding:", "broken:"):
        assert key not in law
