"""All terminal output. Templates are behavioral commitments from concepts/02.

The red-state footer is the D0-004 invariant: every red state prints at
least one work-exit and one law-exit.
"""
from __future__ import annotations

from docket.accord import DoorReport

GLYPH = {"holding": "✔", "review": "⚖", "broken": "✘", "stale": "↻",
         "stuck": "⚠", "pending-harness": "◌", "overlap": "⚑",
         "unstarted": "○", "deferred": "⏸", "retired": "·"}

TWO_EXITS = ("  → fix the code or amend the contract. The docket does not care\n"
             "    which, but it will not go green by argument.")


def short_name(clause) -> str:
    words = clause.obligation.strip().split()
    return " ".join(words[:5])[:40]


def check_line(clause, res) -> str:
    pad = max(2, 55 - len(f"{clause.id} {short_name(clause)}"))
    head = f"{clause.id} {short_name(clause)} " + "." * pad
    if res.result == "green":
        return f"{head} green"
    if res.result == "pending-harness":
        return f"{head} PENDING-HARNESS\n  {res.detail}"
    if res.result == "human":
        return f"{head} verdict: human — cannot go green mechanically; route to docket review"
    body = [f"{head} FAIL",
            f"  obligation:  {clause.obligation.strip()[:100]}",
            f"  evidence:    {res.detail}"]
    if res.drift:
        body.append(f"  drift:       {res.drift}")
    body.append("")
    body.append(TWO_EXITS)
    return "\n".join(body)


def status_report(contract, views, fresh: str) -> str:
    n_amend = max(0, contract.rev - 1)
    head = f"DOCKET — {contract.contract}"
    lines = [f"{head:<52}rev {contract.rev} ({n_amend} amendment{'s' * (n_amend != 1)})",
             f"source: {contract.source}", ""]
    lines.append(f"  {'CLAUSE':<38}{'EVIDENCE':<18}STATE")
    for v in views:
        name = f"{v.clause.id} {short_name(v.clause)}"[:36]
        state = f"{GLYPH[v.state]} {v.state if v.state != 'stale' else 're-verdict'}"
        # outstanding Accord flags never hide behind a stronger state (decision 15);
        # skip the flag already shown AS the state (e.g. pending-harness/overlap)
        extra = [f for f in v.flags if f.lower() != v.state]
        if extra:
            state += " " + " ".join(f"⚑{f}" for f in extra)
        lines.append(f"  {name:<38}{v.evidence_summary[:16]:<18}{state}")
    lines.append("")
    n_review = sum(1 for v in views if v.state == "review")
    n_broken = sum(1 for v in views if v.state == "broken")
    lines.append(f"  {n_review} awaiting your verdict · {n_broken} broken · "
                 f"evidence freshness: {fresh}")
    if n_broken:
        lines.append("")
        lines.append(TWO_EXITS)
    return "\n".join(lines)


ONBOARDING = ("no contracts in .contracts/ — this docket is empty.\n"
              "  bring law to the courtroom:  docket import <file.contract.yaml>")


FAILURE_TOKENS = ("failure", "denied", "error", "timeout", "conflict", "invalid")


def audit_report(contract, views, manifest) -> str:
    covered = sorted({a.value for v in views for a in v.clause.anchors
                      if a.typ == "surface" and v.clause.status == "active"})
    lines = [f"COVERAGE — {contract.contract}".ljust(52) + f"rev {contract.rev}"]
    if manifest:
        cells = manifest["cells"]
        deferred = [c for c in manifest["deferred"] if c in cells]
        uncovered = [c for c in cells if c not in covered and c not in deferred]
        lines.append(f"  surface cells:   {len([c for c in cells if c in covered])}/{len(cells)} covered"
                     f" · deferred (signed): {len(deferred)} · {len(uncovered)} UNCOVERED")
        for c in uncovered:
            lines.append(f"     UNCOVERED:    {c}")
    else:
        lines.append(f"  surface cells:   covered: {len(covered)} "
                     f"(no coverage manifest — uncovered regions unknown)")
    fail_cov = [c for c in covered if any(t in c.lower() for t in FAILURE_TOKENS)]
    lines.append(f"  failure states:  {len(fail_cov)} contracted")
    metrics = [v for v in views if v.clause.acceptance.kind == "metric"]
    lines.append(f"  NFR targets:     {len(metrics)}/{len(metrics)} numbered")
    high = [v for v in views if v.clause.risk == "high"]
    ok = all(len(v.clause.evidence_required or []) >= 2 for v in high)
    lines.append(f"  risk:            {len(high)} high-risk clause{'s' * (len(high) != 1)}"
                 + (f" · evidence_required ≥2 on all ✔" if high and ok else
                    (" · THIN-EVIDENCE outstanding ✘" if high else "")))
    humans = sum(1 for v in views if v.clause.acceptance.kind == "human")
    lines.append(f"  human verdict:   {humans} clause{'s' * (humans != 1)}")
    flags = sorted({f for v in views for f in v.flags})
    if flags:
        lines.append(f"  open flags:      {', '.join(flags)}")
    lines.append("")
    lines.append("  → uncovered regions are visible. Contract them, defer them signed,")
    lines.append("    or accept the dark. The audit does not pretend completeness —")
    lines.append("    it makes incompleteness inspectable.")
    return "\n".join(lines)


def import_report(name: str, rev: int, source: str, signed: list,
                  rep: DoorReport, dest: str) -> str:
    lines = [f"DOCKET IMPORT — {name} rev {rev}", f"source: {source}"]
    if signed:
        s = signed[-1]
        lines.append(f"signed: rev {s.rev} by {s.by} ({s.date})")
    else:
        lines.append("signed: NONE — law without signature (sign with: docket sign)")
    lines.append(f"admitted: {len(rep.admitted)}")
    for o in rep.overrides:
        lines.append(f"  ✍ {o['id']} [A2] admitted unanchored — signed by {o['signed_by']}")
    lines.append(f"refused: {len(rep.refusals)}")
    for f in rep.refusals:
        lines.append(f"  ✘ {f.clause_id} [{f.check}] {f.message}")
    if rep.flags:
        lines.append(f"flags: {len(rep.flags)}")
        for f in rep.flags:
            glyph = "◌" if f.flag == "PENDING-HARNESS" else "⚑"
            lines.append(f"  {glyph} {f.clause_id} [{f.check}] {f.flag} — {f.message}")
    lines.append(f"→ {dest}")
    return "\n".join(lines)
