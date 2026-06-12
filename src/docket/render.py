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
