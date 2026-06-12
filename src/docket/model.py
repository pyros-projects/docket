"""Schema per docs/concepts/01 — the graduation fixtures are ground truth."""
from __future__ import annotations

import datetime as _dt
from pathlib import Path
from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from ruamel.yaml import YAML

ANCHOR_TYPES = ("surface", "decision", "incident", "regulation", "sla", "compat")
QUALITATIVE_WORDS = frozenset({
    "fast", "quick", "quickly", "slow", "reliable", "reliably", "scalable",
    "performant", "efficient", "efficiently", "responsive", "instant",
    "instantly", "lightweight", "snappy", "robust",
})

_yaml = YAML(typ="rt")  # round-trip: amendments must diff cleanly
_yaml.preserve_quotes = True


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class AcceptanceTest(_Strict):
    test: str

    @property
    def kind(self) -> str:
        return "test"

    @property
    def target(self) -> str:
        return self.test.split("::", 1)[0]


class AcceptanceMetric(_Strict):
    metric: str
    threshold: str

    @property
    def kind(self) -> str:
        return "metric"

    @property
    def target(self) -> str:
        return self.metric.split()[0]


class AcceptanceCommand(_Strict):
    command: str
    expect: str

    @property
    def kind(self) -> str:
        return "command"

    @property
    def target(self) -> str:  # first shell token only — NOT authoritative for A3; use runner.command_harness_missing
        return self.command.split()[0]


class AcceptanceHuman(_Strict):
    verdict: Literal["human"]

    @property
    def kind(self) -> str:
        return "human"

    @property
    def target(self) -> str:
        return ""


Acceptance = Union[AcceptanceTest, AcceptanceMetric, AcceptanceCommand, AcceptanceHuman]


class Anchor(_Strict):
    """Exactly one key, of a known type (unknown type / wrong arity = A7 schema error)."""
    surface: Optional[str] = None
    decision: Optional[str] = None
    incident: Optional[str] = None
    regulation: Optional[str] = None
    sla: Optional[str] = None
    compat: Optional[str] = None

    @property
    def typ(self) -> str:
        for t in ANCHOR_TYPES:
            if getattr(self, t) is not None:
                return t
        raise ValueError("empty anchor")

    @property
    def value(self) -> str:
        return getattr(self, self.typ)

    @field_validator("*", mode="after")
    @classmethod
    def _nonempty(cls, v):
        if v == "":
            raise ValueError("anchor value must be non-empty")
        return v

    @model_validator(mode="after")
    def _exactly_one(self):
        n = sum(getattr(self, t) is not None for t in ANCHOR_TYPES)
        if n != 1:
            raise ValueError(f"anchor must carry exactly one typed key, got {n}")
        return self


class Scope(_Strict):
    applies_to: list[str] = Field(default_factory=list)
    excludes: list[str] = Field(default_factory=list)


class Clause(_Strict):
    id: Annotated[str, Field(pattern=r"^[A-Z][A-Z0-9]*-\d+[a-z]?$")]
    obligation: str
    acceptance: Acceptance
    anchors: list[Anchor] = Field(default_factory=list)  # empty = A2's job, not schema's
    status: Literal["active", "deferred", "retired"] = "active"
    risk: Optional[Literal["low", "medium", "high"]] = None
    evidence_required: Optional[list[str]] = None
    scope: Optional[Scope] = None
    notes: Optional[str] = None


class SignEntry(_Strict):
    rev: int
    by: str
    date: str

    @field_validator("date", mode="before")
    @classmethod
    def _date_str(cls, v):  # YAML parses bare 2026-06-12 as datetime.date
        return v.isoformat() if isinstance(v, _dt.date) else str(v)


class Contract(_Strict):
    contract: str
    rev: int
    source: str
    signed: list[SignEntry] = Field(default_factory=list)
    clauses: list[Clause] = Field(default_factory=list)


def load_contract_data(path: Path) -> dict:
    """Raw mapping — the door needs pre-validation access for A1-vs-A7 routing."""
    with open(path) as f:
        data = _yaml.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: not a YAML mapping")
    return data


def load_contract_file(path: Path) -> Contract:
    return Contract.model_validate(load_contract_data(path))


def dump_contract(contract_data: dict, path: Path) -> None:
    """Round-trip dump of the (possibly ruamel-typed) mapping."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        _yaml.dump(contract_data, f)
