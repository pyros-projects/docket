from __future__ import annotations

import argparse
import sys
from pathlib import Path

from docket import __version__


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="docket")
    p.add_argument("--version", action="version", version=f"docket {__version__}")
    p.add_argument("--root", type=Path, default=Path.cwd(),
                   help="repo root containing .contracts/ (default: cwd)")
    sub = p.add_subparsers(dest="cmd")

    imp = sub.add_parser("import", help="admit a contract file through the Accord")
    imp.add_argument("file", type=Path)
    imp.add_argument("--sign-unanchored", metavar="AUTHORITY", default=None)

    chk = sub.add_parser("check", help="run acceptance, name drift, record result")
    chk.add_argument("clause", nargs="?", default=None)
    chk.add_argument("--all", action="store_true")
    chk.add_argument("--quiet", action="store_true")

    sub.add_parser("status", help="the glance — derived state of every clause")

    sub.add_parser("audit", help="coverage views — incompleteness made inspectable")

    tsk = sub.add_parser("tasks", help="derived task view: clause minus evidence")
    tsk.add_argument("--next", action="store_true")
    tsk.add_argument("--json", action="store_true")

    fil = sub.add_parser("file", help="file an evidence bundle (append-only)")
    fil.add_argument("clause")
    fil.add_argument("--bundle", type=Path, required=True)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.cmd is None:
        print("docket: no command given (try: docket status)", file=sys.stderr)
        return 2
    return {"import": cmd_import, "check": cmd_check, "status": cmd_status,
            "audit": cmd_audit, "tasks": cmd_tasks, "file": cmd_file}[args.cmd](args)


def cmd_import(args) -> int:
    from docket.accord import Finding, run_door
    from docket.model import Contract, dump_contract, load_contract_data
    from docket.render import import_report
    from docket.storage import Ledger

    led = Ledger(args.root)
    try:
        data = load_contract_data(args.file)
    except Exception as e:
        print(f"docket import: cannot read {args.file}: {e}", file=sys.stderr)
        return 2

    name = data.get("contract")
    if not name:
        print("docket import: file has no 'contract' name", file=sys.stderr)
        return 2
    dest = led.contract_path(name)
    if dest.exists():
        print(f"docket import: {dest} already exists — amend the law, don't re-import it",
              file=sys.stderr)
        return 2

    # clause ids are per-project monotonic (concepts/01) — the flat
    # evidence/<clause>/ namespace depends on it, so A7 extends across contracts
    existing_ids = {cl.id: c.contract for c in led.contracts() for cl in c.clauses}

    extra_cohort = [cl for c in led.contracts() for cl in c.clauses]
    rep = run_door(data, args.root, sign_unanchored=args.sign_unanchored,
                   extra_cohort=extra_cohort)

    collisions = [c for c in rep.admitted if c.id in existing_ids]
    for c in collisions:
        rep.refusals.append(Finding("A7", c.id, "refuse",
            f"clause id already law in contract {existing_ids[c.id]!r} — ids are per-project monotonic"))
    rep.admitted = [c for c in rep.admitted if c.id not in existing_ids]
    rep.flags = [f for f in rep.flags if f.clause_id not in {c.id for c in collisions}]

    if not rep.admitted:
        print(import_report(name, data.get("rev", 0), str(data.get("source", "?")),
                            [], rep, "(nothing written)"))
        print("docket import: no clauses admitted"
              + (" (file has no clauses)" if not data.get("clauses") else ""),
              file=sys.stderr)
        return 2

    # law: write only admitted clauses (refused clauses do not enter)
    admitted_ids = {c.id for c in rep.admitted}
    data["clauses"] = [c for c in data["clauses"]
                       if isinstance(c, dict) and c.get("id") in admitted_ids]
    dump_contract(data, dest)

    # history: the founding import is an amendment record (design decision 3)
    contract = Contract.model_validate(data)
    led.append_amendment(name, {
        "rev": contract.rev, "by": args.sign_unanchored or "import",
        "kind": "import",
        "changes": [{"id": c.id, "change": "added"} for c in rep.admitted],
        "overrides": rep.overrides,
        "refused": [{"id": f.clause_id, "check": f.check} for f in rep.refusals],
    })

    print(import_report(name, contract.rev, contract.source, contract.signed,
                        rep, str(dest.relative_to(args.root))))
    return 0


