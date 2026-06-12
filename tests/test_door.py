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


def test_a7_unhashable_id_refused_not_crash():
    rep = door(contract(clause(id=["C-001"])))
    assert ("C-001" not in {f.clause_id for f in rep.refusals} or True)  # no crash is the point
    assert any(f.check == "A7" for f in rep.refusals)
    assert rep.admitted == []


def test_a6_metric_acceptance_exempt_from_raw_dict():
    rep = door(contract(clause(
        obligation="Startup MUST be fast.",
        acceptance={"metric": "scripts/bench.sh", "threshold": "p95 < 50ms"})))
    assert rep.refusals == []


def test_a8_newline_dash_list_refused():
    rep = door(contract(clause(
        obligation="The tool MUST handle:\n- input files\n- directories")))
    assert ("C-001", "A8") in refusal_checks(rep)


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
