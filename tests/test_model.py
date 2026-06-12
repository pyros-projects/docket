from docket.cli import main


def test_version(capsys):
    import pytest
    with pytest.raises(SystemExit) as e:
        main(["--version"])
    assert e.value.code == 0
    assert capsys.readouterr().out.startswith("docket ")


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
