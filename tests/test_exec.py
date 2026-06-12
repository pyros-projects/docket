import json
import stat
from pathlib import Path

from docket.runner import run_acceptance, threshold_label_tokens, parse_threshold
from docket.model import AcceptanceCommand, AcceptanceMetric, AcceptanceTest, AcceptanceHuman
from docket.storage import Ledger


def _script(root: Path, name: str, body: str) -> str:
    p = root / name
    p.write_text(f"#!/bin/sh\n{body}\n")
    p.chmod(p.stat().st_mode | stat.S_IEXEC)
    return name


def test_threshold_parsing():
    assert parse_threshold("p95 < 50ms") == ("<", 50.0, "ms")
    assert parse_threshold("peak RSS < 64 MB on the 100 MB reference input") == ("<", 64.0, "mb")
    assert parse_threshold("wall clock < 5 s on the 100 MB reference input") == ("<", 5.0, "s")
    assert threshold_label_tokens("peak RSS < 64 MB ...") == {"peak", "rss"}
    assert threshold_label_tokens("wall clock < 5 s ...") == {"wall", "clock"}


def test_delegation_only(ledger_root):
    """D0-006: acceptance runs via subprocess, judged by exit code/threshold only."""
    marker = ledger_root / "ran.marker"
    name = _script(ledger_root, "ok.sh", f"touch {marker}\nexit 0")
    res = run_acceptance(AcceptanceCommand(command=f"./{name}", expect="exit 0"),
                         ledger_root, Ledger(ledger_root).runner_template)
    assert res.result == "green"
    assert marker.exists()                       # really ran, out of process
    bad = _script(ledger_root, "bad.sh", "exit 1")
    res2 = run_acceptance(AcceptanceCommand(command=f"./{bad}", expect="exit 0"),
                          ledger_root, Ledger(ledger_root).runner_template)
    assert res2.result == "red"


def test_metric_threshold_judged(ledger_root):
    name = _script(ledger_root, "bench.sh",
                   'echo "peak_rss_mb: 41.2"\necho "wall_clock_s: 3.7"')
    green = run_acceptance(
        AcceptanceMetric(metric=f"./{name}", threshold="peak RSS < 64 MB"),
        ledger_root, Ledger(ledger_root).runner_template)
    assert green.result == "green" and "41.2" in green.detail
    red = run_acceptance(
        AcceptanceMetric(metric=f"./{name}", threshold="wall clock < 2 s"),
        ledger_root, Ledger(ledger_root).runner_template)
    assert red.result == "red"
    lost = run_acceptance(
        AcceptanceMetric(metric=f"./{name}", threshold="latency < 9 ms"),
        ledger_root, Ledger(ledger_root).runner_template)
    assert lost.result == "red" and "not found" in lost.drift


def test_pending_harness_and_human(ledger_root):
    res = run_acceptance(AcceptanceTest(test="tests/nope.py::test_x"),
                         ledger_root, Ledger(ledger_root).runner_template)
    assert res.result == "pending-harness"
    res2 = run_acceptance(AcceptanceHuman(verdict="human"),
                          ledger_root, Ledger(ledger_root).runner_template)
    assert res2.result == "human"


def test_a3_command_sees_through_wrappers_and_pipes(ledger_root):
    from docket.runner import command_harness_missing
    assert command_harness_missing(
        "timeout 30 mdtodo demo/docs >/dev/null 2>&1; test $? -ne 124",
        ledger_root) == "mdtodo"
    assert command_harness_missing(
        "echo '42.50' | tipsy 2>&1; test $? -eq 2", ledger_root) == "tipsy"
    assert command_harness_missing(
        "diff <(tipsy 10) <(tipsy 10)", ledger_root) == "tipsy"
    assert command_harness_missing("true && echo ok", ledger_root) is None
    assert command_harness_missing("cat /etc/hostname; >out.txt true", ledger_root) is None


def test_commands_run_under_bash(ledger_root):
    res = run_acceptance(
        AcceptanceCommand(command="diff <(echo a) <(echo a)",
                          expect="process substitution works"),
        ledger_root, Ledger(ledger_root).runner_template)
    assert res.result == "green"


def test_timeout_is_red_not_crash(ledger_root, monkeypatch):
    import docket.runner as runner_mod
    monkeypatch.setattr(runner_mod, "TIMEOUT_S", 1)
    res = run_acceptance(AcceptanceCommand(command="sleep 5", expect="exit 0"),
                         ledger_root, Ledger(ledger_root).runner_template)
    assert res.result == "red"
    assert "timed out" in res.output_tail


def test_unit_mismatch_not_green(ledger_root):
    name = _script(ledger_root, "bench_gb.sh", 'echo "peak rss: 2 GB"')
    res = run_acceptance(
        AcceptanceMetric(metric=f"./{name}", threshold="peak RSS < 64 MB"),
        ledger_root, Ledger(ledger_root).runner_template)
    assert res.result == "red"
    assert "not found" in res.drift
