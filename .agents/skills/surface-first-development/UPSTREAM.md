# Provenance — read before editing

Copied 2026-06-12 from the canonical source:
`limitless/plugins/limitless/skills/surface-first-development/`
(limitless plugin 0.10.2, whitepaper v0.6, SKILL.md pre-0.7).

**Status update (2026-06-12, same day):** this copy now IMPLEMENTS the
docket-emitting variant — taken through the dojo (baseline RED → GREEN →
pressure-test; record at `docs/dojo/sfd-docket-variant-record.md` in this
repo). The 4-point delta below is realized in SKILL.md (Phases 4.5, 5, 5.5,
Gates 1–2) and `references/contract-emission.md` (schema, Accord A1–A9,
round-trip protocol). The whitepaper remains v0.6: for contract derivation
the variant supersedes it (stated in SKILL.md's Reference section); the
upstream 0.7 revision in limitless is tracked separately via
`docs/upstream/2026-06-12-sfd-0.7-contracts-are-the-product-design.md`.
The adaptation's eventual home is the producer's repo (limitless), per
boundary discipline — Docket itself stays producer-agnostic and this
directory must never become a dependency of the docket tool.

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
