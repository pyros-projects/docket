"""The Accord — door policy A1–A9 per docs/concepts/01.

Two outcome classes: refuse (clause does not enter) and flag (clause enters
carrying an obligation to resolve). Flags are re-derived live by state.py;
the door's output is the import-time report.
"""
from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path

from pydantic import ValidationError

from docket.model import QUALITATIVE_WORDS, Clause

MESSAGES = {
    "A1": "no acceptance procedure — how would I check this?",
    "A2": "where did this come from?",
    "A3": "clause is law; it cannot go green until the harness exists",
    "A4": "a hope, not an obligation",
    "A4-should": "decide or defer",
    "A5": "resolve before first verdict",
    "A6": "give me a number, a test, or defer the clause",
    "A8": "two laws in one clause — split them",
    "A9": "a high-risk invariant deserves more than one kind of evidence",
}


@dataclass
class Finding:
    check: str
    clause_id: str | None
    outcome: str            # "refuse" | "flag"
    message: str
    flag: str | None = None  # PENDING-HARNESS | OVERLAP | THIN-EVIDENCE


@dataclass
class DoorReport:
    admitted: list[Clause] = field(default_factory=list)
    refusals: list[Finding] = field(default_factory=list)
    flags: list[Finding] = field(default_factory=list)
    overrides: list[dict] = field(default_factory=list)
    file_error: str | None = None


_MUST_NOT = re.compile(r"\bMUST NOT\b")
_MUST = re.compile(r"\bMUST\b(?! NOT)")
_HOPE = re.compile(r"\bSHOULD\b|\bMAY\b")
_ENUM = re.compile(r"\(\s*\d+\s*\)\s|\n\s*[-*]\s")


def _rfc2119_count(obligation: str) -> int:
    return len(_MUST_NOT.findall(obligation)) + len(_MUST.findall(obligation))


def _check_a4(c: dict) -> Finding | None:
    ob = str(c.get("obligation", ""))
    if _HOPE.search(ob):
        return Finding("A4", c.get("id"), "refuse", MESSAGES["A4-should"])
    if _rfc2119_count(ob) == 0:
        return Finding("A4", c.get("id"), "refuse", MESSAGES["A4"])
    return None


def _check_a8(c: dict) -> Finding | None:
    ob = str(c.get("obligation", ""))
    if _rfc2119_count(ob) > 1 or _ENUM.search(ob):
        return Finding("A8", c.get("id"), "refuse", MESSAGES["A8"])
    return None


def _check_a6(c: dict) -> Finding | None:
    ob = str(c.get("obligation", ""))
    words = set(re.findall(r"[a-z]+", ob.lower()))
    if not (words & QUALITATIVE_WORDS):
        return None
    if re.search(r"\d", ob):
        return None
    acc = c.get("acceptance")
    # raw dict check is equivalent to parsed.acceptance.kind: A6 only runs after pydantic validation succeeds
    if isinstance(acc, dict) and "metric" in acc:
        return None  # the number lives in the threshold
    return Finding("A6", c.get("id"), "refuse", MESSAGES["A6"])


