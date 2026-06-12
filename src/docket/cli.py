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

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.cmd is None:
        print("docket: no command given (try: docket status)", file=sys.stderr)
        return 2
    return {"import": cmd_import}[args.cmd](args)


def cmd_import(args) -> int:
    from docket.accord import run_door
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

    rep = run_door(data, args.root, sign_unanchored=args.sign_unanchored)
    if not rep.admitted:
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


def entry() -> None:
    raise SystemExit(main())
