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
    assert re.search(r"⚑ B-010 \[A5\] OVERLAP", out)
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


def test_import_cross_contract_id_collision_refused(ledger_root, capsys, tmp_path):
    other = tmp_path / "other.contract.yaml"
    other.write_text(
        "contract: other\nrev: 1\nsource: t\nsigned: []\n"
        "clauses:\n"
        "  - id: C-001\n"
        "    obligation: >\n      other MUST exit 1 on failure.\n"
        "    acceptance:\n      test: tests/test_o.py::test_o\n"
        "    anchors:\n      - decision: D-001\n"
        "  - id: C-900\n"
        "    obligation: >\n      other MUST write logs.\n"
        "    acceptance:\n      test: tests/test_o.py::test_o2\n"
        "    anchors:\n      - decision: D-002\n")
    code, out, err = run_cli(["import", str(other)], ledger_root, capsys)
    assert code == 0                      # C-900 still admitted
    assert "admitted: 1" in out
    assert re.search(r"✘ C-001 \[A7\].*already law.*demo", out)


def test_tipsy_pressure_bundle_imports_clean(tmp_path, capsys):
    tipsy = REPO / "docs/dojo/runs/pressure-tipsy/tipsy/.contracts/tipsy.contract.yaml"
    (tmp_path / ".contracts").mkdir()
    code, out, err = run_cli(["import", str(tipsy)], tmp_path, capsys)
    assert code == 0
    assert "admitted: 16" in out
    assert "refused: 0" in out


def test_a5_overlap_flags_across_contracts(ledger_root, capsys, tmp_path):
    other = tmp_path / "other.contract.yaml"
    other.write_text(
        "contract: other\nrev: 1\nsource: t\nsigned: []\n"
        "clauses:\n"
        "  - id: C-800\n"
        "    obligation: >\n      other MUST exit 0 on success.\n"
        "    acceptance:\n      test: tests/test_demo.py::test_exit_zero\n"
        "    anchors:\n      - decision: D-001\n")
    code, out, err = run_cli(["import", str(other)], ledger_root, capsys)
    assert code == 0
    assert "OVERLAP" in out      # C-800 shares demo C-001's test nodeid


def test_all_refused_import_still_cites_checks(tmp_path, capsys):
    (tmp_path / ".contracts").mkdir()
    bad = tmp_path / "hopeless.contract.yaml"
    bad.write_text(
        "contract: hopeless\nrev: 1\nsource: t\nsigned: []\n"
        "clauses:\n"
        "  - id: H-001\n"
        "    obligation: >\n      The tool SHOULD be nice.\n"
        "    acceptance:\n      test: tests/t.py::t\n"
        "    anchors:\n      - decision: D-001\n")
    code, out, err = run_cli(["import", str(bad)], tmp_path, capsys)
    assert code == 2
    assert "✘ H-001 [A4]" in out
    assert not (tmp_path / ".contracts/hopeless.contract.yaml").exists()
