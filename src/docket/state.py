"""Derived state — the one place green/red/holding is computed. Never stored.

Precedence (design decision 15, first match wins):
  retired → deferred → stuck → review → broken → stale
  → pending-harness → overlap → holding → unstarted
Validity: a record is valid iff rev_at_filing/rev >= last amendment rev
touching its clause (design decision 4).
"""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field
from pathlib import Path

from docket.accord import flag_checks
from docket.model import Clause, Contract
from docket.storage import Ledger


@dataclass
class ClauseView:
    clause: Clause
    state: str
    flags: list[str] = field(default_factory=list)
    evidence_summary: str = "—"
    drift: str = ""
    calibration: tuple[int, int] = (0, 0)   # (clause_defects, verdicts)
    last_activity: str | None = None         # ISO timestamp


def _valid(rec: dict, rev_key: str, floor: int) -> bool:
    return int(rec.get(rev_key, 0)) >= floor


def derive_views(contract: Contract, led: Ledger, root: Path) -> list[ClauseView]:
    views = []
    for clause in contract.clauses:
        views.append(_derive_one(clause, contract, led, root))
    return views


def _derive_one(clause: Clause, contract: Contract, led: Ledger, root: Path) -> ClauseView:
    floor = led.last_amend_rev(contract.contract, clause.id)
    bundles = [b for b in led.records(clause.id, "bundle") if _valid(b, "rev_at_filing", floor)]
    checks = [c for c in led.records(clause.id, "check") if _valid(c, "rev", floor)]
    verdicts = [v for v in led.records(clause.id, "verdict") if _valid(v, "rev", floor)]
    all_verdicts = led.records(clause.id, "verdict")  # calibration counts ALL history

    flags = [f.flag for f in flag_checks(clause, list(contract.clauses), root)]
    defects = sum(1 for v in all_verdicts if v.get("rejection_type") == "clause-defect")
    cal = (defects, len(all_verdicts))

    latest_bundle = bundles[-1] if bundles else None
    latest_check = checks[-1] if checks else None
    judged = {v.get("bundle") for v in verdicts}
    accepted = [v for v in verdicts if v.get("verdict") == "accepted"]
    # an accepted verdict whose bundle got invalidated by a later amendment:
    stale_accept = [v for v in led.records(clause.id, "verdict")
                    if v.get("verdict") == "accepted" and not _valid(v, "rev", floor)]

    state = "unstarted"
    if clause.status == "retired":
        state = "retired"
    elif clause.status == "deferred":
        state = "deferred"
    elif latest_bundle and latest_bundle.get("claim") == "stuck" \
            and latest_bundle["_file"].removesuffix(".json") not in judged:
        state = "stuck"
    elif latest_bundle and latest_bundle["_file"].removesuffix(".json") not in judged:
        state = "review"
    elif latest_check and latest_check.get("result") == "red":
        state = "broken"
    elif stale_accept and not accepted:
        state = "stale"
    elif "PENDING-HARNESS" in flags:
        state = "pending-harness"
    elif "OVERLAP" in flags:
        state = "overlap"
    elif accepted:
        state = "holding"

    summary = "—"
    if latest_bundle:
        kinds = [e.get("kind", "?") for e in latest_bundle.get("evidence", [])]
        summary = ", ".join(f"{kinds.count(k)} {k}" for k in dict.fromkeys(kinds)) or "—"
        if state == "review":
            summary = "awaiting verdict"
    if state == "broken" and latest_check:
        summary = (summary + ", 1 FAIL") if summary != "—" else "1 FAIL"

    stamps = [r.get("at", "") for r in (*bundles, *checks, *verdicts) if r.get("at")]
    return ClauseView(clause=clause, state=state, flags=flags,
                      evidence_summary=summary,
                      drift=(latest_check or {}).get("drift", ""),
                      calibration=cal,
                      last_activity=max(stamps, default=None))


def freshness(views: list[ClauseView]) -> str:
    stamps = [v.last_activity for v in views if v.last_activity]
    if not stamps:
        return "—"
    newest = dt.datetime.fromisoformat(max(stamps))
    age = dt.datetime.now(newest.tzinfo) - newest
    h = int(age.total_seconds() // 3600)
    return f"{h}h" if h < 48 else f"{h // 24}d"
