"""File-native ledger IO. Law = .contracts/*.contract.yaml; history = append-only JSON.

Layout (concepts/01 + design decision 3):
  .contracts/<name>.contract.yaml
  .contracts/evidence/<CLAUSE>/{bundle,check,verdict}-NNN.json
  .contracts/amendments/<name>/rev-NNN-seq-NNN.json
  .contracts/drafts/<name>.rev<N>.yaml          (Plan 2)
  .contracts/runners.yaml                        (optional)
  .contracts/coverage.yaml                       (optional)
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

from ruamel.yaml import YAML

from docket.model import Contract, load_contract_data, load_contract_file

_yaml = YAML(typ="safe")


def now_iso() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


class Ledger:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.dir = self.root / ".contracts"

    # -- law ---------------------------------------------------------------
    def contract_paths(self) -> list[Path]:
        return sorted(self.dir.glob("*.contract.yaml"))

    def contracts(self) -> list[Contract]:
        return [load_contract_file(p) for p in self.contract_paths()]

    def contract(self, name: str) -> Contract:
        return load_contract_file(self.contract_path(name))

    def contract_path(self, name: str) -> Path:
        return self.dir / f"{name}.contract.yaml"

    def contract_data(self, name: str) -> dict:
        return load_contract_data(self.contract_path(name))

    # -- per-clause history (append-only) -----------------------------------
    def _clause_dir(self, clause_id: str) -> Path:
        return self.dir / "evidence" / clause_id

    def records(self, clause_id: str, kind: str) -> list[dict]:
        d = self._clause_dir(clause_id)
        if not d.exists():
            return []
        out = []
        for p in sorted(d.glob(f"{kind}-*.json")):
            rec = json.loads(p.read_text())
            rec["_file"] = p.name
            out.append(rec)
        return out

    def append_record(self, clause_id: str, kind: str, payload: dict) -> Path:
        d = self._clause_dir(clause_id)
        d.mkdir(parents=True, exist_ok=True)
        n = len(list(d.glob(f"{kind}-*.json"))) + 1
        p = d / f"{kind}-{n:03d}.json"
        payload.setdefault("at", now_iso())
        p.write_text(json.dumps(payload, indent=2) + "\n")
        return p

    # -- amendment history ---------------------------------------------------
    def _amend_dir(self, contract: str) -> Path:
        return self.dir / "amendments" / contract

    def amendments(self, contract: str) -> list[dict]:
        d = self._amend_dir(contract)
        if not d.exists():
            return []
        return [json.loads(p.read_text()) for p in sorted(d.glob("rev-*.json"))]

    def append_amendment(self, contract: str, payload: dict) -> Path:
        d = self._amend_dir(contract)
        d.mkdir(parents=True, exist_ok=True)
        seq = len(list(d.glob("rev-*.json"))) + 1
        payload.setdefault("at", now_iso())
        p = d / f"rev-{payload['rev']:03d}-seq-{seq:03d}.json"
        p.write_text(json.dumps(payload, indent=2) + "\n")
        return p

    def last_amend_rev(self, contract: str, clause_id: str) -> int:
        revs = [a["rev"] for a in self.amendments(contract)
                if any(ch["id"] == clause_id for ch in a.get("changes", []))]
        return max(revs, default=0)

    # -- optional config -------------------------------------------------------
    def runner_template(self, kind: str) -> str:
        defaults = {"test": "pytest -q {ref}"}
        p = self.dir / "runners.yaml"
        if p.exists():
            data = _yaml.load(p.read_text()) or {}
            return (data.get("runners") or {}).get(kind, defaults[kind])
        return defaults[kind]

    def coverage_manifest(self) -> dict | None:
        p = self.dir / "coverage.yaml"
        if not p.exists():
            return None
        data = _yaml.load(p.read_text()) or {}
        return {"cells": list(data.get("cells") or []),
                "deferred": list(data.get("deferred") or [])}