def cmd_check(args) -> int:
    from docket.render import check_line
    from docket.runner import run_acceptance
    from docket.storage import Ledger

    led = Ledger(args.root)
    if not args.all and args.clause is None:
        print("docket check: name a clause or pass --all", file=sys.stderr)
        return 2

    failures = 0
    matched = 0
    for contract in led.contracts():
        for clause in contract.clauses:
            if clause.status != "active":
                continue
            if not args.all and clause.id != args.clause:
                continue
            matched += 1
            res = run_acceptance(clause.acceptance, args.root, led.runner_template)
            if res.result in ("green", "red"):
                led.append_record(clause.id, "check", {
                    "clause": clause.id, "rev": contract.rev,
                    "result": res.result, "detail": res.detail, "drift": res.drift,
                })
            if res.result == "red":
                failures += 1
            if not args.quiet:
                print(check_line(clause, res))

    if not args.all and matched == 0:
        print(f"docket check: no active clause {args.clause!r} in any contract",
              file=sys.stderr)
        return 2

    # stale clauses fail CI too (concepts/02 §4: any broken/stale clause fails the build)
    from docket.state import derive_views
    for contract in led.contracts():
        for v in derive_views(contract, led, args.root):
            if v.state == "stale" and (args.all or v.clause.id == args.clause):
                failures += 1
                if not args.quiet:
                    print(f"{v.clause.id} stale — evidence invalidated at rev "
                          f"{contract.rev}; re-verdict needed")

    return 1 if failures else 0


def cmd_status(args) -> int:
    from docket.render import ONBOARDING, status_report
    from docket.state import derive_views, freshness
    from docket.storage import Ledger

    led = Ledger(args.root)
    contracts = led.contracts()
    if not contracts:
        print(ONBOARDING)
        return 0
    for contract in contracts:
        views = derive_views(contract, led, args.root)
        print(status_report(contract, views, freshness(views)))
    return 0


def cmd_audit(args) -> int:
    from docket.render import audit_report
    from docket.state import derive_views
    from docket.storage import Ledger
    led = Ledger(args.root)
    for contract in led.contracts():
        print(audit_report(contract, derive_views(contract, led, args.root),
                           led.coverage_manifest()))
    return 0


def cmd_tasks(args) -> int:
    import json as _json
    from docket.state import derive_views
    from docket.storage import Ledger
    led = Ledger(args.root)
    todo = []
    for contract in led.contracts():
        for v in derive_views(contract, led, args.root):
            if v.state in ("unstarted", "broken", "pending-harness", "stale"):
                todo.append((contract, v))
    if not todo:
        print("docket clear — every active clause is holding or awaiting verdict")
        return 0
    if args.next:
        contract, v = todo[0]
        if args.json:
            bundles = led.records(v.clause.id, "bundle")
            print(_json.dumps({
                "clause": v.clause.id,
                "obligation": v.clause.obligation.strip(),
                "acceptance": v.clause.acceptance.model_dump(exclude_none=True),
                "rev": contract.rev,
                "filed_evidence": [b["_file"] for b in bundles],
            }))
        else:
            print(f"{v.clause.id} [{v.state}] {v.clause.obligation.strip()[:90]}")
        return 0
    for contract, v in todo:
        print(f"{v.clause.id} [{v.state}] {v.clause.obligation.strip()[:90]}")
    return 0


def cmd_file(args) -> int:
    import json as _json
    from docket.storage import Ledger
    led = Ledger(args.root)
    try:
        payload = _json.loads(Path(args.bundle).read_text())
    except Exception as e:
        print(f"docket file: malformed bundle — {e}", file=sys.stderr)
        return 2
    required = {"clause", "claim", "filed_by", "rev_at_filing", "evidence"}
    if not required <= set(payload):
        print(f"docket file: malformed bundle — missing {sorted(required - set(payload))}",
              file=sys.stderr)
        return 2
    if payload["clause"] != args.clause:
        print(f"docket file: bundle names clause {payload['clause']!r} but you are "
              f"filing under {args.clause!r} — refused", file=sys.stderr)
        return 2
    target = None
    for contract in led.contracts():
        for clause in contract.clauses:
            if clause.id == args.clause:
                target = (contract, clause)
                break
        if target:
            break
    if target is None:
        print(f"docket file: unknown clause {args.clause}", file=sys.stderr)
        return 2
    contract, clause = target
    if payload["rev_at_filing"] != contract.rev:
        print(f"docket file: rev mismatch — bundle filed against rev "
              f"{payload['rev_at_filing']}, law is rev {contract.rev}. refile.",
              file=sys.stderr)
        return 2
    if payload["claim"] == "stuck" and "stuck_on" not in payload:
        print("docket file: a failure report needs stuck_on", file=sys.stderr)
        return 2
    p = led.append_record(args.clause, "bundle", payload)
    print(f"✔ filed → review queue (status: ⚖) · {p.relative_to(args.root)}")
    return 0


def entry() -> None:
    raise SystemExit(main())
