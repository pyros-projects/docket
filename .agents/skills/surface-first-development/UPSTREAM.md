# Provenance — read before editing

Copied 2026-06-12 from the canonical source:
`limitless/plugins/limitless/skills/surface-first-development/`
(limitless plugin 0.10.2, whitepaper v0.6, SKILL.md pre-0.7).

**Purpose of this copy:** working material for the **docket-emitting SFD
variant** — the version whose Phase 5 emits `.contracts/*.contract.yaml`
clauses that pass the door policy (see `docs/concepts/01`). Develop the
variant here, against the door; the adaptation's eventual home is the
producer's repo (limitless), per boundary discipline — Docket itself stays
producer-agnostic and this directory must never become a dependency of the
docket tool.

**The variant's delta over upstream (small by design — the door and the
SFD 0.7 levers were co-designed):**

1. Phase 5 emits the clause YAML format directly (schema in
   `docs/concepts/01`), not prose contract docs.
2. The Clause Log (0.7 lever 3.1) carries `C-NNN` IDs and `state-cells:` —
   these become the clause IDs and `surface:` anchors verbatim.
3. New pre-Gate-2 step: **self-admission** — run the door checks (A1–A7)
   over the drafted contract file before handoff; refusals are fixed at the
   source, where they're cheapest.
4. The Handoff Bundle includes the `.contract.yaml` file as the primary
   artifact; the round-trip test (0.7 lever 3.2) runs against it.

Upstream improvement spec (the 0.7 design this variant builds on):
`docs/upstream/2026-06-12-sfd-0.7-contracts-are-the-product-design.md`
(copy; canonical lives in `limitless/docs/brainstorm/`).
