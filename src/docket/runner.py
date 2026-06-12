"""Subprocess delegation — docket executes nothing domain-specific (D0-006).

Judgment surface: exit codes for test/command; threshold extraction for
metric. Threshold grammar (design decision 2):
  "<label words> <op> <number><unit> [trailing prose]"
matched against `name: value` lines on the metric script's stdout by
label-token overlap.

Commands are law: authored and signed by the authority. The runner is not a
sandbox — the signature is the trust boundary.
"""
from __future__ import annotations

import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from docket.model import Acceptance

_THRESH = re.compile(r"^(?P<label>[^<>=]*?)\s*(?P<op>[<>]=?)\s*(?P<num>\d+(?:\.\d+)?)\s*(?P<unit>[A-Za-zµ%]*)")
_OUT_LINE = re.compile(r"^(?P<name>[A-Za-z_][\w .-]*?)\s*[:=]\s*(?P<num>-?\d+(?:\.\d+)?)\s*(?P<unit>[A-Za-zµ%]*)\s*$")


@dataclass
class RunResult:
    result: str            # green | red | pending-harness | human
    detail: str = ""       # one-line summary for records/render
    drift: str = ""        # what diverged (red only)
    output_tail: str = ""  # last lines of subprocess output


def parse_threshold(threshold: str) -> tuple[str, float, str]:
    m = _THRESH.search(threshold)
    if not m:
        raise ValueError(f"unparseable threshold: {threshold!r}")
    return m.group("op"), float(m.group("num")), m.group("unit").lower()


def threshold_label_tokens(threshold: str) -> set[str]:
    m = _THRESH.search(threshold)
    label = m.group("label") if m else threshold
    return set(re.findall(r"[a-z0-9]+", label.lower())) - {"the", "a", "an", "on", "of"}


def _compare(value: float, op: str, bound: float) -> bool:
    return {"<": value < bound, "<=": value <= bound,
            ">": value > bound, ">=": value >= bound}[op]


WRAPPERS = {"timeout", "env", "nice", "nohup", "stdbuf"}
_SEGMENT_SPLIT = re.compile(r"\|\||&&|;|\||\$\(|<\(|\(")


def command_harness_missing(command: str, root: Path) -> str | None:
    """A3 for command acceptance: first command-position token that resolves
    nowhere. Scans every pipeline/subshell segment, sees through wrappers."""
    for segment in _SEGMENT_SPLIT.split(command):
        for tok in segment.strip().split():
            tok = tok.strip("'\"")
            if tok in WRAPPERS or re.fullmatch(r"[A-Z_]+=\S*", tok) \
                    or re.fullmatch(r"-{1,2}[\w-]+|\d+(?:\.\d+)?[smh]?", tok) \
                    or tok.startswith(("<", ">")) or re.fullmatch(r"\d+[<>]&?\d*", tok):
                continue  # wrapper, env assignment, option, duration, or redirect
            if not (shutil.which(tok) or (root / tok).exists()):
                return tok
            break  # segment's command resolves; rest are its arguments
    return None


TIMEOUT_S = 600


def _txt(s) -> str:
    """TimeoutExpired.stdout/stderr can be None or bytes even in text mode."""
    if s is None:
        return ""
    return s.decode(errors="replace") if isinstance(s, bytes) else s


def _run(cmd: str, root: Path) -> subprocess.CompletedProcess:
    # bash, not sh: graduation fixtures use process substitution (decision 1)
    try:
        return subprocess.run(cmd, shell=True, executable="/bin/bash", cwd=root,
                              capture_output=True, text=True, timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired as e:
        return subprocess.CompletedProcess(
            args=cmd, returncode=124,
            stdout=_txt(e.stdout),
            stderr=_txt(e.stderr) + f"\ndocket: acceptance timed out after {TIMEOUT_S}s")


def _tail(proc: subprocess.CompletedProcess, n: int = 12) -> str:
    return "\n".join((proc.stdout + proc.stderr).strip().splitlines()[-n:])


def run_acceptance(acc: Acceptance, root: Path,
                   runner_template: Callable[[str], str]) -> RunResult:
    if acc.kind == "human":
        return RunResult("human", "verdict: human — route to docket review")

    # A3 live: missing harness is pending, not red (TDD order)
    if acc.kind in ("test", "metric") and not (Path(root) / acc.target).exists():
        return RunResult("pending-harness", f"{acc.target} missing")
    if acc.kind == "command":
        if (tok := command_harness_missing(acc.command, Path(root))):
            return RunResult("pending-harness", f"{tok} not resolvable")

    if acc.kind == "test":
        proc = _run(runner_template("test").format(ref=acc.test), root)
        if proc.returncode == 0:
            return RunResult("green", f"{acc.test} PASS", output_tail=_tail(proc))
        return RunResult("red", f"{acc.test} FAIL",
                         drift=_extract_failure(proc), output_tail=_tail(proc))

    if acc.kind == "command":
        proc = _run(acc.command, root)
        if proc.returncode == 0:
            return RunResult("green", f"command exit 0 — expect: {acc.expect}",
                             output_tail=_tail(proc))
        return RunResult("red", f"command exit {proc.returncode}",
                         drift=f"expected: {acc.expect}", output_tail=_tail(proc))

    # metric
    proc = _run(acc.metric, root)
    if proc.returncode != 0:
        return RunResult("red", f"{acc.metric} exit {proc.returncode}",
                         drift="metric script failed", output_tail=_tail(proc))
    op, bound, unit = parse_threshold(acc.threshold)
    want = threshold_label_tokens(acc.threshold)
    for line in proc.stdout.splitlines():
        m = _OUT_LINE.match(line.strip())
        if not m:
            continue
        have = set(re.findall(r"[a-z0-9]+", m.group("name").lower()))
        if want & have:
            line_unit = m.group("unit").lower()
            if unit and line_unit and line_unit != unit:
                continue  # decision 2: unit mismatch = not the contracted metric
            value = float(m.group("num"))
            ok = _compare(value, op, bound)
            detail = f"{m.group('name').strip()} = {value} (threshold {op} {bound}{unit})"
            if ok:
                return RunResult("green", detail, output_tail=_tail(proc))
            return RunResult("red", detail,
                             drift=f"measured {value}, contracted {op} {bound}{unit}",
                             output_tail=_tail(proc))
    return RunResult("red", f"threshold {acc.threshold!r}",
                     drift=f"metric matching {sorted(want)} not found in output",
                     output_tail=_tail(proc))


def _extract_failure(proc: subprocess.CompletedProcess) -> str:
    """Drift naming: surface the assertion/error line, not the whole log."""
    lines = (proc.stdout + proc.stderr).splitlines()
    for pat in (r"^E\s+", r"Error", r"assert", r"FAILED"):
        hits = [l.strip() for l in lines if re.search(pat, l)]
        if hits:
            return hits[-1][:160]
    return (lines[-1].strip()[:160]) if lines else "no output"