def run_door(data: dict, root: Path, sign_unanchored: str | None = None,
             extra_cohort: "Iterable[Clause]" = ()) -> DoorReport:
    rep = DoorReport()
    clauses = data.get("clauses") or []
    seen_ids: dict[str, int] = {}
    for c in clauses:
        cid = c.get("id") if isinstance(c, dict) else None
        if not isinstance(cid, str):
            cid = None
        seen_ids[cid] = seen_ids.get(cid, 0) + 1

    parsed_ok: list[tuple[dict, Clause]] = []
    for raw in clauses:
        if not isinstance(raw, dict):
            rep.refusals.append(Finding("A7", None, "refuse", f"clause is not a mapping: {raw!r}"))
            continue
        cid = raw.get("id")
        if not isinstance(cid, str):
            cid = None  # non-str id falls through to pydantic validation -> A7
        # A7: duplicate ids
        if cid is not None and seen_ids.get(cid, 0) > 1:
            rep.refusals.append(Finding("A7", cid, "refuse", f"duplicate clause id {cid}"))
            continue
        # A1: acceptance presence/shape (routed before generic A7)
        if "acceptance" not in raw:
            rep.refusals.append(Finding("A1", cid, "refuse", MESSAGES["A1"]))
            continue
        try:
            parsed = Clause.model_validate(raw)
        except ValidationError as e:
            locs = {err["loc"][0] for err in e.errors() if err["loc"]}
            if "acceptance" in locs:
                rep.refusals.append(Finding("A1", cid, "refuse", MESSAGES["A1"]))
            else:
                rep.refusals.append(Finding("A7", cid, "refuse",
                                            f"schema: {e.errors()[0]['msg']}"))
            continue
        # A4 / A8 / A6
        if (f := _check_a4(raw)):
            rep.refusals.append(f); continue
        if (f := _check_a8(raw)):
            rep.refusals.append(f); continue
        if (f := _check_a6(raw)):
            rep.refusals.append(f); continue
        # A1 (form): a metric threshold must carry the parseable grammar
        if parsed.acceptance.kind == "metric":
            from docket.runner import parse_threshold
            try:
                parse_threshold(parsed.acceptance.threshold)
            except ValueError:
                rep.refusals.append(Finding("A1", parsed.id, "refuse",
                    f"threshold {parsed.acceptance.threshold!r} has no comparator+number — "
                    + MESSAGES["A6"]))
                continue
        # A2: anchors
        if not parsed.anchors:
            if sign_unanchored:
                rep.overrides.append({"id": parsed.id, "check": "A2",
                                      "signed_by": sign_unanchored})
            else:
                rep.refusals.append(Finding("A2", parsed.id, "refuse", MESSAGES["A2"]))
                continue
        parsed_ok.append((raw, parsed))

    cohort = [p for _, p in parsed_ok]
    full_cohort = cohort + list(extra_cohort)
    for raw, parsed in parsed_ok:
        rep.admitted.append(parsed)
        rep.flags.extend(flag_checks(parsed, full_cohort, root))
    return rep


def flag_checks(clause: Clause, cohort: list[Clause], root: Path) -> list[Finding]:
    """A3, A5, A9 — also reused live by state.py (design decision 5)."""
    out: list[Finding] = []
    acc = clause.acceptance
    # A3: acceptance target exists
    if acc.kind in ("test", "metric"):
        if not (Path(root) / acc.target).exists():
            out.append(Finding("A3", clause.id, "flag",
                               f"{acc.target} missing — {MESSAGES['A3']}",
                               flag="PENDING-HARNESS"))
    elif acc.kind == "command":
        from docket.runner import command_harness_missing  # lazy: avoids cycle
        if (tok := command_harness_missing(acc.command, Path(root))):
            out.append(Finding("A3", clause.id, "flag",
                               f"{tok} not resolvable — {MESSAGES['A3']}",
                               flag="PENDING-HARNESS"))
    # A5: overlap (metric-scoped, design decision 7)
    for other in cohort:
        if other.id == clause.id or other.acceptance.kind != acc.kind:
            continue
        if acc.kind == "test" and other.acceptance.test == acc.test:
            out.append(Finding("A5", clause.id, "flag",
                               f"shares {acc.test} with {other.id} — {MESSAGES['A5']}",
                               flag="OVERLAP"))
        elif acc.kind == "metric" and other.acceptance.metric == acc.metric:
            from docket.runner import threshold_label_tokens
            if threshold_label_tokens(acc.threshold) & threshold_label_tokens(other.acceptance.threshold):
                out.append(Finding("A5", clause.id, "flag",
                                   f"shares {acc.metric} with {other.id} and thresholds collide — {MESSAGES['A5']}",
                                   flag="OVERLAP"))
        elif acc.kind == "command" and other.acceptance.command == acc.command \
                and other.acceptance.expect != acc.expect:
            out.append(Finding("A5", clause.id, "flag",
                               f"same command as {other.id}, different expectation — {MESSAGES['A5']}",
                               flag="OVERLAP"))
    # A9: risk/evidence match
    if clause.risk == "high" and len(clause.evidence_required or []) < 2:
        out.append(Finding("A9", clause.id, "flag", MESSAGES["A9"], flag="THIN-EVIDENCE"))
    return out
