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
